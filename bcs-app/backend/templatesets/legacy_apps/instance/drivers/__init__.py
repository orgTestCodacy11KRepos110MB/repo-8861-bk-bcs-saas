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
from backend.apps.constants import ProjectKind
from backend.templatesets.legacy_apps.instance.drivers import k8s

ClusterType = dict(ProjectKind._choices_labels.get_choices())


def get_scheduler_driver(access_token, project_id, configuration, project_kind):
    cluster_type = ClusterType.get(project_kind)

    if cluster_type == 'Kubernetes':
        schduler = k8s.Scheduler(access_token, project_id, configuration, kind="Kubernetes", is_rollback=True)
    else:
        raise NotImplementedError("only support k8s")
    return schduler
