from openai import OpenAI
from google import genai


class Client:
    def __init__(self, api_key, base_url, api_style):
        self.api_key = api_key
        self.base_url = base_url
        self.api_style = api_style
    
    def create(self, **kwargs):
        if self.api_style == "openai":
            self.model_client = OpenAI(
                api_key=self.api_key,
                base_url=self.base_url
            )
            return self.model_client.chat.completions.create(**kwargs)
        if self.api_style == "google":
            self.model_client = genai.Client(
                api_key = self.api_key
            )
            for i in kwargs:
                if i == "messages":
                    kwargs["content"] = kwargs["messages"]
                    del kwargs["messages"]
            return self.model_client.models.generate_content(**kwargs)
        