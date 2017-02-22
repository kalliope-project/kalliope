# Rest API

Kalliope provides the REST API to manage the synapses. For configuring the API refer to the [settings documentation](settings.md).

## Synapse API

| Method | URL                               | Action                             |
|--------|-----------------------------------|------------------------------------|
| GET    | /                                 | Get kaliope version                |
| GET    | /synapses                         | List synapses                      |
| GET    | /synapses/<synapse_name>          | Get synapse details by name        |
| POST   | /synapses/start/id/<synapse_name> | Run a synapse by its name          |
| POST   | /synapses/start/order             | Run a synapse from a text order    |
| POST   | /synapses/start/audio             | Run a synapse from an audio sample |

## Curl examples

>**Note:** --user is only needed if `password_protected` is True

### Get Kalliope's version

Normal response codes: 200
Error response codes: unauthorized(401)
Curl command:
```bash
curl -i --user admin:secret -X GET  http://localhost:5000/
```
Output example:
```JSON
{
  "Kalliope version": "0.4.2"
}
```

### List synapses

Normal response codes: 200
Error response codes: unauthorized(401), itemNotFound(404)
Curl command:
```bash
curl -i --user admin:secret -X GET  http://localhost:5000/synapses
```

Output example:
```JSON
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
```bash
curl -i --user admin:secret -X GET  http://localhost:5000/synapses/say-hello
```

Output example:
```JSON
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
```bash
curl -i --user admin:secret -X POST  http://localhost:5000/synapses/start/id/say-hello
```

Output example:
```JSON
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


### Run a synapse from an order

Normal response codes: 201
Error response codes: unauthorized(401), itemNotFound(404)

Curl command:
```bash
curl -i --user admin:secret -H "Content-Type: application/json" -X POST -d '{"order":"my order"}' http://localhost:5000/synapses/start/order
```

If the order contains accent or quotes, use a file for testing with curl
```bash
cat post.json 
{"order":"j'aime"}
```
Then
```bash
curl -i --user admin:secret -H "Content-Type: application/json" -X POST --data @post.json http://localhost:5000/synapses/start/order
```

Output example if the order have matched and so launched synapses:
```JSON
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

If the order haven't match any synapses:
```JSON
{
  "error": {
    "error": "The given order doesn't match any synapses"
  }
}
```

### Run a synapse from an audio file

Normal response codes: 201
Error response codes: unauthorized(401), itemNotFound(404)

The audio file must use WAV or MP3 extension.

Curl command:
```bash
curl -i --user admin:secret -X POST  http://localhost:5000/synapses/start/audio -F "file=@/home/nico/Desktop/input.wav"
```

Output example if the order inside the audio have matched and so launched synapses:
```JSON
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

If the order haven't match any synapses:
```JSON
{
  "error": {
    "error": "The given order doesn't match any synapses"
  }
}
```
