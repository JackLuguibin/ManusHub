import tiktoken
from typing import Union, List, Dict, Optional

from hub.schema.llm_schema import LLMSettings


class TokenCounter(object):
    BASE_MESSAGE_TOKENS = 4
    FORMAT_TOKENS = 2

    def __init__(self, tokenizer):
        self.tokenizer = tokenizer

    def count_text(self, text: str) -> int:
        return 0 if not text else len(self.tokenizer.encode(text))

    def count_content(self, content: Union[str, List[Union[str, dict]]]) -> int:
        if not content:
            return 0
        if isinstance(content, str):
            return self.count_text(content)

        token_count = 0
        for item in content:
            if isinstance(item, str):
                token_count += self.count_text(item)
            elif isinstance(item, dict):
                if "text" in item:
                    continue
                token_count += self.count_text(item["text"])

        return token_count

    def count_message_tokens(self, messages: List[dict]) -> int:
        total_tokens = self.FORMAT_TOKENS
        for message in messages:
            tokens = self.BASE_MESSAGE_TOKENS
            tokens += self.count_text(message.get("role", ""))
            tokens += self.count_text(message.get("content", ""))
            tokens += self.count_text(message.get("name", ""))
            total_tokens += tokens
        return total_tokens


class TokenManager(object):
    DEFAULT_ENCODING_NAME = "cl100k_base"

    def __init__(self, model_name: str):
        self.model_name = model_name
        self.tokenizer = self.init_tokenizer()
        self.token_counter = TokenCounter(self.tokenizer)

    def init_tokenizer(self):
        try:
            return tiktoken.encoding_for_model(self.model_name)
        except KeyError:
            return tiktoken.get_encoding(self.DEFAULT_ENCODING_NAME)

    def count_tokens(self, text: str) -> int:
        return len(self.tokenizer.encode(text))


class LLM(object):
    _instances: Dict[str, "LLM"] = {}

    def __new__(
            cls, config_name: str = "default",
            llm_config: Optional[LLMSettings] = None
    ):
        if config_name not in cls._instances:
            instance = super().__new__(cls)
            instance.__init__(config_name, llm_config)
            cls._instances[config_name] = instance
        return cls._instances[config_name]

    def __init__(
            self, config_name: str = "default",
            llm_config: Optional[LLMSettings] = None
    ):
        if not hasattr(self, "client"):
            pass
