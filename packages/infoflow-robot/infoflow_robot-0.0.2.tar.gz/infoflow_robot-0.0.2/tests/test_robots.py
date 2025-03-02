# SPDX-FileCopyrightText: 2025-present jiwen <ji.wen@foxmail.com>
#
# SPDX-License-Identifier: MIT
import pytest
import httpx
from infoflow_robot._robot import Robot, _MsgResponse
import infoflow_robot.message as msg


@pytest.fixture
def robot():
    webhook = "http://example.com/webhook"
    toid = [123456]
    return Robot(webhook, toid)


def test_one_off_post(robot, mocker):
    mock_post = mocker.patch.object(httpx, 'post')
    mock_post.raise_for_status = lambda: None
    mock_post.return_value.text = _MsgResponse(errcode=0, errmsg="ok").model_dump_json()

    robot.send(msg.Text("hello"))
    mock_post.assert_called_once()


def test_reuse_client_for_posts(robot, mocker):
    mock_post = mocker.patch.object(httpx.Client, 'post')
    mock_post.raise_for_status = lambda: None
    mock_post.return_value.text = _MsgResponse(errcode=0, errmsg="ok").model_dump_json()

    messages = [
        msg.Text("hello, world!"),
        msg.Text("你好，世界！"),
    ]
    with robot:
        for message in messages:
            robot.send(message)
    assert mock_post.call_count == len(messages)


def test_context_manager(robot):
    with robot as bot:
        assert bot._http_client is not None
    assert bot._http_client.is_closed
