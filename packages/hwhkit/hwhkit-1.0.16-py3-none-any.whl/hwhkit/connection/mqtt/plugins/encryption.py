import base64
import yaml
import hashlib
import struct
import zlib
from pathlib import Path
from typing import Dict
from hwhkit.utils.security.rsa import RSACipher
from hwhkit.utils.security.ecc import ECCCipher
from hwhkit.utils.security.aes import AESCipher
from hwhkit.connection.mqtt.plugins import PluginBase


class EncryptionPlugin(PluginBase):
    def __init__(self, key_pairs_file: str):
        self.topic_keys: Dict[str, Dict[str, str]] = {}
        self.load_key_pairs(key_pairs_file)

    def load_key_pairs(self, key_pairs_file: str):
        if not Path(key_pairs_file).exists():
            self.generate_default_yaml(key_pairs_file)
        with open(key_pairs_file, "r") as f:
            data = yaml.safe_load(f)
        if "key_pairs" not in data:
            raise ValueError("Invalid key_pairs file format: missing 'key_pairs' key")
        self.topic_keys = data["key_pairs"]

    def generate_default_yaml(self, key_pairs_file: str):
        rsa = RSACipher()
        default_data = {
            "key_pairs": {
                "default_topic": {
                    "algorithm": "rsa",
                    "public": rsa.serialize_public_key().decode('utf-8').strip(),
                    "private": rsa.serialize_private_key().decode('utf-8').strip()
                }
            }
        }
        with open(key_pairs_file, "w") as f:
            yaml.safe_dump(default_data, f)
        print(f"Generated default YAML file at: {key_pairs_file}")

    def get_keys(self, topic: str) -> Dict[str, str]:
        if topic not in self.topic_keys:
            raise ValueError(f"No keypair found for topic: {topic}")
        return self.topic_keys[topic]

    def hash_key(self, key: str) -> bytes:
        hasher = hashlib.sha256()
        hasher.update(key.encode('utf-8'))
        return hasher.digest()

    def encode_payload(self, algorithm: str, encrypted_aes_key: bytes, encrypted_message: bytes) -> str:
        if algorithm == "aes":
            algorithm_code = 0
        elif algorithm == "rsa":
            algorithm_code = 1
        elif algorithm == "ecc":
            algorithm_code = 2
        else:
            raise ValueError(f"Unsupported algorithm: {algorithm}")
        if len(encrypted_message) > 50000:
            raise ValueError("Message length exceeds 50,000 characters")
        payload = bytearray()
        payload.append(algorithm_code)
        payload.extend(struct.pack('>H', len(encrypted_message)))
        payload.extend(encrypted_message)
        if algorithm != "aes":
            payload.extend(encrypted_aes_key)
        crc32 = zlib.crc32(payload)
        payload.extend(struct.pack('>I', crc32))
        return base64.urlsafe_b64encode(payload).decode('utf-8')

    def decode_payload(self, payload: str) -> tuple:
        payload_bytes = base64.urlsafe_b64decode(payload + '=' * (-len(payload) % 4))
        crc32 = struct.unpack('>I', payload_bytes[-4:])[0]
        if zlib.crc32(payload_bytes[:-4]) != crc32:
            raise ValueError("Payload checksum mismatch")
        algorithm_code = payload_bytes[0]
        if algorithm_code == 0:
            algorithm = "aes"
        elif algorithm_code == 1:
            algorithm = "rsa"
        elif algorithm_code == 2:
            algorithm = "ecc"
        else:
            raise ValueError("Invalid algorithm code in payload")
        v_length = struct.unpack('>H', payload_bytes[1:3])[0]
        if v_length > 50000:
            raise ValueError("Message length exceeds 50,000 characters")
        v_start = 3
        v_end = v_start + v_length
        v = payload_bytes[v_start:v_end]
        k = payload_bytes[v_end:-4] if algorithm != "aes" else None
        return algorithm, k, v

    def on_message_published(self, topic: str, message: str) -> str:
        try:
            keys = self.get_keys(topic)
            algorithm = keys.get("algorithm", "rsa")
            if algorithm == "aes":
                aes_key = keys.get("private")
                if not aes_key:
                    raise ValueError("AES key is missing for AES algorithm")
                hashed_key = self.hash_key(aes_key)
                aes_cipher = AESCipher(key=hashed_key)
                encrypted_message = aes_cipher.encrypt(message).encode('utf-8')
                encrypted_aes_key = b""
            else:
                aes_cipher = AESCipher()
                aes_key = aes_cipher.get_key()
                if algorithm == "rsa":
                    public_key_pem = keys["public"]
                    public_key_pem_bytes = public_key_pem.encode('utf-8')
                    public_key = RSACipher.deserialize_public_key(public_key_pem_bytes)
                    cipher = RSACipher(public_key=public_key)
                elif algorithm == "ecc":
                    public_key_pem = keys["public"]
                    public_key_pem_bytes = public_key_pem.encode('utf-8')
                    public_key = ECCCipher.deserialize_public_key(public_key_pem_bytes)
                    cipher = ECCCipher(public_key=public_key)
                else:
                    raise ValueError(f"Unsupported algorithm: {algorithm}")
                encrypted_aes_key = cipher.encrypt(aes_key.encode('utf-8'))
                encrypted_message = aes_cipher.encrypt(message).encode('utf-8')
            payload = self.encode_payload(algorithm, encrypted_aes_key, encrypted_message)
            return payload
        except Exception as e:
            raise ValueError(f"Encryption failed: {str(e)}")

    def on_message_received(self, topic: str, message: bytes) -> str:
        try:
            keys = self.get_keys(topic)
            algorithm, k, v = self.decode_payload(message.decode('utf-8'))
            if algorithm == "aes":
                aes_key = keys.get("private")
                if not aes_key:
                    raise ValueError("AES key is missing for AES algorithm")
                hashed_key = self.hash_key(aes_key)
                aes_cipher = AESCipher(key=hashed_key)
                return aes_cipher.decrypt(v.decode('utf-8'))
            else:
                if k is None:
                    raise ValueError("Invalid payload format: missing 'k' for RSA/ECC")
                private_key_pem = keys["private"]
                private_key_pem_bytes = private_key_pem.encode('utf-8')
                if algorithm == "rsa":
                    private_key = RSACipher.deserialize_private_key(private_key_pem_bytes)
                    cipher = RSACipher(private_key=private_key)
                elif algorithm == "ecc":
                    private_key = ECCCipher.deserialize_private_key(private_key_pem_bytes)
                    cipher = ECCCipher(private_key=private_key)
                else:
                    raise ValueError(f"Unsupported algorithm: {algorithm}")
                aes_key = cipher.decrypt(k)
                aes_cipher = AESCipher(key=AESCipher.get_key_bytes(aes_key))
                return aes_cipher.decrypt(v.decode('utf-8'))
        except Exception as e:
            raise ValueError(f"Decryption failed: {str(e)}")