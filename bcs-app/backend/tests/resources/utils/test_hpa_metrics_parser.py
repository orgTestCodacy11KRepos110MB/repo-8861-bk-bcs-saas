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
#
import json

import pytest
from django.conf import settings

from backend.resources.hpa.utils import HPAMetricsParser

# 用于测试解析器的文件路径
TEST_CONFIG_PATH = f'{settings.BASE_DIR}/backend/tests/resources/utils/contents/hpa4parser.json'

with open(TEST_CONFIG_PATH) as fr:
    hpa_configs = json.load(fr)


class TestHPAMetricsParser:
    @pytest.mark.parametrize('manifest, expected', [(v, k) for k, v in hpa_configs.items()])
    def test_metrics_parser(self, manifest, expected):
        assert HPAMetricsParser(manifest).parse() == expected