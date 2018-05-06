v0.5.1 / 2018-05-07
===================
- Fix: I/O error on Python 3
- Fix: Snowboy build for Python 3
- Fix: fix kill_switch core neuron
- Fix: error with Jinja lib when installing
- Fix: 'device unavailable' exception should now be handled properly
- Fix: API call when kalliope is processing
- Enhancement: rename 'mute' to 'deaf' in setting and neuron
- Enhancement: create en 'option' setting. Deaf and mute are now placed in this setting
- Enhancement: add mute / unmute hook
- Enhancement: add 'on_stt_error' hook
- Enhancement: add on_processed_synapses hook
- Enhancement: Snowboy lib updated to v1.3.0
- Enhancement: remove shell gui feature
- Enhancement: add Ubuntu 18.04 support
- Feature: Neuron 'settings'
- Feature: Neuron 'brain'
- Feature: Neuron 'signals'
- Feature: stt correction
- Feature: STT timeout
- Feature: Mute (old no_voice flag). Make Kalliope processing neurons without speaking out loud
- Feature: order signal can now skip the trigger to chain orders without waking Kalliope. See 'Signal' neuron

v0.5.0 / 2018-01-13
===================
- Fix: recognition option in settings
- Fix: no_voice flag in neurotransmitter neuron no longer lost
- Fix: retrieve parameters when user order contains non matching words
- Fix: Update Voicerss TTS
- Fix: Usage of double brackets with json sentence
- Fix: Remove acapela TTS
- Feature: Kalliope can be started muted
- Feature: add geolocation signals
- Feature: add Watson TTS
- Feature: Hook. WARNING: This is a breaking change. Settings must be updated
- Feature: add normal, strict and ordered-strict order

v0.4.6 / 2017-10-03
===================
- add core neuron: neurotimer
- add core neuron: mqtt
- add core signal: mqtt
- new feature: community signal now supported
- dict can be used in global variables
- bug fix: python 3 execution with snowboy lib
- new feature: kalliope memory
- add espeak tts to core
- add stt options. manual or dynamic threshold
- Fix: neurotransmitter bracket in answer

v0.4.5 / 2017-07-23
===================
- add keyword_entries attribute to CMU Sphinx
- add simplerate attribute to Pico2wav TTS
- API: convert mp3 file to wav automatically
- add sensitivity attribute to snowboy trigger
- add grammar attribute to CMU Sphinx
- add no_voice flag to api
- add possibility to send parameters when using api with run synapse by name

v0.4.4 / 2017-05-20
===================
- Fix: Uppercase in order/parameters/global variables are now handled correctly
- Fix: usage of integer in neuron parameters
- Fix: encoding with special character
- Refactor main controller. Use a LIFO to allow full usage of kalliope via API (even with neurotransmitter)
- Add a systemd script to start kalliope automatically
- docker testing
- python 3 support 3.4, 3.5, 3.6
- Increase testing code coverage
- Fix: Raspberry performance. CPU usage from 120% to 15%
- Input value refactoring. "args" parameter replaced by jinja templating
- Review TTS overriding config in neuron declaration
- Fix: accapela TTS
- LED and mute button support for Raspberry Pi
- Player modularity

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
