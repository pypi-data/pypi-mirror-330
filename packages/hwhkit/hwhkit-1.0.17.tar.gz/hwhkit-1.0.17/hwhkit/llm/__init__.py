from hwhkit.llm.config import load_models_from_yaml, load_models_from_dict

class LLMClient:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, config_file="llm_config.yaml", keys_file="llm_keys.yaml", config_dict: dict = None):
        if not hasattr(self, 'models'):
            if config_dict:
                self.models = load_models_from_dict(config_dict=config_dict)
            else:
                self.config_file = config_file
                self.keys_file = keys_file
                self.models = load_models_from_yaml(config_file=self.config_file, keys_file=self.keys_file)

    def list_models(self):
        if self.models is None:
            raise ValueError("Models failed to load.")
        return self.models.list_models()

    async def chat(self, model_name, prompt, system_prompt=""):
        if self.models is None:
            raise ValueError("Models failed to load.")
        return await self.models.get_model_instance(model_name).chat(prompt, system_prompt=system_prompt)

    async def chat_stream(self, model_name, prompt, system_prompt=""):
        if self.models is None:
            raise ValueError("Models failed to load.")
        async for chunk in self.models.get_model_instance(model_name).chat_stream(prompt, system_prompt=system_prompt):
            yield chunk

