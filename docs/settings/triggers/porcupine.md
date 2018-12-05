## Parameters

| parameter    | required | type    | default | choices         | comment                                                                                          |
|--------------|----------|---------|---------|-----------------|--------------------------------------------------------------------------------------------------|
| keyword      | TRUE     | string  |         |                 | Path to the porcupine wake word. The path can be absolute or relative to the brain file          |
| sensitivity  | FALSE    | string  | 0.5     | between 0 and 1 | Increasing the sensitivity value lead to better detection rate, but also higher false alarm rate |
| input_device | FALSE    | integer | default | 				| Select the input device, otherwise the default device will be used        		               |
| tiny_keyword | FALSE 	  | string	| false   | true/false      | If true you can use tiny keywords, these accuracy is slightly lower than the standard model but it consumes considerably less resources |

## Example settings

This is the trigger engine that will catch your magic work to wake up Kalliope. With porcupine we need different keywords for different platforms. The example use the keyword "porcupine" for the raspberry.

```yaml
default_trigger: "porcupine"

# Trigger engine configuration
triggers:
  - porcupine:
      keyword: "trigger/porcupine/porcupine_raspberrypi.ppn"
```
To use multiple keywords with different sensitivities
```yaml
default_trigger: "porcupine"

# Trigger engine configuration
triggers:
  - porcupine:
      keyword:
        - "trigger/porcupine/porcupine_raspberrypi.ppn"
        - "trigger/porcupine/blueberry_raspberrypi.ppn"
      sensitivity:
      	- 0.35
      	- 0.4
```

## Available Porcupine keywords

You can find existing keywords for the raspberry and linux [here](https://github.com/Picovoice/Porcupine/tree/master/resources/keyword_files). 
To create your own wake word you have to use the [optimizer from the porcupine repository](https://github.com/Picovoice/Porcupine/tree/master/tools/optimizer). You can only create keywords for Linux, Mac and Windows unfortunately we cannot create keywords for the raspberry. 

If you use Kalliope on a x86_64 machine with Linux and want to create your own wake word you can do it with the following commands: 

```yaml
git clone https://github.com/Picovoice/Porcupine.git
cd Porcupine
tools/optimizer/linux/x86_64/pv_porcupine_optimizer -r resources -w "Kalliope" -p linux -o ~/
```

The keyword Kalliope will be saved in your home directory.

## Note 

Keywords created by the optimizer tool will expire after 90 days.