# Rest API

Kalliope provides the REST API to manage the synapses. For configuring the API refer to the [settings documentation](settings.md).

## Synapse API

| Method | URL                      | Action                      |
|--------|--------------------------|-----------------------------|
| GET    | /synapses                | List synapses               |
| GET    | /synapses/<synapse_name> | Show synapse details        |
| POST   | /synapses/<synapse_name> | Run a synapse by its name   |
| POST   | /order                   | Run a synapse from an order |

## Curl examples

>**Note:** --user is only needed if `password_protected` is True

### List synapses

Normal response codes: 200
Error response codes: unauthorized(401), itemNotFound(404)
Curl command:
```
curl -i --user admin:secret -X GET  http://localhost:5000/synapses/
```

Output example:
```
{
  "synapses": [
    [
      {
        "name": "stop-kalliope",
        "neurons": [
          {
            "say": {
              "message": "Good bye"
            }
          },
          "kill_switch"
        ],
        "signals": [
          {
            "order": "close"
          }
        ]
      }
    ],
    [
      {
        "name": "say-hello",
        "neurons": [
          {
            "say": {
              "message": [
                "Bonjour monsieur"
              ]
            }
          }
        ],
        "signals": [
          {
            "order": "bonjour"
          }
        ]
      }
    ]
  ]
}
```

### Show synapse details 

Normal response codes: 200
Error response codes: unauthorized(401), itemNotFound(404)
Curl command:
```
curl -i --user admin:secret -X GET  http://localhost:5000/synapses/say-hello
```

Output example:
```
{
  "synapses": {
    "name": "say-hello",
    "neurons": [
      {
        "say": {
          "message": [
            "Bonjour monsieur"
          ]
        }
      }
    ],
    "signals": [
      {
        "order": "bonjour"
      }
    ]
  }
}
```

### Run a synapse by its name

Normal response codes: 201
Error response codes: unauthorized(401), itemNotFound(404)
Curl command:
```
curl -i --user admin:secret -X POST  http://localhost:5000/synapses/say-hello
```

Output example:
```
{
  "synapses": {
    "name": "say-hello",
    "neurons": [
      {
        "say": {
          "message": [
            "Bonjour monsieur"
          ]
        }
      }
    ],
    "signals": [
      {
        "order": "bonjour"
      }
    ]
  }
}
```


Run a synapse from an order

Normal response codes: 201
Error response codes: unauthorized(401), itemNotFound(404)

Curl command:
```
curl -i --user admin:secret -H "Content-Type: application/json" -X POST -d '{"order":"my order"}' http://localhost:5000/order
```

If the order contains accent or quotes, use a file for testing with curl
```
cat post.json 
{"order":"j'aime"}
```
Then
```
curl -i --user admin:secret -H "Content-Type: application/json" -X POST --data @post.json http://localhost:5000/order/
```

Output example if the order have matched and so launched synapses:
```
{
  "synapses": [
    {
      "name": "Say-hello", 
      "neurons": [
        {
          "name": "say", 
          "parameters": "{'message': ['Hello sir']}"
        }
      ], 
      "signals": [
        {
          "order": "hello"
        }
      ]
    }
  ]
}
```

If the order haven't match ny synapses:
```
{
  "error": {
    "error": "The given order doesn't match any synapses"
  }
}
```
