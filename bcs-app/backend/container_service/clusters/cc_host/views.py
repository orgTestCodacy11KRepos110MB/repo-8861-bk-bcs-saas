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
import logging

from rest_framework.decorators import action
from rest_framework.response import Response

from backend.bcs_web.viewsets import SystemViewSet
from backend.components import cc
from backend.container_service.clusters.serializers import FetchCCHostSLZ
from backend.utils.filter import filter_by_ips
from backend.utils.paginator import custom_paginator

from . import utils

logger = logging.getLogger(__name__)


class CCViewSet(SystemViewSet):
    """ CMDB 主机查询相关接口 """

    @action(methods=['GET'], url_path='topology', detail=False)
    def biz_inst_topo(self, request, project_id):
        """ 查询业务实例拓扑 """
        topo_info = cc.search_biz_inst_topo(request.user.username, request.project.cc_app_id)
        return Response(data=topo_info)

    @action(methods=['POST'], url_path='hosts', detail=False)
    def hosts(self, request, project_id):
        """ 查询指定业务拓扑下主机列表 """
        params = self.params_validate(FetchCCHostSLZ)
        username = request.user.username
        access_token = request.user.token.access_token
        bk_biz_id = request.project.cc_app_id

        # 从 CMDB 获取可用主机信息，业务名称信息
        host_list = utils.fetch_cc_app_hosts(username, bk_biz_id, params['set_id'], params['module_id'])
        cc_app_name = cc.get_application_name(username, bk_biz_id)

        # 根据指定的 IP 过滤
        host_list = filter_by_ips(host_list, params['ip_list'], key='bk_host_innerip', fuzzy=params['fuzzy'])

        response_data = {'results': [], 'count': 0, 'cc_app_name': cc_app_name}
        # 补充节点使用情况，包含使用的项目 & 集群
        project_cluster_info = utils.fetch_project_cluster_info(access_token)
        all_cluster_nodes = utils.fetch_all_cluster_nodes(access_token)
        host_list = utils.attach_project_cluster_info(host_list, all_cluster_nodes, project_cluster_info)

        # 更新 可选择的机器 数量信息
        response_data['selectable_cnt'] = len([h for h in host_list if utils.is_host_selectable(h)])

        # 如没有符合过滤条件的，直接返回默认值
        if not host_list:
            return Response(response_data)

        ret = custom_paginator(host_list, params['offset'], params['limit'])
        # 更新 Host 的 GSE Agent 状态信息
        ret['results'] = utils.update_gse_agent_status(username, ret['results'])

        response_data['results'] = ret['results']
        response_data['count'] = ret['count']
        return Response(response_data)
