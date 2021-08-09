# -*- coding: utf-8 -*-
"""
Tencent is pleased to support the open source community by making 蓝鲸智云PaaS平台社区版 (BlueKing PaaS Community
Edition) available.
Copyright (C) 2017-2021 THL A29 Limited, a Tencent company. All rights reserved.
Licensed under the MIT License (the "License"); you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://opensource.org/licenses/MIT

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the
specific language governing permissions and limitations under the License.
"""
# Generated by Django 1.11.5 on 2018-05-09 03:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0005_auto_20180326_1725'),
    ]

    operations = [
        migrations.CreateModel(
            name='Conf',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creator', models.CharField(max_length=32, verbose_name='创建者')),
                ('updator', models.CharField(max_length=32, verbose_name='修改着')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('deleted_time', models.DateTimeField(blank=True, null=True)),
                ('key', models.CharField(max_length=64, unique=True, verbose_name='标识')),
                ('name', models.CharField(max_length=128, verbose_name='名称')),
                ('value', models.TextField(verbose_name='值')),
            ],
            options={
                'verbose_name': '平台配置',
                'verbose_name_plural': '平台配置',
            },
        ),
        migrations.AlterField(
            model_name='projectuser',
            name='status',
            field=models.IntegerField(choices=[(0, '正常'), (1, '在职'), (2, '已离职'), (3, '试用'), (8, '待入职'), (9, '待入职')], default=0),
        ),
    ]
