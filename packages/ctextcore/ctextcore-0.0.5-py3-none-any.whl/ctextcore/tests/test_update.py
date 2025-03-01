"""Model Version Update Pytest Unit Test"""

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

import json
import os
import logging
import pytest

LOGGER = logging.getLogger(__name__)

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE_NAME_ORIGINAL_DIR = os.path.abspath(os.path.join(CURRENT_DIR, "..", "core", "models"))
INPUT_FILE_NAME_ORIGINAL = INPUT_FILE_NAME_ORIGINAL_DIR + "/installed_versions.json"
INPUT_FILE_NAME_UPDATES = CURRENT_DIR + "/data/installed_versions_updates.json"
# lang, tech
test_params = []

# Download models wat in installed version update json sit.

LOGGER.info("Testing model version updates")

with open(INPUT_FILE_NAME_ORIGINAL, 'r', encoding='UTF-8') as file_installed_versions:
    installed_versions_data = json.load(file_installed_versions)
with open(INPUT_FILE_NAME_UPDATES, 'r', encoding='UTF-8') as file_installed_updates:
    installed_updates_data = json.load(file_installed_updates)

for key in installed_updates_data.keys():
    if key in installed_updates_data:
        installed_version = float(installed_versions_data[key])
        installed_update = float(installed_updates_data[key])
        test_params.append(tuple((key,installed_version,installed_update)))

@pytest.mark.parametrize("key,installed_version,installed_update", test_params)
def test_installed_vs_update_versions(key,installed_version,installed_update):
    """Model version update test_installed_vs_update_versions function"""
    message = f'{key}: installed version {installed_version} is equal to installed update version {installed_update}'
    assert installed_version != installed_update, print(message)