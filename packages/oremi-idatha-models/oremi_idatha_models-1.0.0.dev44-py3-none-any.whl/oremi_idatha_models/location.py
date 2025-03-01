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
from pydantic import BaseModel


class Address(BaseModel):
  country: str
  country_code: str
  region: str | None = None
  postcode: int | str | None = None
  road: str | None = None
  town: str | None = None
  municipality: str | None = None
  county: str | None = None
  state: str | None = None
  city: str | None = None


class Location(BaseModel):
  type: str
  name: str
  boundingbox: list[float]
  lat: float
  lon: float
  addresstype: str
  display_name: str
  address: Address

  def __str__(self) -> str:
    info = [
      self.address.city,
      self.address.state,
      self.address.country,
    ]

    return ', '.join([item for item in info if item]) or self.display_name


class ComputedLocation(BaseModel):
  location: Location | None
