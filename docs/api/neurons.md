# Kalliope API: Neurons

| Method | URL              | Action                        |
| :----- | :--------------- | :---------------------------- |
| GET    | /neurons         | Get list of installed neurons |
| GET    | /neurons/install | Install a community neuron    |

## List installed neurons

Normal response codes: 200
Error response codes: unauthorized(401)
Curl command:

```bash
curl -i \
--user admin:secret \
-X GET \
http://localhost:5000/neurons
```

Output example:

```JSON
{
  "community": [
    "gmail_checker",
    "wikipedia_searcher"
  ],
  "core": [
    "script",
    "brain",
    "systemdate",
    "neurotimer",
    "uri",
    "say",
    "sleep",
    "ansible_playbook",
    "neurotransmitter",
    "settings",
    "signals",
    "shell",
    "debug",
    "mqtt_publisher",
    "kalliope_version",
    "kill_switch"
  ]
}
```

## Install a neuron

```bash
curl -i -H "Content-Type: application/json" \
--user admin:secret \
-X POST \
-d '
{
    "git_url": "https://github.com/kalliope-project/kalliope_neuron_wikipedia.git",
    "sudo_password": "raspberry"
}
' \
http://127.0.0.1:5000/neurons/install
```

Output example:

```JSON
{
  "author": "The dream team of Kalliope project",
  "kalliope_supported_version": [
    0.4,
    0.5
  ],
  "name": "wikipedia_searcher",
  "tags": [
    "wikipedia",
    "search engine",
    "wiki"
  ],
  "type": "neuron"
}
```
