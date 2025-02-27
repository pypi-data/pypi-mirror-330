
import yaml
from typing import Type

from hwhkit.llm.models import LanguageModelFactory, LanguageModelProperty, LanguageModel
from hwhkit.llm.models.alibaba import AlibabaStrategy
from hwhkit.llm.models.anthropic import AnthropicStrategy
from hwhkit.llm.models.deepseek import DeepSeekStrategy
from hwhkit.llm.models.lingyi import LingYiStrategy
from hwhkit.llm.models.moonshot import MoonshotStrategy
from hwhkit.llm.models.nvidia import NvidiaStrategy
from hwhkit.llm.models.openai import OpenaiStrategy
from hwhkit.llm.models.siliconflow import SiliconFlowStrategy
from hwhkit.llm.models.zhipu import ZhipuStrategy

provider_map = {
    "alibaba": AlibabaStrategy,
    "anthropic": AnthropicStrategy,
    "deepseek": DeepSeekStrategy,
    "lingyi": LingYiStrategy,
    "moonshot": MoonshotStrategy,
    "nvidia": NvidiaStrategy,
    "openai": OpenaiStrategy,
    "siliconflow": SiliconFlowStrategy,
    "zhipu": ZhipuStrategy,
}


def load_models_from_yaml(
        config_file: str = 'llm_config.yaml', keys_file: str = "llm_key.yaml"
) -> Type[LanguageModelFactory]:
    with open(config_file, "r") as f:
        config = yaml.safe_load(f)

    with open(keys_file, "r") as f:
        keys = yaml.safe_load(f).get("keys", {})

    models_config = config.get("models", {})
    for provider, provider_config in models_config.items():
        for model_name, model_config in provider_config.items():
            model_keys = {}
            for key_config in model_config.get("keys", []):
                key_name = key_config["name"]
                if key_name in keys:
                    model_keys[key_name] = keys[key_name]

            provider_strategy = provider_map.get(provider)
            if provider_strategy:
                model = LanguageModel(provider_strategy(model_keys, LanguageModelProperty(**model_config)))
                LanguageModelFactory.register_model_instance(model_name, model)

    return LanguageModelFactory


def load_models_from_dict(config_dict: dict) -> Type[LanguageModelFactory]:
    models_config = config_dict.get("models", {})
    for provider, provider_config in models_config.items():
        for model_name, model_config in provider_config.items():
            model_keys = {}
            for index, key_config in enumerate(model_config.get("keys", [])):
                model_keys[f"k_{index}"] = key_config["key"]

            provider_strategy = provider_map.get(provider)
            if provider_strategy:
                model = LanguageModel(provider_strategy(model_keys, LanguageModelProperty(**model_config)))
                LanguageModelFactory.register_model_instance(model_name, model)
    return LanguageModelFactory