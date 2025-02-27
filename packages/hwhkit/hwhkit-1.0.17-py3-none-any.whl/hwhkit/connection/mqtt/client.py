import paho.mqtt.client as mqtt
import asyncio
from typing import Dict, Optional, Callable, Any, List
from hwhkit.utils import logger
from hwhkit.connection.mqtt.plugins import PluginBase
from hwhkit.connection.mqtt.plugins.encryption import EncryptionPlugin


class MQTTClientManager:
    def __init__(self, add_plugins=True, mqtt_config="mqtt_key_pairs.yaml"):
        self.clients: Dict[str, mqtt.Client] = {}
        self.topic_callbacks: Dict[str, List[Callable[[mqtt.Client, str], Any]]] = {}
        self.plugins = []

        if add_plugins:
            self.plugins.append(EncryptionPlugin(mqtt_config))
            # self.plugins.append(ProtobufPlugin())
            self.reversed_plugins = list(reversed(self.plugins))

    def create_client(
        self,
        client_id: str,
        broker: str,
        port: int = 1883,
        username: Optional[str] = None,
        password: Optional[str] = None,
    ) -> 'MQTTClientManager':
        if client_id in self.clients:
            raise ValueError(f"Client with ID {client_id} already exists.")

        client = mqtt.Client(client_id=client_id)
        if username and password:
            client.username_pw_set(username, password)

        client.broker = broker
        client.port = port
        client.on_connect = self._on_connect
        client.on_disconnect = self._on_disconnect
        client.reconnect_delay_set(min_delay=1, max_delay=120)

        self.clients[client_id] = client
        return self

    def get_client(self, client_id: str) -> Optional[mqtt.Client]:
        return self.clients.get(client_id)

    def remove_client(self, client_id: str):
        client = self.clients.pop(client_id, None)
        if client:
            client.disconnect()

    def add_plugin(self, plugin: PluginBase) -> 'MQTTClientManager':
        self.plugins.append(plugin)
        return self

    def start_all_clients(self) -> 'MQTTClientManager':
        for client_id, client in self.clients.items():
            client.connect(client.broker, client.port, 60)
            client.loop_start()
        return self

    def start_client(self, client_id: str):
        client = self.get_client(client_id)
        if client:
            client.connect(client.broker, client.port, 60)
            client.loop_start()
        else:
            raise ValueError(f"Client with ID {client_id} not found.")

    def _on_connect(self, client: mqtt.Client, userdata, flags, rc):
        if rc == 0:
            logger.info(f"Client {client._client_id.decode()} connected to MQTT Broker!")
        else:
            logger.info(f"Client {client._client_id.decode()} failed to connect, return code {rc}")

    def _on_disconnect(self, client: mqtt.Client, userdata, rc):
        logger.info(f"Client {client._client_id.decode()} disconnected from MQTT Broker!")
        if rc != 0:
            logger.info(f"Unexpected disconnection. Reconnecting...")
            client.reconnect()

    def _on_message(self, topic: str, client: mqtt.Client, msg: mqtt.MQTTMessage):
        logger.info(f"Received topic@{topic}, {msg.payload}")
        try:
            if topic in self.topic_callbacks:
                processed_message = msg.payload
                for plugin in self.reversed_plugins:
                    processed_message = plugin.on_message_received(topic, processed_message)
                for callback in self.topic_callbacks[topic]:
                    callback(client, processed_message)
        except Exception as e:
            logger.error(f"on_message error: {e}")

    def subscribe(self, topic: str):
        def decorator(callback: Callable[[mqtt.Client, str], Any]):
            if topic not in self.topic_callbacks:
                self.topic_callbacks[topic] = []

            self.topic_callbacks[topic].append(callback)

            for client_id, client in self.clients.items():
                client.subscribe(topic)
                client.message_callback_add(
                    topic,
                    lambda c, userdata, msg: self._on_message(topic, c, msg),
                )
            logger.info(f"Subscribed to topic: {topic}")
            return callback

        return decorator

    def publish(self, client_id: str, topic: str, message: str, qos: int = 0, retain: bool = False):
        client = self.get_client(client_id)
        if client:
            if not client.is_connected():
                logger.info(f"Client {client_id} is not connected. Attempting to reconnect...")
                client.reconnect()

            processed_message = message
            for plugin in self.plugins:
                processed_message = plugin.on_message_published(topic, processed_message)

            result = client.publish(topic, processed_message, qos=qos, retain=retain)
            if result.rc == mqtt.MQTT_ERR_SUCCESS:
                logger.info(f"Client {client_id} published message to {topic}")
            else:
                logger.info(f"Client {client_id} failed to publish message to {topic}, error code: {result.rc}")
        else:
            raise ValueError(f"Client with ID {client_id} not found.")