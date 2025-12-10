# llm_interface.py
from openai import OpenAI

class LLMInterface:
    def __init__(self, base_url: str, api_key: str = "EMPTY", model_name: str = "breeze-8b"):
        self.client = OpenAI(
            base_url=base_url,
            api_key=api_key
        )
        self.model_name = model_name

    def generate_response(self, messages: list, max_tokens: int = 1024, temperature: float = 0.1):
        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                max_tokens=max_tokens,
                temperature=temperature
            )
            return response.choices[0].message.content
        except Exception as e:
            raise RuntimeError(f"LLM 調用失敗: {e}")