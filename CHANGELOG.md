v0.4.3 / 2017-03-11
===================
- Update Documentation
- Improve API + manage incoming audio
- Fix bug maximum recursion
- Disable REST API by default 
- Add command line run-order to start a synapse
- Run default synapse if STT engine do not return an order
- Manage global variables
- Remove password from log
- cli command to delete a neuron
- Fix neurotransmitter
- Fix Acapela TTS
- Remove Voxygen TTS (not working anymore)

v0.4.2 / 2017-01-18
===================
- fix community neuron installation

v0.4.1 / 2017-01-15
===================
- add CORS support for REST API
- fix installation of community STT and TTS
- add feature: sound/sentence when Kalliope is ready
- fix Raspbian install
- add offline STT (CMUSphinx)
- orders are not anymore case sensitive
- add STT utils class to split the audio catching from the processing
- fix CTRL-C to kill Kalliope

v0.4.0 / 2016-12-28
===================
- Add resources directory (neuron, stt, tts, (trigger))
- Install community modules from git url
- Fix API (strict slashes + included brains)
- starter kits (FR - EN)
- Add support Ubuntu 14.04
- Fix neurotransmitter (multiple synapses call)
- Neurotransmitter improvements (pass arguments to called synapse)
- Split Core Neurons and Community Neurons
- update some pip dependencies
- Add Russian snowboy model for каллиопа 

v0.3.0 / 2016-12-7
=================
- add unit tests for core & neurons
- add CI (Travis)
- refactor Event manager
- support installation with setup.py
- support pip installation
- fix ansible_playbook neuron
- add rss_reader neuron
- review settings and brain file loading
- add default neuron used if Kalliope does not match the spelt order

v0.2 / 2016-11-21
=================

- add neuron URI to call web services
- fix wikipedia neuron. renamed wikipedia_searcher
- update neuron neurotransmitter: can now call another synapse directly without asking a question


v0.1 / 2016-11-02
=================

- Initial Release
