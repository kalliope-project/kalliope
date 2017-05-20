# Players

With Kalliope project, you can set whatever Sound Player you want to use.

## Settings

The setting.yml defines the Player you want to use by default
```yml
default_player: "type default player here"
```

Then, still in the settings.yml file, each Player must set up its configuration following the 'players' tag :
```yml
players:
   - player1:
      player1parameter1: "value option1"
      player1parameter2: "value option2"
   - player2:
      player2parameter1: "value option1"
```
Sometime, parameters will be necessary to use an engine. 
Click on a Player engine link in the `Current CORE Available Players` section to know which parameter are required.

## Current CORE Available Players

Core players are already packaged with the installation of Kalliope an can be used out of the box. See the [complete list here](player_list.md).

## Full Example

In the settings.yml file :

```yml
default_player: "mplayer"

players:
  - mplayer: {}
  - pyalsaaudio:
     device: "default"
     convert_to_wav: True
  - pyaudioplayer:
     convert_to_wav: True
  - sounddeviceplayer:
     convert_to_wav: True
```