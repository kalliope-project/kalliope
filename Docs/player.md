# Players                                                                                                                                         # Players

The player is the library/software used to make Kalliope talk.
With Kalliope project, you can set whatever sound player you want to use.

## Settings

Define the player you want to use by default in the [setting.yml](settings.md) file.
```yml
default_player: "player_name"
```

E.g
```yml
default_player: "mplayer"
```

Then, still in the [setting.yml](settings.md) file, each player must set up its configuration following the 'players' tag :
```yml
players:
   - player1:
      player1parameter1: "value option1"
      player1parameter2: "value option2"
   - player2:
      player2parameter1: "value option1"
```

E.g
```yml
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

>**Note:** Sometime, parameters will be necessary to use an engine. 
Click on a Player engine link in the `Current CORE Available Players` section to know which parameter are required.

>**Note:** A player which does not ask for input parameters need to be declared as an empty dict. E.g: ```- player_name: {}```

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