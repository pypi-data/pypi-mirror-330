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
from typing import Any
from typing import Literal

from pydantic import BaseModel

from .document import BaseMeta
from .document import Document
from .document import UserMeta


class Field(BaseModel):
  name: str
  type: Literal['string', 'number', 'null', 'date', 'time', 'datetime', 'boolean', 'array', 'object', 'any'] = 'any'
  optional: bool = False
  scope: Literal['data', 'meta', 'computed'] = 'data'

  @property
  def scoped_name(self) -> str:
    return f'{self.scope}.{self.name}'

  def lower_than(self, value: Any) -> 'ViewFilter':
    return ViewFilter(
      field=self.scoped_name,
      operator='<',
      value=value,
    )

  def lower_than_or_equal(self, value: Any) -> 'ViewFilter':
    return ViewFilter(
      field=self.scoped_name,
      operator='<=',
      value=value,
    )

  def equal_to(self, value: Any) -> 'ViewFilter':
    return ViewFilter(
      field=self.scoped_name,
      operator='==',
      value=value,
    )

  def greater_than_or_equal(self, value: Any) -> 'ViewFilter':
    return ViewFilter(
      field=self.scoped_name,
      operator='>=',
      value=value,
    )

  def greater_than(self, value: Any) -> 'ViewFilter':
    return ViewFilter(
      field=self.scoped_name,
      operator='>',
      value=value,
    )

  def in_values(self, values: Any) -> 'ViewFilter':
    return ViewFilter(
      field=self.scoped_name,
      operator='in',
      value=values,
    )


FieldCreatedAt = Field(name='created_at', type='datetime', scope='meta')
FieldUpdatedAt = Field(name='updated_at', type='datetime', scope='meta', optional=True)


class ViewFilter(BaseModel):
  field: str
  operator: Literal['<', '<=', '==', '>=', '>', 'in']
  value: Any


class CollectionView(BaseModel):
  name: str
  sort_field: str | None = None  # By default FieldCreatedAt will be used
  filters: list[ViewFilter] | None = None


class Collection(BaseModel):
  name: str
  fields: list[Field]
  views: list[CollectionView]


CollectionDocument = Document[Collection, None, BaseMeta].create_alias_from_base_meta(
  data_cls=Collection,
)

UserCollectionDocument = Document[Collection, None, UserMeta].create_alias_from_user_meta(
  data_cls=Collection,
)
