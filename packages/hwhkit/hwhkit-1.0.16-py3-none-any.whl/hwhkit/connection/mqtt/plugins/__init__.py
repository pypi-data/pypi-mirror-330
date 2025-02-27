# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# Time       ：2025/1/4 11:05
# Author     ：Maxwell
# Description：
"""


from abc import ABC, abstractmethod


class PluginBase(ABC):
    @abstractmethod
    def on_message_published(self, topic: str, message: str) -> str:
        pass

    @abstractmethod
    def on_message_received(self, topic: str, message: str) -> str:
        pass