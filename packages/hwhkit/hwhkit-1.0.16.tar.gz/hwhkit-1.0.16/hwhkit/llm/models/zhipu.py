import traceback
import random
from openai import OpenAI
from typing import List, Dict, Optional, AsyncGenerator
from hwhkit.utils import logger
from hwhkit.llm.models import ModelStrategy, LanguageModelProperty


class ZhipuStrategy(ModelStrategy):
    def __init__(self, keys: Dict[str, str], model_property: LanguageModelProperty):
        self._keys = keys
        self._property = model_property
        self._client_pool = self._initialize_client_pool()

    def get_name(self) -> str:
        return "zhipu"

    def base_url(self) -> str:
        return "https://open.bigmodel.cn/api/paas/v4/"

    def _initialize_client_pool(self) -> List[Dict[str, OpenAI]]:
        return [{"name": k, "client": OpenAI(api_key=v, base_url=self.base_url())} for k, v in self._keys.items()]

    def _get_client(self) -> Dict[str, OpenAI]:
        if not self._client_pool:
            raise Exception(f"No {self.get_name()} client available.")
        return random.choice(self._client_pool)

    async def gen_messages(
            self, question: str, system_prompt: Optional[str] = None, history_messages: Optional[List[Dict]] = None
    ) -> List[Dict[str, str]]:
        messages = []
        if system_prompt:
            messages.append({'role': 'system', 'content': system_prompt})
        if history_messages:
            messages.extend(history_messages)
        if question:
            messages.append({'role': 'user', 'content': question})
        return messages

    async def chat(self, messages: List[Dict[str, str]]) -> str:
        client_info = self._get_client()
        client_name, client = client_info["name"], client_info["client"]

        try:
            response = client.chat.completions.create(
                model=self._property.name,
                messages=messages,
                timeout=self._property.timeout,
                temperature=self._property.temperature,
                top_p=self._property.top_p,
                max_tokens=self._property.max_output_token
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(
                f"\nContent Generate error: "
                f"\nLLM {self._property.name}@key: {client_name}"
                f"\nError: {traceback.format_exc()}"
            )
            raise e

    async def chat_stream(self, messages: List[Dict[str, str]]) -> AsyncGenerator[str, None]:
        client_info = self._get_client()
        client_name, client = client_info["name"], client_info["client"]

        try:
            for part in client.chat.completions.create(
                model=self._property.name,
                messages=messages,
                timeout=self._property.timeout,
                temperature=self._property.temperature,
                top_p=self._property.top_p,
                max_tokens=self._property.max_output_token,
                stream=True
            ):
                if part.choices:
                    content = part.choices[0].delta.content
                    if content:
                        yield content
        except Exception as e:
            logger.error(
                f"\nContent Generate Stream error: "
                f"\nLLM {self._property.name}@key: {client_name}"
                f"\nError: {traceback.format_exc()}"
            )
            raise e
        