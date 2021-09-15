Launch synapses when receiving a message on a topic from a MQTT messaging broker server.

> MQTT is a Client Server publish/subscribe messaging transport protocol.
> It is mostly used in communication in Machine to Machine (M2M) and Internet of Things (IoT) contexts.
> The main concept is that a client will publish a message attached to a "topic" to a server called a "broker", and other clients which are interested by the topic will subscribe to it.
> The broker filters all incoming messages and distributes them accordingly.

## Input parameters

| parameter    | required | default  | choices           | comment                                                                                                                                           |
| ------------ | -------- | -------- | ----------------- | ------------------------------------------------------------------------------------------------------------------------------------------------- |
| broker_ip    | YES      |          |                   | IP address of the MQTT broker server.                                                                                                             |
| topic        | YES      |          |                   | topic name to subscribe.                                                                                                                          |
| is_json      | NO       | FALSE    | True, False       | if true, all received messages will be converted into a dict.                                                                                     |
| broker_port  | NO       | 1883     |                   | Port of the broker. By default 1883. 8883 when TLS is activated.                                                                                  |
| client_id    | NO       | kalliope |                   | The client identifier is an identifier of each MQTT client and used by the broker server for identifying the client. Should be unique per broker. |
| keepalive    | NO       | 60       |                   | A time interval in seconds where the clients commits to by sending regular PING Request messages to the broker.                                   |
| password     | NO       |          |                   | password for authenticating the client.                                                                                                           |
| username     | NO       |          |                   | username for authenticating the client.                                                                                                           |
| protocol     | NO       | MQTTv311 | MQTTv31, MQTTv311 | Can be either MQTTv31 or MQTTv311.                                                                                                                |
| ca_cert      | NO       |          |                   | Path to the remote server CA certificate used for securing the transport.                                                                         |
| certfile     | NO       |          |                   | Path to the client certificate file used for authentication.                                                                                      |
| keyfile      | NO       |          |                   | Path to the client key file attached to the client certificate.                                                                                   |
| tls_insecure | NO       | FALSE    | True, False       | Set the verification of the server hostname in the server certificate.                                                                            |

## Values sent to the synapse

| Name                    | Description                      | Type        | sample                                               |
| ----------------------- | -------------------------------- | ----------- | ---------------------------------------------------- |
| mqtt_subscriber_message | message received from the broker | string/dict | "on", "off", {"temperature": "25", "humidity": "30"} |

## Synapses example

### Topic with plain text message

The topic send the status of a light. The received message would be "on" or off"

```yaml
- name: "test-mqtt-1"
  signals:
    - mqtt_subscriber:
        broker_ip: "127.0.0.1"
        topic: "topic1"
  neurons:
    - say:
        message:
          - "The light is now {{ mqtt_subscriber_message }}"
```

Kalliope output example:

```
The light is now on
```

### Topic with json message

In this example, the topic send a json payload that contains multiple information. E.g: `{"temperature": "25", "humidity": "30"}`

```yaml
- name: "test-mqtt-2"
  signals:
    - mqtt_subscriber:
        broker_ip: "127.0.0.1"
        topic: "topic2"
        is_json: True
  neurons:
    - say:
        message:
          - "The temperature is now {{ mqtt_subscriber_message['temperature'] }}, humidity {{ mqtt_subscriber_message['humidity'] percents }}"
```

Kalliope output example:

```
The temperature is now 25 degrees, humidity 30%
```

### The broker require authentication

Password authentication

```yaml
- name: "test-mqtt-3"
  signals:
    - mqtt_subscriber:
        broker_ip: "127.0.0.1"
        topic: "topic 3"
        username: "guest"
        password: "guest"
  neurons:
    - say:
        message:
          - "Message received on topic 3"
```

It's better to use TLS when using password authentication for securing the transport

```yaml
- name: "test-mqtt-4"
  signals:
    - mqtt_subscriber:
        broker_ip: "127.0.0.1"
        broker_port: 8883
        topic: "topic 4"
        username: "guest"
        password: "guest"
        ca_cert: "/path/to/ca.cert"
        tls_insecure: True
  neurons:
    - say:
        message:
          - "Message received on topic 3"
```

Authentication based on client certificate

```yaml
- name: "test-mqtt-5"
  signals:
    - mqtt_subscriber:
        broker_ip: "127.0.0.1"
        broker_port: 8883
        topic: "topic 5"
        ca_cert: "/path/to/ca.cert"
        tls_insecure: True
        certfile: "/path/to/client.crt"
        keyfile: "/path/to/client.key"
  neurons:
    - say:
        message:
          - "Message received on topic 5"
```

## Notes

When you want to use the same broker within your multiple synapses in your brain, you must keep in mind that the configuration must be the same
It means that you cannot declare a synapse that use a broker ip with TLS activated, and another synapse that use the same broker ip but without TLS activated.
When you declare a "broker_ip", a unique object is created once, then topic are added following all synapses

On the other hand, you can subscribe to multiple topics that use json or not within the same broker ip.

```yaml
- name: "synapse-mqtt-1"
  signals:
    - mqtt_subscriber:
        broker_ip: "127.0.0.1"
        topic: "topic1"
        is_json: False
  neurons:
    - say:
        message:
          - "I'm started when message on topic 1"

- name: "synapse-mqtt-2"
  signals:
    - mqtt_subscriber:
        broker_ip: "127.0.0.1"
        topic: "topic2"
        is_json: True
  neurons:
    - say:
        message:
          - "I'm started when message on topic 2"
```

## Test with rabbitmq-server broker

This part can help you to configure your brain by sending message to a local broker

### Install rabbitmq

```bash
sudo apt-get install rabbitmq-server mosquitto-clients
```

Enable mqtt plugin

```bash
sudo rabbitmq-plugins enable rabbitmq_mqtt
sudo systemctl restart rabbitmq-server
```

Active web ui (optional)

```bash
sudo rabbitmq-plugins enable rabbitmq_management
```

Get the cli and make it available to use

```bash
wget http://127.0.0.1:15672/cli/rabbitmqadmin
sudo mv rabbitmqadmin /etc/rabbitmqadmin
sudo chmod 755 /etc/rabbitmqadmin
```

Create admin account (when UI installed)

```bash
sudo rabbitmqctl add_user admin p@ssw0rd
sudo rabbitmqctl set_user_tags admin administrator
sudo rabbitmqctl set_permissions -p / admin ".*" ".*" ".*"
```

### Publish message from CLI

Publish a plain text message

```bash
mosquitto_pub -t 'my_topic' -m 'message'
```

Test publish a json message

```bash
mosquitto_pub -t 'my_topic' -m '{"test" : "message"}'
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
