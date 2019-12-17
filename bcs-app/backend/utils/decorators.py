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
import logging
import time
from functools import wraps
from urllib import parse

import six
from django.utils.encoding import force_str
from django.utils.translation import ugettext_lazy as _
from requests.models import Response

from backend.apps.constants import SENSITIVE_KEYWORD
from backend.utils.exceptions import ComponentError

logger = logging.getLogger(__name__)

# 格式化方法
FORMAT_FUNC = {
    'json': json.loads,
}

# 最大返回字符数 10KB
MAX_RESP_TEXT_SIZE = 1024 * 10

# 马赛克
MOSAIC_CHAR = '*'
MOSAIC_WORD = MOSAIC_CHAR * 3


def requests_curl_log(resp, st, params):
    """记录requests curl log
    """
    if not isinstance(resp, Response):
        raise ValueError(_("返回值[{}]必须是Respose对象").format(resp))

    desensitive_params = {}
    # params 可能为 None
    params = params or {}
    for key, value in params.items():
        if key in SENSITIVE_KEYWORD:
            desensitive_params[key] = MOSAIC_WORD
        else:
            desensitive_params[key] = value

    raw_url = parse.urlparse(resp.request.url)
    desensitive_url = raw_url._replace(query=parse.urlencode(desensitive_params, safe=MOSAIC_CHAR)).geturl()

    # 添加日志信息
    curl_req = "REQ: curl -X {method} '{url}'".format(method=resp.request.method, url=desensitive_url)

    if resp.request.body:
        curl_req += " -d '{body}'".format(body=force_str(resp.request.body))

    if resp.request.headers:
        for key, value in resp.request.headers.items():
            # ignore headers
            if key in ['User-Agent', 'Accept-Encoding', 'Connection', 'Accept', 'Content-Length']:
                continue
            if key == 'Cookie' and value.startswith('x_host_key'):
                continue

            # 去除敏感信息, key保留, 表示鉴权信息有传递
            if key in SENSITIVE_KEYWORD:
                value = MOSAIC_WORD

            curl_req += " -H '{k}: {v}'".format(k=key, v=value)

    if len(resp.text) > MAX_RESP_TEXT_SIZE:
        resp_text = f"{resp.text[:MAX_RESP_TEXT_SIZE]}...(total {len(resp.text)} Bytes)"
    else:
        resp_text = resp.text

    curl_resp = 'RESP: [%s] %.2fms %s' % (resp.status_code, (time.time() - st) * 1000, resp_text)

    logger.info('%s\n \t %s', curl_req, curl_resp)


def response(f=None):
    """返回值格式化
    """

    def decorator(func):
        @wraps(func)
        def _wrapped_func(*args, **kwargs):
            resp = func(*args, **kwargs)
            format_func = FORMAT_FUNC.get(f)
            if format_func:
                # 获取内容
                if isinstance(resp, Response):
                    content = resp.text
                elif isinstance(resp, six.string_types):
                    content = resp
                else:
                    raise ValueError(_("返回值[{}]必须是字符串或者Respose对象").format(resp))

                # 解析格式
                err_msg = kwargs.get('err_msg', None)
                try:
                    resp = format_func(content)
                except Exception as error:
                    logger.exception(
                        "请求第三方失败，使用【%s】格式解析 %s 异常，%s", f, content, error)
                    raise ComponentError(err_msg or error)

            return resp
        return _wrapped_func
    return decorator
