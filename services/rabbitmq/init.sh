#!/bin/sh

# Create Rabbitmq user
( sleep 5 ; \
rabbitmqctl add_user $RABBITMQ_ALIVE_USER $RABBITMQ_ALIVE_PASSWORD 2>/dev/null ; \
rabbitmqctl set_user_tags $RABBITMQ_ALIVE_USER administrator ; \
rabbitmqctl set_permissions -p / $RABBITMQ_ALIVE_USER  ".*" ".*" ".*" ; \
echo "*** User '$RABBITMQ_ALIVE_USER' with password '$RABBITMQ_ALIVE_PASSWORD' completed. ***" ; \
echo "*** Log in the WebUI at port 15672 (example: http:/localhost:15672) ***") &

# $@ is used to pass arguments to the rabbitmq-server command.
# For example if you use it like this: docker run -d rabbitmq arg1 arg2,
# it will be as you run in the container rabbitmq-server arg1 arg2
rabbitmq-server $@
