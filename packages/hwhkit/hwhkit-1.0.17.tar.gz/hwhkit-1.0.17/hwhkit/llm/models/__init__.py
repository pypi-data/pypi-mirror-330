import tiktoken
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, AsyncGenerator
from hwhkit.utils import logger


class ModelNotFoundError(Exception):
    def __init__(self, model_name: str):
        super().__init__(f"Model '{model_name}' not found in the model instances.")


class LanguageModelProperty:
    def __init__(
            self, name: str, short_name: str, company: str, max_input_token: int, max_output_token: int,
            top_p: Optional[float] = None, top_k: Optional[int] = None, temperature: Optional[float] = None,
            timeout: int = 120, input_token_fee_pm: float = 0.0, output_token_fee_pm: float = 0.0,
            train_token_fee_pm: float = 0.0, prompt_version: int = 1, keys: List[str] = None
    ):
        self.name = name
        self.short_name = short_name
        self.company = company
        self.max_input_token = max_input_token
        self.max_output_token = max_output_token
        self.top_p = top_p
        self.top_k = top_k
        self.temperature = temperature
        self.timeout = timeout
        self.input_token_fee_pm = input_token_fee_pm
        self.output_token_fee_pm = output_token_fee_pm
        self.train_token_fee_pm = train_token_fee_pm
        self.prompt_version = prompt_version


class ModelStrategy(ABC):

    @abstractmethod
    def base_url(self) -> str: pass

    @abstractmethod
    def get_name(self) -> str: pass

    @abstractmethod
    async def gen_messages(
            self, question: str, system_prompt: Optional[str] = None, history_messages: Optional[List[Dict]] = None
    ) -> List[Dict[str, str]]:
        pass

    @abstractmethod
    async def chat(self, messages: List[Dict[str, str]]) -> str:
        pass

    @abstractmethod
    async def chat_stream(self, messages: List[Dict[str, str]]) -> AsyncGenerator[str, None]:
        pass

    def calculate_token_count(self, text: str, encoding_name: str = "cl100k_base") -> int:
        encoding = tiktoken.get_encoding(encoding_name)
        return len(encoding.encode(text))

    def calculate_messages_token_count(self, messages: List[Dict[str, str]], encoding_name: str = "cl100k_base") -> int:
        total_tokens = 0
        for message in messages:
            content = f"role:{message['role']} content:{message['content']}"
            total_tokens += self.calculate_token_count(content, encoding_name)
        return total_tokens

    async def resized_messages(
            self, messages: List[Dict[str, str]], encoding_name: str = "cl100k_base"
    ) -> List[Dict[str, str]]:
        if not messages:
            return []

        max_token_count = self._property.max_input_token
        total_tokens = self.calculate_messages_token_count(messages, encoding_name)
        if total_tokens <= max_token_count:
            return messages

        while total_tokens > max_token_count and len(messages) > 1:
            removed_message = messages.pop(1)
            total_tokens = self.calculate_messages_token_count(messages, encoding_name)
            logger.info(f"Removed message due to token limit: {removed_message}")

        if total_tokens > max_token_count and len(messages) > 0:
            removed_message = messages.pop(0)
            total_tokens = self.calculate_messages_token_count(messages, encoding_name)
            logger.info(f"Removed system message due to token limit: {removed_message}")
        return messages


class LanguageModel:

    def __init__(self, strategy: ModelStrategy):
        self._strategy = strategy

    async def chat(
            self, question: str, system_prompt: Optional[str] = None, history_messages: Optional[List[Dict]] = None
    ) -> str:
        messages = await self._strategy.gen_messages(question, system_prompt, history_messages)
        messages = await self._strategy.resized_messages(messages)
        return await self._strategy.chat(messages)

    async def chat_stream(
            self, question: str, system_prompt: Optional[str] = None, history_messages: Optional[List[Dict]] = None
    ) -> AsyncGenerator[str, None]:
        messages = await self._strategy.gen_messages(question, system_prompt, history_messages)
        messages = await self._strategy.resized_messages(messages)
        async for chunk in self._strategy.chat_stream(messages):
            yield chunk

    async def gen_messages(
            self, question: str, system_prompt: Optional[str] = None, history_messages: Optional[List[Dict]] = None
    ) -> List[Dict[str, str]]:
        return await self._strategy.gen_messages(question, system_prompt, history_messages)

    async def chat_with_message(self,  messages: List[Dict[str, str]]) -> str:
        return await self._strategy.chat(messages)

    async def chat_stream_with_message(self, messages: List[Dict[str, str]]) -> AsyncGenerator[str, None]:
        async for chunk in self._strategy.chat_stream(messages):
            yield chunk


class LanguageModelFactory:
    _model_instances: Dict[str, LanguageModel] = {}

    @classmethod
    def register_model_instance(cls, name: str, model_instance: LanguageModel):
        cls._model_instances[name] = model_instance

    @classmethod
    def get_model_instance(cls, name: str) -> LanguageModel:
        model = cls._model_instances.get(name)
        if not model:
            logger.error(f"Model '{name}' not found in the model instances.")
            raise ModelNotFoundError(name)
        return model

    @classmethod
    def list_models(cls) -> List[str]:
        return list(cls._model_instances)

    @classmethod
    def all_models(cls) -> Dict[str, LanguageModel]:
        return cls._model_instances
