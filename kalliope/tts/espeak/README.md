# eSpeak

## Synopsis

This TTS is based on the eSpeak engine

## Installation

    kalliope install --git-url "https://github.com/Ultchad/kalliope-espeak.git"

## Options

| Parameters | Required | Default         | Choices                | Comment                                                                                       |
|------------|----------|-----------------|------------------------|-----------------------------------------------------------|
| voice      | yes      |                 | all voice installed    | see the full list with command "espeak --voices=LANGUAGE" |
| variant    | no       |                 | all language installed | see the full list with command "espeak --voices=variant"  |
| speed      | no       | 160             | 80 to 450              | Speed in words per minute                                 |
| amplitude  | no       | 100             | 0 to 200               | Amplitude                                                 |
| pitch      | no       | 50              | 0 to 99                | Pitch adjustment                                          |
| path       | no       | /usr/bin/espeak | 0 to 99                | Path of espeak                                            |
| cache      | no       | TRUE            |                        | True if you want to use the cache with this TTS           | 

## Notes :

To see the full list of language and voices:

    espeak --voices

To see the full list of voices:

    espeak --voices=LANGUAGE
    
    # exemple:
    
    espeak --voices=fr
    Pty Language Age/Gender VoiceName          File          Other Languages
     5  fr-fr          M  french               fr            (fr 5)
     7  fr             M  french-mbrola-1      mb/mb-fr1
     7  fr             F  french-mbrola-4      mb/mb-fr4
     5  fr-be          M  french-Belgium       europe/fr-be  (fr 8)
     
     # Configuration for "7  fr             M  french-mbrola-1      mb/mb-fr1"
     voice: "mb-fr1"

To see the full list of variant:

    espeak --voices=variant
    
    # exemple:
    
    espeak --voices=variant
    Pty Language Age/Gender VoiceName          File          Other Languages
     5  variant        F  female2              !v/f2
     5  variant        F  female3              !v/f3
     5  variant        F  female4              !v/f4
     5  variant        F  female5              !v/f5
     5  variant        F  female_whisper       !v/whisperf
     5  variant        -  klatt                !v/klatt
     5  variant        -  klatt2               !v/klatt2
     [...]
     
     # Configuration for "5  variant        F  female3              !v/f3"
     # chose your language voice
     voice: "fr"
     variant: "f3"
