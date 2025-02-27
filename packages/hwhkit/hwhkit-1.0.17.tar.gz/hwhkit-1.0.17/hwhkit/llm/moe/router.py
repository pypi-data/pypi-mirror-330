# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# Time       ：2025/1/3 19:28
# Author     ：Maxwell
# Description：
"""
import random
from typing import Dict, List, Optional, AsyncGenerator
from hwhkit.llm.models import LanguageModel


class MOERouter:
    def __init__(self, model_instances: Dict[str, LanguageModel]):
        self.model_instances = model_instances

    async def chat(
        self, question: str, system_prompt: Optional[str] = None, history_messages: Optional[List[Dict]] = None
    ) -> str:
        selected_model = await self.select_model(question)
        return await selected_model.chat(question, system_prompt, history_messages)

    async def chat_stream(
        self, question: str, system_prompt: Optional[str] = None, history_messages: Optional[List[Dict]] = None
    ) -> AsyncGenerator[str, None]:
        selected_model = self.select_model(question)
        async for chunk in selected_model.chat_stream(question, system_prompt, history_messages):
            yield chunk

    async def select_model(self, question: str) -> LanguageModel:
        return random.choice(list(self.model_instances.values()))