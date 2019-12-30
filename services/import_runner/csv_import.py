import csv
import asyncio
import argparse
import logging
from enum import Enum
from urllib.parse import urlencode
from collections import OrderedDict

import aiohttp
from aiohttp import web, http

from utils import AsyncPool

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())
logging.basicConfig(level=logging.DEBUG, format="%(message)s")

BASE_ENDPOINT = 'http://local.gridscale.com'
CUSTOMER_API_ENDPOINT = '{}/customer/api/1.0/customer/'.format(BASE_ENDPOINT)
PRICE_API_ENDPOINT = '{}/customer/api/1.0/customer/get_price/'.format(BASE_ENDPOINT)
PRODUCT_API_ENDPOINT = '{}/product/api/1.0/product/'.format(BASE_ENDPOINT)
ORDER_API_ENDPOINT = '{}/order/api/1.0/order/'.format(BASE_ENDPOINT)

CUSTOMER_STATUS_DELETED = 'D'
PRODUCT_STATUS_INACTIVE = 'I'

HTTPStatus = Enum('Status', 'ok not_found error')


class FetchError(Exception):
    def __init__(self, order):
        self.order = order


class IntegrityError(Exception):
    def __init__(self, data):
        self.data = data


def build_price_data_params(order, customer, product):
    return {
        'quantity': order['quantity'],
        'type': customer['type'],
        'vat_percentage': customer['vat_percentage'],
        'price_net': product['price_net'],
    }


def serialize_order(order, customer, product):
    return {
        'order_no': order['order_no'],
        'customer_id': customer['id'],
        'product_id': product['id'],
        'quantity': order['quantity'],
        'price_gross': order['price_gross'],
        'price_net': order['price_net'],
    }


async def fetch_product(product_name, session):
    url_params = urlencode(OrderedDict(name=product_name))
    url = '%s?%s' % (PRODUCT_API_ENDPOINT, url_params)
    async with session.get(url) as response:
        if response.status == 200:
            results = await response.json()
            if results['results']:
                product = results['results'][0]
                if product['status'] == PRODUCT_STATUS_INACTIVE:
                    raise IntegrityError("Given product is inactive! name: {}".format(product_name))
                return product
            raise web.HTTPNotFound(reason="Product with name: {} not found!".format(product_name))
        else:
            raise http.HttpProcessingError(
                code=response.status, message=response.reason,
                headers=response.headers)


async def fetch_customer(customer_id, session):
    url = '%s/%s' % (CUSTOMER_API_ENDPOINT, customer_id)
    async with session.get(url) as response:
        if response.status == 200:
            customer = await response.json()
            if customer['status'] == CUSTOMER_STATUS_DELETED:
                raise IntegrityError("Given customer is deleted! customer_id: {}".format(customer_id))
            return customer
        elif response.status == 404:
            raise web.HTTPNotFound(reason="Customer with id: {} not found!".format(customer_id))
        else:
            raise http.HttpProcessingError(
                code=response.status, message=response.reason,
                headers=response.headers)


async def fetch_price(price_params, session):
    url_params = urlencode(price_params)
    url = '%s?%s' % (PRICE_API_ENDPOINT, url_params)
    async with session.get(url) as response:
        if response.status == 200:
            price_details = await response.json()
            return price_details
        else:
            raise http.HttpProcessingError(
                code=response.status, message=response.reason,
                headers=response.headers)


async def persist_order(order_data, session):
    async with session.post(ORDER_API_ENDPOINT, json=order_data) as response:
        if response.status == 201:
            order = await response.json()
            return order
        else:
            raise http.HttpProcessingError(
                code=response.status, message=response.reason,
                headers=response.headers)


async def order_worker(order_row, semaphore, result_queue):
    async with semaphore:
        async with aiohttp.ClientSession() as session:  # TODO make exception handling narrower
            try:
                customer = await fetch_customer(order_row['customer_id'], session)
                # We hit the result set url so we need to extract the result from the set
                product = await fetch_product(order_row['product_name'], session)

                price_params = build_price_data_params(order_row, customer, product)
                price_details = await fetch_price(price_params, session)
                order_row['price_gross'] = price_details['price_gross']
                order_row['price_net'] = price_details['price_net']
                order_data = serialize_order(order_row, customer, product)
                order = await persist_order(order_data, session)
                # else
                status = HTTPStatus.ok
                msg = 'Created Order: {}'.format(order)
                logger.info(msg)
            except web.HTTPNotFound as exc:
                status = HTTPStatus.not_found  # TODO log the specific details
                msg = str(exc)
                logger.error(msg)
            except IntegrityError as exc:
                status = HTTPStatus.error
                msg = str(exc)
                logger.error(msg)
            except Exception as exc:
                logger.error("Unhandled error: {}".format(exc))
                status = HTTPStatus.error
                msg = str(exc)
                logger.error(msg)
                # raise FetchError(order_row) from exc  # TODO re-raise the exception and handle it on the caller

    await result_queue.put({'status': status, 'msg': msg})


def header_is_valid(header):
    valid_headers = {'customer_id', 'order_no', 'product_name', 'quantity'}
    return set(header) == valid_headers


async def main(loop):
    parser = argparse.ArgumentParser(description="Import orders from csv file")
    parser.add_argument('--num', '-n', help="Number of items processing concurrently", metavar='int', type=int, default=32)
    parser.add_argument('--csv', help="Number of items processing concurrently", metavar='file', type=argparse.FileType('r'), required=True)
    parser.add_argument('--max_requests', help="Maximum Number of concurrently http requests", metavar='int', type=int, default=1000)
    options = parser.parse_args()

    result_queue = asyncio.Queue()
    semaphore = asyncio.Semaphore(options.max_requests)

    async with AsyncPool(loop, num_workers=options.num, name="OrderProcessor",
                         logger=logger,
                         worker_co=order_worker, max_task_time=300,
                         expected_total='+1000',
                         log_every_n=10) as pool:
        with options.csv as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            headers = next(csv_reader, None)
            if not header_is_valid(headers):
                print("Can't process CSV file, invalid columns!")  # TODO show more info
            else:
                for row in csv_reader:
                    await pool.push(dict(zip(headers, row)), semaphore, result_queue)

    await result_queue.put(None)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(loop))
