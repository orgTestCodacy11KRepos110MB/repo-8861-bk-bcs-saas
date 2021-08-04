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
from dataclasses import dataclass
from typing import Dict, List, Optional, Type

from backend.iam.permissions.perm import PermCtx, Permission, ResourceRequest
from backend.iam.permissions.resources.project import related_project_perm
from backend.packages.blue_krill.data_types.enum import EnumField, StructuredEnum

from .. import decorators
from ..request import ActionResourcesRequest

ResourceType = 'cluster'


class ClusterAction(str, StructuredEnum):
    CREATE = EnumField('cluster_create', label='cluster_create')
    VIEW = EnumField('cluster_view', label='cluster_view')
    MANAGE = EnumField('cluster_manage', label='cluster_manage')
    DELETE = EnumField('cluster_delete', label='cluster_delete')


@dataclass
class ClusterPermCtx(PermCtx):
    project_id: str = ''
    cluster_id: Optional[str] = None


class ClusterRequest(ResourceRequest):
    resource_type: str = ResourceType
    attr = {'_bk_iam_path_': f'/project,{{project_id}}/'}

    def _make_attribute(self, res_id: str) -> Dict:
        self.attr['_bk_iam_path_'] = self.attr['_bk_iam_path_'].format(project_id=self.attr_kwargs['project_id'])
        return self.attr


class related_cluster_perm(decorators.RelatedPermission):

    module_name: str = ResourceType

    def _convert_perm_ctx(self, instance, args, kwargs) -> PermCtx:
        """仅支持第一个参数是 PermCtx 子类实例"""
        if len(args) <= 0:
            raise TypeError('missing ClusterPermCtx instance argument')
        if isinstance(args[0], PermCtx):
            return ClusterPermCtx(
                username=args[0].username, project_id=args[0].project_id, cluster_id=args[0].cluster_id
            )
        else:
            raise TypeError('missing ClusterPermCtx instance argument')

    def _action_request_list(self, perm_ctx: ClusterPermCtx) -> List[ActionResourcesRequest]:
        """"""
        resources = [perm_ctx.cluster_id] if perm_ctx.cluster_id else None
        return [
            ActionResourcesRequest(
                resource_type=self.perm_obj.resource_type, action_id=self.action_id, resources=resources
            )
        ]


class cluster_perm(decorators.Permission):
    module_name: str = ResourceType


class ClusterPermission(Permission):
    """集群权限"""

    resource_type: str = ResourceType
    resource_request_cls: Type[ResourceRequest] = ClusterRequest

    @related_project_perm(method_name='can_view')
    def can_create(self, perm_ctx: ClusterPermCtx, raise_exception: bool = True) -> bool:
        return self.can_action(perm_ctx, ClusterAction.CREATE, raise_exception)

    @related_project_perm(method_name='can_view')
    def can_view(self, perm_ctx: ClusterPermCtx, raise_exception: bool = True) -> bool:
        return self.can_action(perm_ctx, ClusterAction.VIEW, raise_exception, use_cache=True)

    @related_cluster_perm(method_name='can_view')
    def can_manage(self, perm_ctx: ClusterPermCtx, raise_exception: bool = True) -> bool:
        return self.can_action(perm_ctx, ClusterAction.MANAGE, raise_exception)

    @related_cluster_perm(method_name='can_view')
    def can_delete(self, perm_ctx: ClusterPermCtx, raise_exception: bool = True) -> bool:
        return self.can_action(perm_ctx, ClusterAction.DELETE, raise_exception)

    def _make_res_request(self, res_id: str, perm_ctx: ClusterPermCtx) -> ResourceRequest:
        return self.resource_request_cls(res_id, project_id=perm_ctx.project_id)

    def _get_resource_id_from_ctx(self, perm_ctx: ClusterPermCtx) -> Optional[str]:
        return perm_ctx.cluster_id
