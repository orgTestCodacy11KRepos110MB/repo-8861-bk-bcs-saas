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
from unittest import mock

import pytest

from .fake_iam import FakeIAMClient

pytestmark = pytest.mark.django_db


@pytest.fixture(autouse=True)
def patch_iam_client():
    with mock.patch('backend.iam.views.IAMClient', new=FakeIAMClient):
        yield


class TestUserPermsViewSet:
    def test_get_perms_resource_type(self, api_client):
        """资源实例无关"""
        response = api_client.post(
            f'/api/iam/user_perms/', data={'action_ids': ['project_create', 'bcs_project_create']}
        )
        perms = response.json()['data']['perms']
        assert perms['project_create'] is True
        assert perms['bcs_project_create'] is False

    def test_get_perms_resource_inst(self, api_client, project_id, cluster_id):
        """资源实例相关"""
        data = {
            'action_ids': ['cluster_view', 'namespace_create'],
            'resource_type': 'cluster',
            'resource_id': cluster_id,
            'iam_path_attrs': {'project_id': project_id},
        }
        response = api_client.post(f'/api/iam/user_perms/', data)
        perms = response.json()['data']['perms']
        assert perms['cluster_view'] is True
        assert perms['namespace_create'] is False

    def test_get_perm_by_action_id_resource_type(self, api_client):
        """资源实例无关"""
        response = api_client.post(f'/api/iam/user_perms/actions/project_create/')
        assert response.json()['data']['perms']['project_create'] is True

        response = api_client.post(f'/api/iam/user_perms/actions/bcs_project_create/')
        perms = response.json()['data']['perms']
        assert perms['bcs_project_create'] is False
        assert 'apply_url' in perms

    def test_get_perm_by_action_id_resource_inst(self, api_client, project_id, cluster_id):
        """资源实例相关"""
        data = {
            'resource_type': 'cluster',
            'resource_id': cluster_id,
            'iam_path_attrs': {'project_id': project_id},
        }
        response = api_client.post(f'/api/iam/user_perms/actions/namespace_create/', data=data)
        perms = response.json()['data']['perms']
        assert perms['namespace_create'] is False
        assert 'apply_url' in perms
