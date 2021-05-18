# -*- coding: utf-8 -*-
#
# Tencent is pleased to support the open source community by making 蓝鲸智云PaaS平台社区版 (BlueKing PaaS Community Edition) available.
# Copyright (C) 2017-2019 THL A29 Limited, a Tencent company. All rights reserved.
# Licensed under the MIT License (the "License"); you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://opensource.org/licenses/MIT
#
# Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
# an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the
# specific language governing permissions and limitations under the License.
#
import json

import pytest

from backend.resources.storages.storage_class.formatter import StorageClassFormatter
from backend.tests.resources.formatter.conftest import STORAGE_CONFIG_DIR


@pytest.fixture(scope="module", autouse=True)
def storage_class_configs():
    with open(f'{STORAGE_CONFIG_DIR}/storage_class.json') as fr:
        configs = json.load(fr)
    return configs


class TestStorageClassFormatter:
    def test_format_dict(self, storage_class_configs):
        """ 测试 format_dict 方法 """
        result = StorageClassFormatter().format_dict(storage_class_configs['normal'])
        assert set(result.keys()) == {'age', 'createTime', 'updateTime'}
