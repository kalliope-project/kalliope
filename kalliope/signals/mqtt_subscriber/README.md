# MQTT Subscriber

## Install rabbitmq

```
sudo apt-get install rabbitmq-server amqp-tools
```

Enable mqtt plugin
```
sudo rabbitmq-plugins enable rabbitmq_mqtt
sudo systemctl restart rabbitmq-server
```

Active web ui
```bash
sudo rabbitmq-plugins enable rabbitmq_management
```

Get the cli and make it available to use
```
wget http://127.0.0.1:15672/cli/rabbitmqadmin
sudo mv rabbitmqadmin /etc/rabbitmqadmin
sudo chmod 755 /etc/rabbitmqadmin
```

Create admin account
```bash
sudo rabbitmqctl add_user admin p@ssw0rd
sudo rabbitmqctl set_user_tags admin administrator
sudo rabbitmqctl set_permissions -p / admin ".*" ".*" ".*"
```

Publish a message with amqp-tools in the default rabbitmq exchange with the topic key "test.light"
```
amqp-publish -e "amq.topic" -r "test.light" -b "your message"
```


Test publish json
```
amqp-publish -e "amq.topic" -r "test.light" -b '{"test" : "message"}'
```


amqp-publish -e "amq.topic" -r "topic1" -b "your message"