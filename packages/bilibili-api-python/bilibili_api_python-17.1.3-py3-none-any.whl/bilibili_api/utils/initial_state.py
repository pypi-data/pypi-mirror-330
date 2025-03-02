"""
bilibili_api.utils.initial_state

用于获取页码的初始化信息
"""

import re
import json
from enum import Enum
from typing import Tuple

from ..exceptions import *
from .network import Api, Credential, HEADERS


class InitialDataType(Enum):
    """
    识别返回类型
    """

    INITIAL_STATE = "window.__INITIAL_STATE__"
    NEXT_DATA = "__NEXT_DATA__"


async def get_initial_state(
    url: str, credential: Credential = Credential()
) -> Tuple[dict, InitialDataType]:
    """
    异步获取初始化信息

    Args:
        url (str): 链接

        credential (Credential, optional): 用户凭证. Defaults to Credential().
    """
    try:
        resp = await Api(
            url=url, method="GET", credential=credential, comment="[获取初始化信息]"
        ).request(byte=True)
    except Exception as e:
        raise e
    else:
        content = resp.decode("utf-8")
        pos = content.find("window.__INITIAL_STATE__=")
        if pos == -1:
            pos = content.find('<script id="__NEXT_DATA__" type="application/json">')
            content_type = InitialDataType.NEXT_DATA
            if pos == -1:
                raise ApiException("未找到相关信息")
            pos += len('<script id="__NEXT_DATA__" type="application/json">')
        else:
            content_type = InitialDataType.INITIAL_STATE
            pos += len("window.__INITIAL_STATE__=")
        try:
            content = json.JSONDecoder().raw_decode(content[pos:])[0]
        except json.JSONDecodeError:
            raise ApiException("信息解析错误")
        return content, content_type
