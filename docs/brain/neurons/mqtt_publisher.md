Publish a message to a MQTT broker server

## Input parameters

| parameter    | required | type    | default  | choices             | comment                                                                                            |
| ------------ | -------- | ------- | -------- | ------------------- | -------------------------------------------------------------------------------------------------- |
| broker_ip    | YES      | string  |          |                     | IP address of the MQTT broker server                                                               |
| port         | NO       | int     | 1883     |                     | Port of the broker. By default 1883. 8883 when TLS is activated.                                   |
| topic        | YES      | string  |          |                     | Topic name where the message will be published                                                     |
| payload      | YES      | string  |          |                     | Message to publish on the topic                                                                    |
| qos          | NO       | int     | 0        | 0 or 1 or 2         | The quality of service level to use                                                                |
| retain       | NO       | Boolean | FALSE    | True, False         | if set to True, the message will be set as the “last known good”/retained message for the topic. |
| client_id    | NO       | string  | kalliope |                     | The MQTT client id to use. If not set, the name will be set to "kalliope"                          |
| keepalive    | NO       | int     | 60       |                     | The keepalive timeout value for the client                                                         |
| username     | NO       | string  |          |                     | username for authenticating the client                                                             |
| password     | NO       | string  |          |                     | password for authenticating the client                                                             |
| ca_cert      | NO       | string  |          |                     | Path to the remote server CA certificate used for securing the transport                           |
| certfile     | NO       | string  |          |                     | Path to the client certificate file used for authentication                                        |
| keyfile      | NO       | string  |          |                     | Path to the client key file attached to the client certificate                                     |
| protocol     | NO       | string  | MQTTv311 | MQTTv31 or MQTTv311 | Can be either MQTTv31 or MQTTv311                                                                  |
| tls_insecure | NO       | string  | FALSE    |                     | Set the verification of the server hostname in the server certificate                              |

## Returned values

No returned values

## Synapses example

Publish a message to the topic "my/topic" with minimal configuration
```yaml
- name: "mqtt-publisher-1"
  signals:
    - order: "this is my order"
  neurons:
    - mqtt_publisher:
        broker_ip: "127.0.0.1"
        topic: "my/topic"
        payload: "my message"
```

Publish a json formatted message. Note that anti-slashes must be escaped.
```yaml
- name: "mqtt-publisher-2"
  signals:
    - order: "this is my order"
  neurons:
    - mqtt_publisher:
        broker_ip: "127.0.0.1"
        topic: "mytopic"
        payload: "{\"mykey\": \"myvalue\"}"
```

The broker require authentication
```yaml
- name: "mqtt-publisher-3"
  signals:
    - order: "this is my order"
  neurons:
    - mqtt_publisher:
        broker_ip: "127.0.0.1"
        topic: "my/topic"
        payload: "my message"
        username: "guest"
        password: "guest"
```

The broker require a secure TLS connection
```yaml
- name: "mqtt-publisher-4"
  signals:
    - order: "this is my order"
  neurons:
    - mqtt_publisher:
        broker_ip: "127.0.0.1"
        topic: "my/topic"
        payload: "my message"
        ca_cert: "/path/to/ca.cert"
```

The broker require a secure TLS connection and authentication based on client certificate
```yaml
- name: "mqtt-publisher-5"
  signals:
    - order: "this is my order"
  neurons:
    - mqtt_publisher:
        broker_ip: "127.0.0.1"
        topic: "my/topic"
        payload: "my message"
        ca_cert: "/path/to/ca.cert"
        certfile: "path/to/client.crt"
        keyfile: "path/to/client.key"
```

The broker require a secure TLS connection, an authentication based on client certificate and the CA is a self signed certificate
```yaml
- name: "mqtt-publisher-6"
  signals:
    - order: "this is my order"
  neurons:
    - mqtt_publisher:
        broker_ip: "127.0.0.1"
        topic: "my/topic"
        payload: "my message"
        ca_cert: "/path/to/ca.cert"
        certfile: "path/to/client.crt"
        keyfile: "path/to/client.key"
        tls_insecure: True
```


## Test with CLI

The following part of the documentation can help you to configure your synapse with right options.
From here we suppose that you have already a running broker server on your local machine. If it's not the case, please refer to the documentation of the [signal mqtt_subscriber](../signals/mqtt_subscriber#test-with-rabbitmq-server-broker) to install a testing broker server.

Install a CLI mqtt client
```bash
sudo apt-get install mosquitto-clients
```

Run a subscriber
```bash
mosquitto_sub -t 'this/is/a/topic'
```

Then use your neuron. E.g
```yaml
- name: "test-mqtt-publisher"
  signals:
    - order: "this is my order"
  neurons:
    - mqtt_publisher:
        broker_ip: "127.0.0.1"
        topic: "this/is/a/topic"
        payload: "info"
```
