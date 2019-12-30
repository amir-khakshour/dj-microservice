FROM python:3.5
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
RUN mkdir /code
WORKDIR /code
COPY requirements/base.txt requirements/dev.txt requirements/test.txt /code/requirements/

RUN pip3 install -r requirements/base.txt \
        && pip install -r requirements/dev.txt \
        && pip install -r requirements/test.txt


ADD scripts/dev/ /code/
ADD . /code/
