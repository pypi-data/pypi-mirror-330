# infoflow-robot

[![PyPI - Version](https://img.shields.io/pypi/v/infoflow-robot.svg)](https://pypi.org/project/infoflow-robot)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/infoflow-robot.svg)](https://pypi.org/project/infoflow-robot)

-----

## 目录

- [安装](#安装)
- [使用](#使用)

## 安装

```console
pip install infoflow-robot
```

## 使用

```python
import infoflow_robot
import infoflow_robot.message as msg


webhook = "http://example.com/webhook"
toid = [123456]

# 发送单条信息
robot = infoflow_robot.Robot(webhook, toid)
robot.send(msg.Text("Hello, World!\n你好，世界"))

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

## License

`infoflow-robot` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
