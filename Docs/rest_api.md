# Rest API

Kalliope provides the REST API to manage the synapses. For configuring the API refer to the [settings documentation](settings.md).

## Synapse API

| Method | URL                      | Action               |
|--------|--------------------------|----------------------|
| GET    | /synapses                | List synapses        |
| GET    | /synapses/<synapse_name> | Show synapse details |
| POST   | /synapses/<synapse_name> | Run a synapse        |

## Curl examples

>**Note:** --user is only needed if `password_protected` is True

### Get all synapse

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

### Get one synapse's detail by its name. 

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

### Run a synapse by its name. 

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