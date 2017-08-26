# MQTT Subscriber


## Test with rabbitmq-server broker

### Install rabbitmq

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

### Test publish
Publish a message with amqp-tools in the default rabbitmq exchange with the topic key "test.light"
```
amqp-publish -e "amq.topic" -r "test.light" -b "your message"
```

Test publish json
```
amqp-publish -e "amq.topic" -r "test.light" -b '{"test" : "message"}'
```

### Add TLS to rabbitmq

#### Create root CA

Install openssl
```bash
apt-get install openssl
```

Create PKI structure
```bash
mkdir testca
cd testca
echo 01 > serial
```

Create private key and CA certificate
```bash
openssl req -out ca.key -new -x509 
```

Generate server/key pair
```bash
openssl genrsa -out server.key 2048 
openssl req -key server.key -new -out server.req 
openssl x509 -req -in server.req -CA ca.crt -CAkey privkey.pem -CAserial serial -out server.crt
```

#### Create client certificate/key pair

Create private key
```bash
openssl genrsa -out client.key 2048
```

Create a certificate request
```bash
openssl req -key client.key -new -out client.req 
```

Sign the client request with the CA
```bash
openssl x509 -req -in client.req -CA ca.cert -CAkey privkey.pem -CAserial serial -out client.crt 
```

#### Update rabbitmq configuration

Edit (or create if the file is not present) a config file `/etc/rabbitmq/rabbitmq.config`
```
[
  {rabbit, [
     {ssl_listeners, [5671]},
     {ssl_options, [{cacertfile,"/path/to/ca.cert"},
                    {certfile,"/path/to/server.crt"},
                    {keyfile,"/path/to/server.key"},
                    {verify,verify_peer},
                    {fail_if_no_peer_cert,false}]}
   ]},
  {rabbitmq_mqtt, [
                  {ssl_listeners,    [8883]},
                  {tcp_listeners,    [1883]}
                ]}

].
```

Restart rabbitmq server to take care of changes
```bash
sudo systemctl restart rabbitmq-server
```


