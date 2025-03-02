# SPDX-FileCopyrightText: 2025-present jiwen <ji.wen@foxmail.com>
#
# SPDX-License-Identifier: MIT
from typing import Sequence

from pydantic import BaseModel
import httpx

from . import message as msg


class _MsgPayload(BaseModel):
    message: msg._Message


class _MsgResponse(BaseModel):
    errcode: int
    errmsg: str


class InfoflowRobotSendError(Exception):
    pass


class Robot:
    """如流机器人

    Args:
        webhook (str): 机器人的 webhook 地址
        toid (list[int]): 接收消息的群 id
    """
    def __init__(self, webhook: str, toid: list[int]) -> None:
        self.webhook = webhook
        self.toid = toid
        self._http_client = None
        self._is_in_ctx_manager = False

    def send(self, bodies: msg.MessageBody | Sequence[msg.MessageBody]) -> None:
        """发送消息

        Args:
            bodies (MessageBody | Sequence[MessageBody]): 消息体, 支持 5 种类型
                文本 (`Text`)、链接 (`Link`)、@ (`At`)、图片 (`Image`) 、Markdown (`Markdown`)

        Examples:
            ```python
            import infoflow_robot
            import infoflow_robot.message as msg

            webhook = "http://example.com/webhook"
            toid = [123456]

            # 发送单条信息
            robot = infoflow_robot.Robot(webhook, toid)
            robot.send(msg.Text("Hello, World!\\n你好，世界"))

            # 发送多条信息 (session 复用)
            with infoflow_robot.Robot(webhook, toid) as robot:
                robot.send(msg.Text("崭新的一年即将开始，愿新的一年里我们都能收获成长与喜悦！"))
                robot.send([
                    msg.Text("本周五晚上有聚餐，记得来！"),
                    msg.At(atall=True),
                ])

            # 发送图片
            import base64
            with open("loveyou.png", "rb") as f:
                img = base64.b64encode(f.read())
            robot.send(msg.Image(img))
            ```
        """
        if isinstance(bodies, msg.MessageBody):
            bodies = [bodies]
        else:
            bodies = list(bodies)
        payload = _MsgPayload(message=msg._Message(
            header=msg._Header(toid=self.toid),
            body=bodies
        ))
        http_post = httpx.post if self._http_client is None else self._http_client.post
        r = http_post(self.webhook, json=payload.model_dump())
        r.raise_for_status()
        res = _MsgResponse.model_validate_json(r.text)
        if res.errcode != 0:
            raise InfoflowRobotSendError(f"errorcode: {res.errcode}, {res.errmsg}")

    def __enter__(self):
        self._http_client = httpx.Client()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._http_client.close()
