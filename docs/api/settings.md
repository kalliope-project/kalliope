# Kalliope API: Settings

| Method | URL                                                 | Action                                              |
|--------|-----------------------------------------------------|-----------------------------------------------------|
| GET    | /settings/deaf                                      | Get the current deaf status                         |
| POST   | /settings/deaf                                      | Switch the deaf status                              |
| GET    | /settings/mute                                      | Get the current mute status                         |
| POST   | /settings/mute                                      | Switch the mute status                              |
| GET    | /settings/recognizer_multiplier                     | Get the current recognizer_multiplier               |
| POST   | /settings/recognizer_multiplier                     | Update the recognizer_multiplier value              |
| GET    | /settings/recognizer_energy_ratio                   | Get the recognizer_energy_ratio                     |
| POST   | /settings/recognizer_energy_ratio                   | Update the recognizer_energy_ratio                  |
| GET    | /settings/recognizer_recording_timeout              | Get the current recognizer_recording_timeout        |
| POST   | /settings/recognizer_recording_timeout              | Update the recognizer_recording_timeout value       |
| GET    | /settings/recognizer_recording_timeout_with_silence | Get the recognizer_recording_timeout_with_silence   |
| POST   | /settings/recognizer_recording_timeout_with_silence | Update the recognizer_recording_timeout_with_silence|
| GET    | /settings/hooks                                     | Get the current hooks                               |
| POST   | /settings/hooks                                     | Update the hooks list                               |
| GET    | /settings/variables                                 | Get the variables list                              |
| POST   | /settings/variables                                 | Update the variables list                           |
| GET    | /settings/default_tts                               | Get current tts                                     |
| POST   | /settings/default_tts                               | Update current tts                                  |
| GET    | /settings/default_stt                               | Get current stt                                     |
| POST   | /settings/default_stt                               | Update current stt                                  |
| GET    | /settings/default_player                            | Get the current player                              |
| POST   | /settings/default_player                            | Update current player                               |
| GET    | /settings/default_trigger                           | Get the current trigger                             |
| POST   | /settings/default_trigger                           | Update the current trigger                          |

>**Note:** --user is only needed if `password_protected` is True

## Get current settings

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

## Deaf

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

## Mute

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

## recognizer_multiplier

Define the [recognizer_multiplier](settings/settings.md#recognizer_multiplier) in the settings.

### Get recognizer_multiplier status

Normal response codes: 200
Error response codes : unauthorized(401), Bad request(400)


Curl command:
```bash
curl -i --user admin:secret  -X GET  http://127.0.0.1:5000/settings/recognizer_multiplier
```

Output example:
```JSON
{
  "recognizer_multiplier": 4000
}
```

### Set recognizer_multiplier status

Normal response codes: 200
Error response codes : unauthorized(401), Bad request(400)


Curl command:
```bash
curl -i -H "Content-Type: application/json" --user admin:secret  -X POST -d '{"recognizer_multiplier": 1.0}' http://127.0.0.1:5000/settings/recognizer_multiplier
```

Output example:
```JSON
{
  "recognizer_multiplier": 1.0
}
```

## recognizer_energy_ratio

Define the [recognizer_energy_ratio](settings/settings.md#recognizer_energy_ratio) in the settings.

### Get recognizer_energy_ratio status

Normal response codes: 200
Error response codes : unauthorized(401), Bad request(400)


Curl command:
```bash
curl -i --user admin:secret  -X GET  http://127.0.0.1:5000/settings/recognizer_energy_ratio
```

Output example:
```JSON
{
  "recognizer_energy_ratio": 1.5
}
```

### Set recognizer_energy_ratio status

Normal response codes: 200
Error response codes : unauthorized(401), Bad request(400)


Curl command:
```bash
curl -i -H "Content-Type: application/json" --user admin:secret  -X POST -d '{"recognizer_energy_ratio": 1.5}' http://127.0.0.1:5000/settings/recognizer_energy_ratio
```

Output example:
```JSON
{
  "recognizer_energy_ratio": 1.5
}
```

## recognizer_recording_timeout

Define the [recognizer_recording_timeout](settings/settings.md#recognizer_recording_timeout) in the settings.

### Get recognizer_recording_timeout status

Normal response codes: 200
Error response codes : unauthorized(401), Bad request(400)


Curl command:
```bash
curl -i --user admin:secret  -X GET  http://127.0.0.1:5000/settings/recognizer_recording_timeout
```

Output example:
```JSON
{
  "recognizer_recording_timeout": 15.0
}
```

### Set recognizer_recording_timeout status

Normal response codes: 200
Error response codes : unauthorized(401), Bad request(400)


Curl command:
```bash
curl -i -H "Content-Type: application/json" --user admin:secret  -X POST -d '{"recognizer_recording_timeout": 15.0}' http://127.0.0.1:5000/settings/recognizer_recording_timeout
```

Output example:
```JSON
{
  "recognizer_recording_timeout": 15.0
}
```

## recognizer_recording_timeout_with_silence

Define the [recognizer_recording_timeout_with_silence](settings/settings.md#recognizer_recording_timeout_with_silence) in the settings.

### Get recognizer_recording_timeout_with_silence status

Normal response codes: 200
Error response codes : unauthorized(401), Bad request(400)


Curl command:
```bash
curl -i --user admin:secret  -X GET  http://127.0.0.1:5000/settings/recognizer_recording_timeout_with_silence
```

Output example:
```JSON
{
  "recognizer_recording_timeout_with_silence": 3.0
}
```

### Set recognizer_recording_timeout_with_silence status

Normal response codes: 200
Error response codes : unauthorized(401), Bad request(400)


Curl command:
```bash
curl -i -H "Content-Type: application/json" --user admin:secret  -X POST -d '{"recognizer_recording_timeout_with_silence": 3.0}' http://127.0.0.1:5000/settings/recognizer_recording_timeout_with_silence
```

Output example:
```JSON
{
  "recognizer_recording_timeout_with_silence": 3.0
}
```

## Variables

### Get variables list

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

### Update Variables

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



## default tts, stt, player, trigger

### Get

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

### Update

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
