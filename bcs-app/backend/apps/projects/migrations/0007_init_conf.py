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
# Generated by Django 1.11.5 on 2018-01-18 09:53
from __future__ import unicode_literals

from django.db import migrations

from backend.apps.projects.models import Conf


def init_conf(apps, schema_editor):
    """初始化配置信息
    """
    Conf.objects.get_or_create(
        key='STANDARD_LOG_PREFIX_KEY',
        defaults={
            "value": 'bcs_standard_log_v1_',
            "name": '标准日志采集前缀',
        }
    )
    Conf.objects.get_or_create(
        key='NON_STANDARD_LOG_PREFIX_KEY',
        defaults={
            "value": 'bcs_non_standard_log_v1_',
            "name": '非标准日志采集前缀',
        }
    )


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0006_auto_20180509_1148'),
    ]

    operations = [
        migrations.RunPython(init_conf)
    ]
