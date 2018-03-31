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
| GET    | /mute                             | Get the current mute status        |
| POST   | /mute                             | Switch the mute status             |

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
  "matched_synapses": [
    {
      "matched_order": null,
      "neuron_module_list": [
        {
          "generated_message": "Bonjour monsieur",
          "neuron_name": "Say"
        }
      ],
      "synapse_name": "say-hello-fr"
    }
  ],
  "status": "complete",
  "user_order": null
}

Some neuron inside a synapse will wait for parameters that comes from the order. 
You can provide those parameters by adding a `parameters` list of data.
Curl command:
```bash
curl -i -H "Content-Type: application/json" --user admin:secret -X POST  \
-d '{"parameters": {"parameter1": "value1" }}' \
http://127.0.0.1:5000/synapses/start/id/synapse-id
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
  "matched_synapses": [
    {
      "matched_order": "Bonjour",
      "neuron_module_list": [
        {
          "generated_message": "Bonjour monsieur",
          "neuron_name": "Say"
        }
      ],
      "synapse_name": "say-hello-fr"
    }
  ],
  "status": "complete",
  "user_order": "bonjour"
}
```

If the order haven't match any synapses it will try to run the default synapse if it exists in your settings:
```JSON
{
  "matched_synapses": [
    {
      "matched_order": null,
      "neuron_module_list": [
        {
          "generated_message": "Je n'ai pas compris votre ordre",
          "neuron_name": "Say"
        }
      ],
      "synapse_name": "default-synapse"
    }
  ],
  "status": "complete",
  "user_order": "not existing order"
}
```

Or return an empty list of matched synapse
```
{
  "matched_synapses": [],
  "status": null,
  "user_order": "not existing order"
}

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
  "matched_synapses": [
    {
      "matched_order": "Bonjour",
      "neuron_module_list": [
        {
          "generated_message": "Bonjour monsieur",
          "neuron_name": "Say"
        }
      ],
      "synapse_name": "say-hello-fr"
    }
  ],
  "status": "complete",
  "user_order": "bonjour"
}
```

If the order haven't match any synapses it will try to run the default synapse if it exists in your settings:
```JSON
{
  "matched_synapses": [
    {
      "matched_order": null,
      "neuron_module_list": [
        {
          "generated_message": "Je n'ai pas compris votre ordre",
          "neuron_name": "Say"
        }
      ],
      "synapse_name": "default-synapse"
    }
  ],
  "status": "complete",
  "user_order": "not existing order"
}
```

Or return an empty list of matched synapse
```
{
  "matched_synapses": [],
  "status": null,
  "user_order": "not existing order"
}
```

#### The neurotransmitter case

In case of leveraging the [neurotransmitter neuron](https://github.com/kalliope-project/kalliope/tree/master/kalliope/neurons/neurotransmitter), Kalliope expects back and forth answers.
Fortunately, the API provides a way to continue interaction with Kalliope and still use neurotransmitter neurons while doing API calls.

When you start a synapse via its name or an order (like shown above), the answer of the API call will tell you in the response that kalliope is waiting for a response via the "status" return. 

Status can either by ```complete``` (nothing else to do) or ```waiting_for_answer```, in which case Kalliope is waiting for your response :).

In this case, you can launch another order containing your response.

Let's take as an example the simple [neurotransmitter brain of the EN starter kit](https://github.com/kalliope-project/kalliope_starter_en/blob/master/brains/neurotransmitter.yml):

First step is to fire the "ask me a question order":

```bash
curl -i --user admin:secret -H "Content-Type: application/json" -X POST -d '{"order":"ask me a question"}' http://localhost:5000/synapses/start/order
```

The response should be as follow:

```JSON
{
  "matched_synapses": [
    {
      "matched_order": "ask me a question",
      "neuron_module_list": [
        {
          "generated_message": "do you like french fries?",
          "neuron_name": "Say"
        }
      ],
      "synapse_name": "synapse1"
    }
  ],
  "status": "waiting_for_answer",
  "user_order": "ask me a question"
}
```

The ```"status": "waiting_for_answer"``` indicates that it waits for a response, so let's send it:

```bash
 --user admin:secret -H "Content-Type: application/json" -X POST -d '{"order":"not at all"}' http://localhost:5000/synapses/start/order
```

```JSON
{
  "matched_synapses": [
    {
      "matched_order": "ask me a question",
      "neuron_module_list": [
        {
          "generated_message": "do you like french fries?",
          "neuron_name": "Say"
        },
        {
          "generated_message": null,
          "neuron_name": "Neurotransmitter"
        }
      ],
      "synapse_name": "synapse1"
    },
    {
      "matched_order": "not at all",
      "neuron_module_list": [
        {
          "generated_message": "You don't like french fries.",
          "neuron_name": "Say"
        }
      ],
      "synapse_name": "synapse3"
    }
  ],
  "status": "complete",
  "user_order": null
}

```

And now the status is complete. This works also when you have nested neurotransmitter neurons, you just need to keep monitoring the status from the API answer.

### Get mute status

Normal response codes: 200
Error response codes: unauthorized(401), Bad request(400)

Curl command:
```bash
curl -i --user admin:secret  -X GET  http://127.0.0.1:5000/mute
```

Output example:
```JSON
{
  "mute": true
}
```

### Switch mute status

Normal response codes: 200
Error response codes: unauthorized(401), Bad request(400)

Curl command:
```bash
curl -i -H "Content-Type: application/json" --user admin:secret  -X POST -d '{"mute": "True"}' http://127.0.0.1:5000/mute
```

Output example:
```JSON
{
  "mute": true
}
```