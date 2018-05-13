# MaryTTS

## Synopsis

MaryTTS is an open-source, multilingual Text-to-Speech Synthesis platform written in Java.

## Options

| Parameters | Required | Default  | Choices                           | Comment                                               |
|------------|----------|----------|-----------------------------------|-------------------------------------------------------|
| voice      | yes      | None     | e.g. bits1, cmu-bdl, enst-camille | Run ./marytts list to check your installed voices     |
| locale     | yes      | None     | e.g. de, en_US, fr                | Check http://localhost:59125/locales for installed locales| 
| host       | no       | localhost|                                   | Host address of your MaryTTS server                   |
| port       | no       | 59125    |                                   | Port of your MaryTTS server                           |

## Example on how to setup MaryTTS in Kalliope :

For english voice on localhost add the following lines in your settings.yml:
```
text_to_speech:
  - marytts:
      voice: "cmu-bdl"
      locale: "en_US"
      cache: True 
```
For english voice on remote host with default port:
```
text_to_speech:
  - marytts:
      voice: "cmu-bdl"
      locale: "en_US"
      host: 192.168.0.25
      cache: True
```      
## Notes :

You need to install Marytts server.  
https://github.com/marytts/marytts-installer
