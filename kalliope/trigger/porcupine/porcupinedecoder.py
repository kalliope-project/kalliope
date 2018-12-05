#
# Copyright 2018 Picovoice Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import os
import struct
from threading import Thread
import pyaudio
import logging

from kalliope.core.ConfigurationManager import SettingLoader
from kalliope.trigger.porcupine.porcupine_binding import Porcupine
from kalliope import Utils

logging.basicConfig()
logger = logging.getLogger("kalliope")
TOP_DIR = os.path.dirname(os.path.abspath(__file__))
RESOURCE_FILE = os.path.join(TOP_DIR, "lib")

class HotwordDetector(Thread):
    def __init__(
            self,
            keyword_file_paths,
            sensitivities,
            input_device_index,
            tiny,
            detected_callback=None
            ):

        """
        Constructor.
        :param keyword_file_paths: List of absolute paths to keyword files.
        :param sensitivities: Sensitivity parameter for each wake word. For more information refer to
        'include/pv_porcupine.h'. It uses the
        same sensitivity value for all keywords.
        :param input_device_index: Optional argument. If provided, audio is recorded from this input device. Otherwise,
        the default audio input device is used.
        """

        super(HotwordDetector, self).__init__()
        sl = SettingLoader()
        settings = sl.settings
        
        # For the raspberry there are 3 different types of libpv_porcupine.so provided, 
        # we use cortex-a53, tested on rpi 2 and 3.
        self._library_path = RESOURCE_FILE + "/%s/libpv_porcupine.so" % (settings.machine)
        if not tiny:
            self._model_file_path = RESOURCE_FILE + "/common/porcupine_params.pv"
        else:
            self._model_file_path = RESOURCE_FILE + "/common/porcupine_tiny_params.pv"
        
        self._input_device_index = input_device_index
        self.kill_received = False
        self.paused = False
        self.detected_callback = detected_callback

        keyword_file_paths = [x.strip() for x in keyword_file_paths.split(',')]
        if isinstance(sensitivities, float):
            sensitivities = [sensitivities] * len(keyword_file_paths)
        else:
            sensitivities = [float(x) for x in sensitivities.split(',')]

        self._keyword_file_paths = keyword_file_paths
        self._sensitivities = sensitivities

    def run(self):
        """
         Creates an input audio stream, initializes wake word detection (Porcupine) object, and monitors the audio
         stream for occurrences of the wake word(s).
         """

        num_keywords = len(self._keyword_file_paths)

        keyword_names =\
            [os.path.basename(x).replace('.ppn', '').replace('_tiny', '').split('_')[0] for x in self._keyword_file_paths]
        
        for keyword_name, sensitivity in zip(keyword_names, self._sensitivities):
            logger.debug('Listening for %s with sensitivity of %s' % (keyword_name, sensitivity))
        
        self.porcupine = Porcupine(
            library_path=self._library_path,
            model_file_path=self._model_file_path,
            keyword_file_paths=self._keyword_file_paths,
            sensitivities=self._sensitivities)

        self.pa = pyaudio.PyAudio()
        self.audio_stream = self.pa.open(
            rate=self.porcupine.sample_rate,
            channels=1,
            format=pyaudio.paInt16,
            input=True,
            frames_per_buffer=self.porcupine.frame_length,
            input_device_index=self._input_device_index)
                
        logger.debug("[Porcupine] detecting...")

        while not self.kill_received:
            if not self.paused:
                callback = None
                pcm = self.audio_stream.read(self.porcupine.frame_length)
                pcm = struct.unpack_from("h" * self.porcupine.frame_length, pcm)
                result = self.porcupine.process(pcm)
                
                if num_keywords == 1 and result:
                    message = "Keyword " + str(keyword_names[0]) + " detected"
                    callback = self.detected_callback
                    
                elif num_keywords > 1 and result >= 0:
                    message = "Keyword " + str(keyword_names[result]) + " detected"
                    callback = self.detected_callback

                if callback is not None:
                    logger.debug(message)
                    Utils.print_info(message)
                    callback()
                    logger.debug("[Porcupine] detect voice break")
                    break

    def terminate(self):
        """
        Terminate audio stream. Users cannot call start() again to detect.
        :return: None
        """
        if self.porcupine is not None:
                self.porcupine.delete()
        
        if self.audio_stream is not None:
            self.audio_stream.close()

        if self.pa is not None:
            self.pa.terminate()
        logger.debug("[Porcupine] Audio stream cleaned.")
