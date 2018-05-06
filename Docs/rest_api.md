# Rest API

Kalliope provides the REST API to manage the synapses. For configuring the API refer to the [settings documentation](settings.md).

- [Rest API](#rest-api)
  - [Synapse API](#synapse-api)
  - [Curl examples](#curl-examples)
    - [Get Kalliope's version](#get-kalliopes-version)
    - [List synapses](#list-synapses)
    - [Show synapse details](#show-synapse-details)
    - [Run a synapse by its name](#run-a-synapse-by-its-name)
    - [Run a synapse from an order](#run-a-synapse-from-an-order)
    - [Run a synapse from an audio file](#run-a-synapse-from-an-audio-file)
    - [The neurotransmitter case](#the-neurotransmitter-case)
    - [Get deaf status](#get-deaf-status)
    - [Switch deaf status](#switch-deaf-status)
  - [Mute flag](#mute-flag)
    - [Get mute status](#get-mute-status)
    - [Set mute status](#set-mute-status)

## Synapse API

| Method | URL                               | Action                             |
|--------|-----------------------------------|------------------------------------|
| GET    | /                                 | Get kaliope version                |
| GET    | /synapses                         | List synapses                      |
| GET    | /synapses/<synapse_name>          | Get synapse details by name        |
| POST   | /synapses/start/id/<synapse_name> | Run a synapse by its name          |
| POST   | /synapses/start/order             | Run a synapse from a text order    |
| POST   | /synapses/start/audio             | Run a synapse from an audio sample |
| GET    | /settings/deaf                    | Get the current deaf status        |
| POST   | /settings/deaf                    | Switch the deaf status             |
| GET    | /settings/mute                    | Get the current mute status        |
| POST   | /settings/mute                    | Switch the mute status             |
| GET    | /settings/energy_threshold        | Get the current energy_threshold   |
| POST   | /settings/energy_threshold        | Update the energy_threshold value  |
| GET    | /settings/ambient_noise_second    | Get the ambient_noise_second       |
| POST   | /settings/ambient_noise_second    | Update the ambient_noise_second    |



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
```

The [mute flag](#mute-flag) can be added to this call.
Curl command:
```bash
curl -i -H "Content-Type: application/json" --user admin:secret -X POST \
-d '{"mute":"true"}' http://127.0.0.1:5000/synapses/start/id/say-hello-fr
```

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
```

The [mute flag](#mute-flag) can be added to this call.
Curl command:
```bash
curl -i --user admin:secret -H "Content-Type: application/json" -X POST \
-d '{"order":"my order", "mute":"true"}' http://localhost:5000/synapses/start/order
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

The [mute flag](#mute-flag) can be added to this call with a form.
Curl command:
```bash
curl -i --user admin:secret -X POST http://localhost:5000/synapses/start/audio -F "file=@path/to/file.wav" -F mute="true"
```

### The neurotransmitter case

In case of leveraging the [neurotransmitter neuron](../kalliope/neurons/neurotransmitter), Kalliope expects back and forth answers.
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
curl -i --user admin:secret -H "Content-Type: application/json" -X POST -d '{"order":"not at all"}' http://localhost:5000/synapses/start/order
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

### Get deaf status

Normal response codes: 200
Error response codes: unauthorized(401), Bad request(400)

Curl command:
```bash
curl -i --user admin:secret  -X GET  http://127.0.0.1:5000/deaf
```

Output example:
```JSON
{
  "deaf": true
}
```

### Switch deaf status
Kalliope can switch to 'deaf' mode, so she can not ear you anymore, the trigger/hotword is desactivated.
However Kalliope continues to process synapses.

Normal response codes: 200
Error response codes: unauthorized(401), Bad request(400)

Curl command:
```bash
curl -i -H "Content-Type: application/json" --user admin:secret  -X POST -d '{"deaf": "True"}' http://127.0.0.1:5000/deaf
```

Output example:
```JSON
{
  "deaf": true
}
```

## Mute flag

When you use the API, by default Kalliope will generate a text and process it into the TTS engine.
Some calls to the API can be done with a flag that will tell Kalliope to only return the generated text without processing it into the audio player.
When `mute` is switched to true, Kalliope will not speak out loud on the server side.

### Get mute status

Normal response codes: 200
Error response codes : unauthorized(401), Bad request(400)


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

### Set mute status

Normal response codes: 200
Error response codes : unauthorized(401), Bad request(400)


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

## energy_threshold flag
Define the [energy_threshold](settings.md) in the settigns 

### Get energy_threshold status

Normal response codes: 200
Error response codes : unauthorized(401), Bad request(400)


Curl command:
```bash
curl -i --user admin:secret  -X GET  http://127.0.0.1:5000/settings/energy_threshold
```

Output example:
```JSON
{
  "energy_threshold": 4000
}
```

### Set energy_threshold status

Normal response codes: 200
Error response codes : unauthorized(401), Bad request(400)


Curl command:
```bash
curl -i -H "Content-Type: application/json" --user admin:secret  -X POST -d '{"energy_threshold": 4000}' http://127.0.0.1:5000/settings/energy_threshold
```

Output example:
```JSON
{
  "energy_threshold": 4000
}
```