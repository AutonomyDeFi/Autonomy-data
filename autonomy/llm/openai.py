import os
import openai
import autonomy as a
from typing import *


class OpenAI(a.Block):
    def init(self, api_key: str = 'OPENAI_API_KEY', api_base = "https://openrouter.ai/api/v1"):
        openai.api_base = api_base
        from dotenv import load_dotenv
        self.set_api_key(api_key)

    def set_api_key(self, api_key: str):
        api_key = os.getenv(api_key, api_key)
        self.api_key = api_key
        openai.api_key = api_key

    models = [
        'gpt-3.5-turbo'
        'gpt-3.5-turbo-0301'
        'gpt-3.5-turbo-0613'
        'gpt-3.5-turbo-16k'
        'gpt-3.5-turbo-16k-0613'
        'gpt-3.5-turbo-instruct'
        'gpt-3.5-turbo-instruct-0914'
    ]

    def chat(self, prompt: str = "Say this is a test",
              model = 'gpt-3.5-turbo-instruct', 
              max_tokens: int = 5, 
              temperature: float = 0.5) -> str:
            import random
            if not model:
                model = random.choice(self.models)
            
            params = {'max_tokens': max_tokens, 'temperature': temperature}
            try:
                response = openai.ChatCompletion.create(
                model=model, # Optional (user controls the default)
                messages=[{'role': 'user', 'content': prompt}],
                **params
                )
                return response.choices[0].message['content']
            except Exception as e:
                 response = openai.Completion.create( model= model, **params)
                 return response.choices[0].text
    def embed(self, input: Union[List[str],str] = "Say this is a test",
            model = 'text-embedding-ada-002', 
            max_tokens: int = 5, 
            temperature: float = 0.5) -> str:
        import random
        if not model:
            model = random.choice(self.models)
        
        params = {'max_tokens': max_tokens, 'temperature': temperature}
        response = openai.Embedding.create(
        model=model, # Optional (user controls the default)
        input=input,
        **params
        )
        response =  [r['embedding'] for r in response['data']]
        if isinstance(input, str):
            return response[0]
        return response



    @classmethod
    def test(cls):
        print("Testing OpenAI")
        self = cls()
        print(self.chat())
        input = ['hello', 'world']
        embeddings = self.embed(input)
        assert len(embeddings) == len(input)
        input = 'hello world'
        embeddings = self.embed(input)
        return {'status': 'success'}
    
