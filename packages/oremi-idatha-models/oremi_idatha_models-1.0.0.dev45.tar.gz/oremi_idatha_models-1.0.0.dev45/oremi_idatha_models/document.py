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
import json
import uuid
from datetime import datetime
from types import NoneType
from typing import Any
from typing import Generic
from typing import TypeVar

from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field


class BaseMeta(BaseModel):
  created_at: str = Field(default_factory=lambda: datetime.now().isoformat())
  updated_at: str | None = Field(default=None)


class UserMeta(BaseModel):
  uid: str
  created_at: str = Field(default_factory=lambda: datetime.now().isoformat())
  updated_at: str | None = Field(default=None)


Data = TypeVar('Data', bound=BaseModel | dict)
Computed = TypeVar('Computed', bound=BaseModel | NoneType)
Meta = TypeVar('Meta', bound=BaseMeta | UserMeta)


class Document(BaseModel, Generic[Data, Computed, Meta]):
  id: str = Field(default_factory=lambda: str(uuid.uuid4()), alias='_id')
  rev: str | None = Field(alias='_rev', default=None)
  type: str
  data: Data
  computed: Computed | None = None
  meta: Meta

  model_config = ConfigDict(
    arbitrary_types_allowed=True,
    populate_by_name=True,
    extra='forbid',
  )

  @classmethod
  def create_alias_from_user_meta(
    cls: type['Document[Data, Computed, Meta]'],
    data_cls: type[Data],
    computed_cls: type[Computed] | None = None,
    meta_cls: type[UserMeta] = UserMeta,
  ) -> 'Document[Data, Computed, UserMeta]':
    return cls.create_alias_from_base_meta(
      data_cls=data_cls,
      computed_cls=computed_cls,
      meta_cls=meta_cls,
    )

  @classmethod
  def create_alias_from_base_meta(
    cls: type['Document[Data, Computed, Meta]'],
    data_cls: type[Data],
    computed_cls: type[Computed] | None = None,
    meta_cls: type[BaseMeta] = BaseMeta,
  ) -> 'Document[Data, Computed, Meta]':
    class WrappedDocument(BaseModel):
      @staticmethod
      def model_validate(obj: dict[str, Any], **kwargs):
        data = data_cls.model_validate(obj['data']) if isinstance(data_cls, dict) else obj['data']
        meta = meta_cls.model_validate(obj['meta'])
        computed = computed_cls.model_validate(obj['computed']) if computed_cls and obj.get('computed') else None

        return cls.model_validate({**obj, 'data': data, 'meta': meta, 'computed': computed}, **kwargs)

      @classmethod
      def model_validate_json(cls, json_data: str, **kwargs):
        data_dict = json.loads(json_data)
        return WrappedDocument.model_validate(data_dict, **kwargs)

      def model_dump(self, by_alias: bool = True, **kwargs) -> dict[str, Any]:
        return super().model_dump(by_alias=by_alias, **kwargs)

    return WrappedDocument


GenericDocumentType = Document[dict, None, BaseMeta]
GenericDocument = GenericDocumentType.create_alias_from_base_meta(data_cls=dict)

GenericUserDocumentType = Document[dict, None, UserMeta]
GenericUserDocument = GenericUserDocumentType.create_alias_from_user_meta(data_cls=dict)
