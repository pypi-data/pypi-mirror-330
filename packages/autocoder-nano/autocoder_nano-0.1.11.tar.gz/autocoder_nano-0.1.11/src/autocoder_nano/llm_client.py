from loguru import logger
from openai import OpenAI, Stream
from openai.types.chat import ChatCompletionChunk, ChatCompletion

from autocoder_nano.llm_types import LLMRequest, LLMResponse


class AutoLLM:
    def __init__(self):
        self.default_model_name = None
        self.sub_clients = {}

    def setup_sub_client(self, client_name: str, api_key: str, base_url: str, model_name=""):
        self.sub_clients[client_name] = {
            "client": OpenAI(api_key=api_key, base_url=base_url),
            "model_name": model_name
        }
        return self

    def remove_sub_client(self, client_name: str):
        if client_name in self.sub_clients:
            del self.sub_clients[client_name]

    def get_sub_client(self, client_name: str):
        return self.sub_clients.get(client_name, None)

    def setup_default_model_name(self, model_name: str):
        self.default_model_name = model_name

    def stream_chat_ai(self, conversations, model=None) -> Stream[ChatCompletionChunk]:
        if not model and not self.default_model_name:
            raise Exception("model name is required")

        if not model:
            model = self.default_model_name

        model_name = self.sub_clients[model]["model_name"]
        logger.info(f"正在使用 {model} 模型, 模型名称 {model_name}")
        request = LLMRequest(
            model=model_name,
            messages=conversations
        )
        res = self._query(model, request, stream=True)
        return res

    def chat_ai(self, conversations, model=None) -> LLMResponse:
        # conversations = [{"role": "user", "content": prompt_str}]  deepseek-chat
        if not model and not self.default_model_name:
            raise Exception("model name is required")

        if not model:
            model = self.default_model_name

        if isinstance(conversations, str):
            conversations = [{"role": "user", "content": conversations}]

        model_name = self.sub_clients[model]["model_name"]
        logger.info(f"正在使用 {model} 模型, 模型名称 {model_name}")
        request = LLMRequest(
            model=model_name,
            messages=conversations
        )

        res = self._query(model, request)
        return LLMResponse(
            output=res.choices[0].message.content,
            input="",
            metadata={
                "id": res.id,
                "model": res.model,
                "created": res.created
            }
        )

    def _query(self, model_name: str, request: LLMRequest, stream=False) -> ChatCompletion | Stream[ChatCompletionChunk]:
        """ 与 LLM 交互 """
        response = self.sub_clients[model_name]["client"].chat.completions.create(
            model=request.model,
            messages=request.messages,
            stream=stream,
            max_tokens=request.max_tokens,
            temperature=request.temperature,
            top_p=request.top_p,
            n=request.n,
            stop=request.stop,
            presence_penalty=request.presence_penalty,
            frequency_penalty=request.frequency_penalty,
        )
        return response