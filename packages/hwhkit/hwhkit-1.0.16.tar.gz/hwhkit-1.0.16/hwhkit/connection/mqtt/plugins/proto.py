# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# Time       ：2025/1/4 11:05
# Author     ：Maxwell
# Description：
"""

from hwhkit.connection.mqtt.plugins import proto_pb2
from hwhkit.connection.mqtt.plugins import PluginBase


class ProtobufPlugin(PluginBase):
    def on_message_published(self, topic: str, message: str) -> str:
        payload = proto_pb2.EncryptedPayload(data=message.encode('utf-8'))
        return payload.SerializeToString()

    def on_message_received(self, topic: str, message: str) -> str:
        payload_proto = proto_pb2.EncryptedPayload()
        payload_proto.ParseFromString(message)
        return payload_proto.data.decode('utf-8')