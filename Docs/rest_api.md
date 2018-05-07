# Rest API

Kalliope provides the REST API to manage the synapses. For configuring the API refer to the [settings documentation](settings.md).

- [Rest API](#rest-api)
  - [API ref](#api-ref)
  - [Get Kalliope's version](#get-kalliopes-version)
  - [Brain](#brain)
    - [List synapses](#list-synapses)
    - [Show synapse details](#show-synapse-details)
    - [Run a synapse by its name](#run-a-synapse-by-its-name)
    - [Run a synapse from an order](#run-a-synapse-from-an-order)
    - [Run a synapse from an audio file](#run-a-synapse-from-an-audio-file)
  - [The neurotransmitter case](#the-neurotransmitter-case)
  - [Settings](#settings)
    - [Get current settings](#get-current-settings)
    - [Deaf](#deaf)
      - [Get deaf status](#get-deaf-status)
      - [Switch deaf status](#switch-deaf-status)
    - [Mute](#mute)
      - [Get mute status](#get-mute-status)
      - [Set mute status](#set-mute-status)
    - [energy_threshold](#energy-threshold)
      - [Get energy_threshold status](#get-energy-threshold-status)
      - [Set energy_threshold status](#set-energy-threshold-status)
    - [Variables](#variables)
      - [Get variables list](#get-variables-list)
      - [Update Variables](#update-variables)
    - [default tts, stt, player, trigger](#default-tts--stt--player--trigger)
      - [Get](#get)
      - [Update](#update)

## API ref

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
| GET    | /settings/hooks                   | Get the current hooks              |
| POST   | /settings/hooks                   | Update the hooks list              |
| GET    | /settings/variables               | Get the variables list             |
| POST   | /settings/variables               | Update the variables list          |
| GET    | /settings/default_tts             | Get current tts                    |
| POST   | /settings/default_tts             | Update current tts                 |
| GET    | /settings/default_stt             | Get current stt                    |
| POST   | /settings/default_stt             | Update current stt                 |
| GET    | /settings/default_player          | Get the current player             |
| POST   | /settings/default_player          | Update current player              |
| GET    | /settings/default_trigger         | Get the current trigger            |
| POST   | /settings/default_trigger         | Update the current trigger         |

>**Note:** --user is only needed if `password_protected` is True

## Get Kalliope's version

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

## Brain

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
```JSON
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

## The neurotransmitter case

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

## Settings

### Get current settings

Normal response codes: 200
Error response codes: unauthorized(401), Bad request(400)

Curl command:
```bash
curl -i --user admin:secret  -X GET  http://127.0.0.1:5000/settings
```

Output example:
```JSON
{
  "settings": {
    "cache_path": "/tmp/kalliope_tts_cache", 
    "default_player_name": "mplayer", 
    "default_stt_name": "google", 
    "default_trigger_name": "snowboy", 
    "default_tts_name": "pico2wave", 
    "hooks": {
      "on_deaf": null, 
      "on_mute": null, 
      "on_order_found": null, 
      "on_order_not_found": "order-not-found-synapse", 
      "on_processed_synapses": null, 
      "on_start": "on-start-synapse", 
      "on_start_listening": null, 
      "on_start_speaking": null, 
      "on_stop_listening": null, 
      "on_stop_speaking": null, 
      "on_stt_error": null, 
      "on_triggered": "on-triggered-synapse", 
      "on_undeaf": null, 
      "on_unmute": null, 
      "on_waiting_for_trigger": null
    }, 
    "kalliope_version": "0.5.1b", 
    "machine": "x86_64", 
    "options": {
      "adjust_for_ambient_noise_second": 0, 
      "deaf": false, 
      "energy_threshold": 4000, 
      "mute": false, 
      "name": "Options", 
      "stt_timeout": 0
    }, 
    "players": [
      {
        "name": "mplayer", 
        "parameters": {}
      }, 
      {
        "name": "pyalsaaudio", 
        "parameters": {
          "convert_to_wav": true, 
          "device": "default"
        }
      }, 
      {
        "name": "pyaudioplayer", 
        "parameters": {
          "convert_to_wav": true
        }
      }, 
      {
        "name": "sounddeviceplayer", 
        "parameters": {
          "convert_to_wav": true
        }
      }
    ], 
    "resources": {
      "neuron_folder": null, 
      "signal_folder": null, 
      "stt_folder": null, 
      "trigger_folder": null, 
      "tts_folder": null
    }, 
    "rest_api": {
      "active": true, 
      "allowed_cors_origin": false, 
      "login": "admin", 
      "password": "secret", 
      "password_protected": true, 
      "port": 5000
    }, 
    "stts": [
      {
        "name": "google", 
        "parameters": {
          "language": "fr-FR"
        }
      }, 
      {
        "name": "wit", 
        "parameters": {
          "key": "fakekey"
        }
      }, 
      {
        "name": "bing", 
        "parameters": {
          "key": "fakekey"
        }
      }, 
      {
        "name": "apiai", 
        "parameters": {
          "key": "fakekey", 
          "language": "fr"
        }
      }, 
      {
        "name": "houndify", 
        "parameters": {
          "client_id": "fakeclientid", 
          "key": "fakekey"
        }
      }
    ], 
    "triggers": [
      {
        "name": "snowboy", 
        "parameters": {
          "pmdl_file": "trigger/snowboy/resources/kalliope-FR-40samples.pmdl"
        }
      }
    ], 
    "ttss": [
      {
        "name": "pico2wave", 
        "parameters": {
          "cache": true, 
          "language": "fr-FR"
        }
      }, 
      {
        "name": "googletts", 
        "parameters": {
          "cache": true, 
          "language": "fr"
        }
      }, 
      {
        "name": "voicerss", 
        "parameters": {
          "cache": true, 
          "key": "API_Key", 
          "language": "fr-fr"
        }
      }, 
      {
        "name": "watson", 
        "parameters": {
          "password": "password", 
          "username": "me", 
          "voice": "fr-FR_ReneeVoice"
        }
      }
    ], 
    "variables": {}
  }
}
```

### Deaf

#### Get deaf status

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

#### Switch deaf status
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

### Mute

When you use the API, by default Kalliope will generate a text and process it into the TTS engine.
Some calls to the API can be done with a flag that will tell Kalliope to only return the generated text without processing it into the audio player.
When `mute` is switched to true, Kalliope will not speak out loud on the server side.

#### Get mute status

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

#### Set mute status

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

### energy_threshold

Define the [energy_threshold](settings.md) in the settigns 

#### Get energy_threshold status

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

#### Set energy_threshold status

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


### Variables

#### Get variables list 

Normal response codes: 200
Error response codes : unauthorized(401), Bad request(400)


Curl command:
```bash
curl -i --user admin:secret  -X GET  http://127.0.0.1:5000/settings/variables
```

Output example:
```JSON
{
  "variables": {
    "my_variable": "blabla", 
    "nickname": "monf"
  }
}
```

#### Update Variables

Normal response codes: 200
Error response codes : unauthorized(401), Bad request(400)


Curl command:
```bash
curl -i -H "Content-Type: application/json" --user admin:secret  -X POST -d '{"mySecondVariable": "SecondValue", "Nickname2": "Nico"}' http://127.0.0.1:5000/settings/variables
```

Output example:
```JSON
{
  "variables": {
    "my_variable ": "blabla", 
    "nickname": "monf",
    "mysecondVariable": "SecondValue",
    "Nickname2": "Nico"
  }
}
```



### default tts, stt, player, trigger

#### Get 

Normal response codes: 200
Error response codes : unauthorized(401), Bad request(400)


Curl command:
```bash
curl -i --user admin:secret  -X GET  http://127.0.0.1:5000/settings/default_tts
curl -i --user admin:secret  -X GET  http://127.0.0.1:5000/settings/default_stt
curl -i --user admin:secret  -X GET  http://127.0.0.1:5000/settings/default_player
curl -i --user admin:secret  -X GET  http://127.0.0.1:5000/settings/default_trigger
```

Output example:
```JSON
{
  "default_tts": "pico2wave"
}
```


#### Update

Normal response codes: 200
Error response codes : unauthorized(401), Bad request(400)

/!\ Note: To update a tts, stt, player, trigger it should be properly defined in the 'settings.yml' in the corresponding list.

Curl command:
```bash
curl -i -H "Content-Type: application/json" --user admin:secret  -X POST -d '{"default_tts": "pico2wave"}' http://127.0.0.1:5000/settings/default_tts
```

Output example:
```JSON
{
  "default_tts": "googletts"
}
```
