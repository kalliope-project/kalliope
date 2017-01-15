# dna.yml file

The dna file is the descriptor of your module.
This file has a yaml syntax and must be present to allow Kalliope to install it from the [CLI](../kalliope_cli.md).

## DNA parameters

| parameter                  | type   | required | default | choices          | comment                                                                                                                               |
|----------------------------|--------|----------|---------|------------------|---------------------------------------------------------------------------------------------------------------------------------------|
| name                       | string | yes      |         |                  | Lowercase. It will be the name of the folder installed in ressources_dir for the target type of resource                              |
| type                       | string | yes      |         | neuron, stt, tts | The type of resource. This will be used by Kalliope install process to place the resource in the right directory set in resources_dir |
| author                     | string | no       |         |                  | String that contain info about the author of the modul like a name or a github profile page                                           |
| kalliope_supported_version | list   | yes      |         | 0.4              | list of kalliope __MAJOR__ version the module support. E.g `- 0.4`                                                                    |
| tags                       | list   | no       |         |                  | list of tags that can help to categorize the module. E.g: "email", "social network", "search engine"                                  |

## DNA file examples

A dna file for a neuron
```yml
name: "wikipedia_searcher"
type: "neuron"
author: "The dream team of Kalliope project"

kalliope_supported_version:
  - 0.4

tags:
  - "search engine"
  - "wiki"
```
