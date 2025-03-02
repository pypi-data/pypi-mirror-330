# SPDX-FileCopyrightText: 2025-present jiwen <ji.wen@foxmail.com>
#
# SPDX-License-Identifier: MIT
from typing import Literal
from pydantic import BaseModel


class Text(BaseModel):
    """文本类型"""
    content: str
    type: Literal["TEXT"] = "TEXT"

    def __init__(self, content: str):
        """文本消息

        Args:
            content (str): 文本内容, 总长度不得超过 2k，使用 \\n 换行
        """
        super().__init__(content=content)


class Link(BaseModel):
    """链接类型"""
    href: str
    type: Literal["LINK"] = "LINK"
    label: str | None = None

    def __init__(self, href: str, label: str | None = None):
        """链接消息

        Args:
            href (str): 跳转的链接, 单个链接长度不得超过 1k，暂不支持自定义链接文字
            type (str): 固定为 "LINK", 表示链接类型
            label (str, optional): 超链接显示文本
        """
        super().__init__(href=href, label=label)


class At(BaseModel):
    """@群成员"""
    atuserids: list[str] | None = None
    atall: bool = False
    type: Literal["AT"] = "AT"

    def __init__(self, atuserids: list[str] | None = None, atall: bool = False):
        """@群成员消息

        `atuserids` 与 `atall` 必须选填一个，若只选 `atall` 则对应值必须填 `True`，否则会发送失败.

        Args:
            atuserids (list[str], optional): userid 为企业后台通讯录中成员录入的成员 ID 字段
            atall (bool, optional): @全体成员
        """
        super().__init__(atuserids=atuserids, atall=atall)


class Image(BaseModel):
    """图片类型"""
    content: str
    type: Literal["IMAGE"] = "IMAGE"

    def __init__(self, content: str):
        """图片消息

        支持与 `Text`、`At` 以及 `Link` 类型消息同时发送.

        Args:
            content (str): 单张图片 base64 编码后的值，不要携带 "data:image/jpg;base64" 描述信息，否则会发送失败
        """
        super().__init__(content=content)


class Markdown(BaseModel):
    """Markdown 类型"""
    content: str
    type: Literal["MD"] = "MD"

    def __init__(self, content: str):
        """Markdown 消息

        Args:
            content (str): Markdown 格式的消息内容，总长度不得超过 2k 个字符

        Notes:
            支持的语法子集:
            ```
            1. 标题: 1-6 级标题
                # 一级标题
                ## 二级标题
                ### 三级标题
                #### 四级标题
                ##### 五级标题
                ###### 六级标题
            2. 粗体: **加粗文本**
            3. 斜体: *斜体文本*
            4. 引用: > 引用文本
            5. 字体颜色：只支持三种内置颜色 green (绿色)、gray (灰色)、red (红色)
                <font color="green">绿色</font>
                <font color="gray">灰色</font>
                <font color="red">红色</font>
                (注意: `color=` 后边只能用双引号，用单引号不会显示颜色)
            6. 链接:
                [百度一下](https://www.baidu.com)
                https://www.baidu.com
            7. 有序列表: 序号和文本之间要加一个空格
                1. 有序列表
                2. 有序列表
                3. 有序列表
            8. 无序列表: - 和文本之间要加一个空格
                - 无序列表
                - 无序列表
            9. 行内代码: `code`
            ```
        """
        super().__init__(content=content)


# 消息体
MessageBody = Text | Link | At | Image | Markdown


class _Header(BaseModel):
    """消息头部"""
    toid: list[int]


class _Message(BaseModel):
    """消息对象"""
    header: _Header
    body: list[MessageBody]
