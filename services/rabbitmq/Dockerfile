FROM rabbitmq:3.7.8

RUN mkdir /code
WORKDIR /scripts

ADD rabbitmq.conf /etc/rabbitmq
ADD enabled_plugins /etc/rabbitmq
ADD init.sh /scripts/

RUN apt-get update
RUN apt-get install -y curl

CMD ["sh", "/scripts/init.sh"]

