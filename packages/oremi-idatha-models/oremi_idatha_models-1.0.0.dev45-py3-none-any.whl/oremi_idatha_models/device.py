# Copyright 2024-2025 Sébastien Demanou. All Rights Reserved.
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
# ==============================================================================
from typing import Literal

from pydantic import BaseModel

from .document import BaseMeta
from .document import Document
from .location import ComputedLocation


class Device(BaseModel):
  name: str  # Human-readable name of the device
  timezone: str | None  # Timezone in which the device is located
  location: str | None  # Physical location of the device
  language: Literal['en', 'fr'] = 'fr'  # Language used to speak to Oremi on the device
  temperature_unit: Literal['Celsius', 'Fahrenheit'] = 'Celsius'  # Measurement unit for temperature (default: Celsius)
  distance_unit: Literal['Kilometers', 'Miles'] = 'Kilometers'  # Measurement unit for distance (default: Kilometers)
  follow_up_mode: bool = False  # Indicates if follow-up mode is enabled
  voice: str | None = None  # Voice type used by the device
  wake_word: Literal['Oremi'] = 'Oremi'  # Wake word used by the device
  do_not_disturb: bool = False  # Indicates if do not disturb mode is enabled
  platform: str
  architecture: str
  os_name: str


DeviceDocumentType = Document[Device, ComputedLocation, BaseMeta]
DeviceDocument = DeviceDocumentType.create_alias_from_base_meta(
  data_cls=Device,
  computed_cls=ComputedLocation,
)
