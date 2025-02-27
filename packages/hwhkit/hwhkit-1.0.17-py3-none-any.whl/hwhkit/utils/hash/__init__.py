# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# Time       ：2025/1/6 15:46
# Author     ：Maxwell
# Description：
"""

import hashlib
import uuid
import time
import random


class HashManager(object):

    @classmethod
    def md5(cls, content: str) -> str:
        if not content:
            content = ""
        md5_hash = hashlib.md5()
        md5_hash.update(content.encode('utf-8'))
        return md5_hash.hexdigest()

    @classmethod
    def sha256(cls, content: str) -> str:
        if not content:
            content = ""
        sha256_hash = hashlib.sha256()
        sha256_hash.update(content.encode('utf-8'))
        return sha256_hash.hexdigest().upper()

    @classmethod
    def generate_uuid(cls) -> str:
        return uuid.uuid4().hex.upper()

    @classmethod
    def uuid(cls) -> str:
        uuid_str = uuid.uuid1().hex.upper()
        unique_id = "-".join([str(random.randint(0, 100_0000_0000)) for _ in range(10)])
        return cls.sha256(f"{uuid_str}-{int(time.time())}-{unique_id}").upper()

    @classmethod
    def is_sha256(cls, string):
        if len(string) != 64:
            return False
        try:
            hashlib.sha256(string.encode()).hexdigest()
            return True
        except ValueError:
            return False


