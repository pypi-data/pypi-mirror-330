"""Phrase Chunking Pytest Unit Test"""

# Copyright 2024 Centre for Text Technology, North-West University.
# All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

__authors__ = 'askruger'

from ctextcore.core import CCore as core
from pathlib import Path
import json
import logging
import os
import pytest

LOGGER = logging.getLogger(__name__)
server = core()

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE_NAME = ".input.test.txt"
INPUT_DIR = CURRENT_DIR+"/data/input/"
EXPECTED_OUTPUT_FILE_NAME = ".pc.output.expected."

test_params = []
technologies = server.list_available_techs()
languages = ["af", "nso", "nr", "ss", "st", "tn", "ts", "ve", "xh", "zu"]
levels = ["line","file"]
formats = ["json", "list", "delimited"]

LOGGER.info("Testing Phrase Chunking for the followig languages: {0}".format(languages))

def download_pc_model(lang, server, retry_count=1):
    """
    Downloads PC model if not available, with retries.
    """
    for attempt_count in range(retry_count + 1):
        # Get updated list of available technologies 
        technologies = server.list_available_techs()
        print(technologies)
        if lang in technologies.get("pc", []):
            print(f"PC model for language {lang} is already available.")
            return
        print(f"{'Attempting' if attempt_count == 0 else 'Retrying'} download of PC model for language: {lang}, Attempt {attempt_count+1}")
        try:
            server.download_model(language=lang, tech="pc")
            print("Download successful.")
            return
        except Exception as e:
            print(f"Error occurred: {e}")
            if attempt_count == retry_count:
                print("Max retry attempts reached. Download failed.")

for lang in languages:
    download_pc_model(lang, server, retry_count=1)
    if lang not in technologies["pc"]:
        server.download_model(language=lang, tech="pc")
    for level in levels:
        EXPECTED_OUTPUT_DIR = CURRENT_DIR+"/data/expected/{0}_level/pc/".format(level)  # Check
        for output_format in formats:
            if output_format=="json":
                OUTPUT_FILENAME = str(lang+EXPECTED_OUTPUT_FILE_NAME+output_format+".json")
            else:
                OUTPUT_FILENAME = str(lang+EXPECTED_OUTPUT_FILE_NAME+output_format+".txt")
            if level=="line":
                with open(Path(INPUT_DIR,str(lang+INPUT_FILE_NAME)), 'r', encoding='UTF-8') as input_file:
                    input_file_all_lines = ''.join(input_file.readlines())
                # process_text returns JSON object if you choose JSON as output (JSON is default)
                server_output = server.process_text(text_input=input_file_all_lines, tech="pc", language=lang, output_format=output_format)
            elif level=="file":
                server_output = server.process_text(text_input=Path(INPUT_DIR,str(lang+INPUT_FILE_NAME)), tech="pc", language=lang,output_format=output_format)
            with open(Path(EXPECTED_OUTPUT_DIR, OUTPUT_FILENAME), 'r', encoding='UTF-8') as expected_file:
                if output_format=="json":
                    expected_output= json.load(expected_file)
                    server_output_str = server_output
                else:
                    expected_output= ''.join(expected_file.readlines())
                    server_output_str = str(server_output)
            test_params.append(tuple((lang,server_output_str,expected_output)))

@pytest.mark.parametrize("lang,test_input,expected", test_params)
def test_process_string(lang,test_input, expected):
    """Phrase Chunking test_process_string function"""
    assert test_input == expected,"PC failed for {0}".format(lang)