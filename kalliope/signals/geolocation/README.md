# Geolocalisation

## Synopsis

**Geolocation** is a way to launch a synapse when ENTERING a geolocated zone.

As Kalliope does not manage its own geolocation, this signal has been designed in view to be implemented from external clients (smartphones, watches, embedded devices, etc).

The syntax of a geolocation declaration in a synapse is the following.
```yml
signals:
    - geolocation:
          latitude: "46.204391"
          longitude: "6.143158"
          radius: "10000"
```

For example, if we want Kalliope to run the synapse when entering in Geneva
```yml
- geolocation:
      latitude: "46.204391"
      longitude: "6.143158"
      radius: "1000"
```

## Options

Parameters are keyword you can use to build your geolocation

List of available parameter:

| parameter   | required | default | choices                                                         | comment   |
|-------------|----------|---------|-----------------------------------------------------------------|-----------|
| latitude    | yes      |         | 46.204391                                                         | E.g: 2016 |
| longitude   | yes      |         | 6.143158                                                    |           |
| radius      | yes      |         | 1 (meters)                                               |           |

## Synapses example

### Web clock radio

Let's make a complete example. 
We want to Kalliope to :
- welcome when coming back home
- Play our favourite web radio

The synapse in the brain would be:
```yml
  - name: "geolocation-welcome-radio"
    signals:
      - geolocation:
            latitude: "46.204391"
            longitude: "6.143158"
            radius: "10"
    neurons:
      - say:
          message:
            - "Welcome Home!"
      - shell: 
          cmd: "mplayer http://192.99.17.12:6410/"
          async: True
```

After setting up a geolocation signal, you must restart Kalliope
```bash
python kalliope.py start
```

If the syntax is NOT ok, Kalliope will raise an error and log a message:
```
[Geolocation] The signal is missing mandatory parameters, check documentation
```

### Note

/!\ this feature is supported by the [Kalliope official smartphone application.](https://github.com/kalliope-project/kalliope-app)