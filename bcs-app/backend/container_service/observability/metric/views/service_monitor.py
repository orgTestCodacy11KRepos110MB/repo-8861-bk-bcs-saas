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
import logging
from typing import Dict

from django.utils.translation import ugettext_lazy as _
from rest_framework.decorators import action
from rest_framework.response import Response

from backend.accounts import bcs_perm
from backend.bcs_web.audit_log.constants import BaseActivityStatus, BaseActivityType
from backend.bcs_web.viewsets import SystemViewSet
from backend.components.bcs.k8s import K8SClient
from backend.container_service.observability.metric import constants
from backend.container_service.observability.metric.serializers import (
    ServiceMonitorBatchDeleteSLZ,
    ServiceMonitorCreateSLZ,
    ServiceMonitorUpdateSLZ,
)
from backend.container_service.observability.metric.views.mixins import ServiceMonitorMixin
from backend.utils.basic import getitems
from backend.utils.error_codes import error_codes

logger = logging.getLogger(__name__)


class ServiceMonitorViewSet(SystemViewSet, ServiceMonitorMixin):
    """ 集群 ServiceMonitor 相关操作 """

    def list(self, request, project_id, cluster_id):
        """ 获取 ServiceMonitor 列表 """
        cluster_map = self._get_cluster_map(project_id)
        namespace_map = self._get_namespace_map(project_id)

        if cluster_id not in cluster_map:
            raise error_codes.APIError(_('集群 ID {} 不合法').format(cluster_id))

        client = K8SClient(request.user.token.access_token, project_id, cluster_id, env=None)
        manifest = client.list_service_monitor()
        response_data = self._handle_items(cluster_id, cluster_map, namespace_map, manifest)

        perm = bcs_perm.Namespace(request, project_id, bcs_perm.NO_RES)
        response_data = perm.hook_perms(response_data, ns_id_flag='namespace_id')
        response_data = self._update_service_monitor_perm(response_data)
        return Response(response_data)

    def create(self, request, project_id, cluster_id):
        """ 创建 ServiceMonitor """
        params = self.params_validate(ServiceMonitorCreateSLZ)

        name, namespace = params['name'], params['namespace']
        endpoints = [
            {
                'path': params['path'],
                'interval': params['interval'],
                'port': params['port'],
                'params': params.get('params') or {},
            }
        ]
        manifest = {
            'apiVersion': 'monitoring.coreos.com/v1',
            'kind': 'ServiceMonitor',
            'metadata': {
                'labels': {
                    'release': 'po',
                    'io.tencent.paas.source_type': 'bcs',
                    'io.tencent.bcs.service_name': params['service_name'],
                },
                'name': name,
                'namespace': namespace,
            },
            'spec': {
                'endpoints': endpoints,
                'selector': {'matchLabels': params['selector']},
                'sampleLimit': params['sample_limit'],
            },
        }

        client = K8SClient(request.user.token.access_token, project_id, cluster_id, env=None)
        result = self._single_service_monitor_operate_handler(
            client.create_service_monitor,
            _('创建'),
            project_id,
            BaseActivityType.Add,
            namespace,
            name,
            manifest,
            log_success=True,
        )
        return Response(result)

    @action(methods=['DELETE'], url_path='batch', detail=False)
    def batch_delete(self, request, project_id, cluster_id):
        """ 批量删除 ServiceMonitor """
        params = self.params_validate(ServiceMonitorBatchDeleteSLZ)
        svc_monitors = params['service_monitors']

        self._validate_namespace_use_perm(project_id, cluster_id, [sm['namespace'] for sm in svc_monitors])
        client = K8SClient(request.user.token.access_token, project_id, cluster_id, env=None)
        for m in svc_monitors:
            self._single_service_monitor_operate_handler(
                client.delete_service_monitor, _('删除'), project_id, BaseActivityType.Delete, m['namespace'], m['name']
            )

        metrics_names = ','.join([f"{sm['namespace']}/{sm['name']}" for sm in svc_monitors])
        message = _('删除 Metrics: {} 成功').format(metrics_names)
        self._activity_log(
            project_id,
            request.user.username,
            metrics_names,
            message,
            BaseActivityType.Delete,
            BaseActivityStatus.Succeed,
        )
        return Response({'successes': svc_monitors})


class ServiceMonitorDetailViewSet(SystemViewSet, ServiceMonitorMixin):
    """ 单个 ServiceMonitor 相关操作 """

    lookup_field = 'name'

    def retrieve(self, request, project_id, cluster_id, namespace, name):
        """ 获取单个 ServiceMonitor """
        client = K8SClient(request.user.token.access_token, project_id, cluster_id, env=None)
        result = client.get_service_monitor(namespace, name)
        if result.get('status') == 'Failure':
            raise error_codes.APIError(result.get('message', ''))

        labels = getitems(result, 'metadata.labels', {})
        result['metadata'] = {
            k: v for k, v in result['metadata'].items() if k not in constants.INNER_USE_SERVICE_METADATA_FIELDS
        }
        result['metadata']['service_name'] = labels.get(constants.SM_SERVICE_NAME_LABEL)

        if isinstance(getitems(result, 'spec.endpoints'), list):
            result['spec']['endpoints'] = self._handle_endpoints(result['spec']['endpoints'])

        return Response(result)

    def destroy(self, request, project_id, cluster_id, namespace, name):
        """ 删除 ServiceMonitor """
        self._validate_namespace_use_perm(project_id, cluster_id, namespace)
        client = K8SClient(request.user.token.access_token, project_id, cluster_id, env=None)
        result = self._single_service_monitor_operate_handler(
            client.delete_service_monitor,
            _('删除'),
            project_id,
            BaseActivityType.Delete,
            namespace,
            name,
            manifest=None,
            log_success=True,
        )
        return Response(result)

    def update(self, request, project_id, cluster_id, namespace, name):
        """ 更新 ServiceMonitor (先删后增) """
        params = self.params_validate(ServiceMonitorUpdateSLZ)
        client = K8SClient(request.user.token.access_token, project_id, cluster_id, env=None)
        result = self._single_service_monitor_operate_handler(
            client.get_service_monitor, _('更新'), project_id, BaseActivityType.Retrieve, namespace, name
        )
        manifest = self._update_manifest(result, params)

        # 更新会合并 selector，因此先删除, 再创建
        self._single_service_monitor_operate_handler(
            client.delete_service_monitor, _('更新'), project_id, BaseActivityType.Delete, namespace, name
        )
        result = self._single_service_monitor_operate_handler(
            client.create_service_monitor,
            _('更新'),
            project_id,
            BaseActivityType.Add,
            namespace,
            name,
            manifest,
            log_success=True,
        )
        return Response(result)

    def _update_manifest(self, manifest: Dict, params: Dict) -> Dict:
        """ 使用 api 请求参数更新 manifest """
        manifest['metadata']['labels']['release'] = 'po'
        manifest['spec']['selector'] = {'matchLabels': params['selector']}
        manifest['spec']['sampleLimit'] = params['sample_limit']
        manifest['spec']['endpoints'] = [
            {
                'path': params['path'],
                'interval': params['interval'],
                'port': params['port'],
                'params': params.get('params') or {},
            }
        ]
        manifest['metadata'] = {
            k: v for k, v in manifest['metadata'].items() if k not in constants.INNER_USE_SERVICE_METADATA_FIELDS
        }
        return manifest
