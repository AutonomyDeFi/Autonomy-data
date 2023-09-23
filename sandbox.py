from litellm import completion
import os

## set ENV variables
os.environ["OPENAI_API_KEY"] = "sk-litellm-7_NPZhMGxY2GoHC59LgbDw" # [OPTIONAL] replace with your openai key
os.environ["COHERE_API_KEY"] = "sk-litellm-7_NPZhMGxY2GoHC59LgbDw" # [OPTIONAL] replace with your cohere key

messages = [{ "content": "Hello, how are you?","role": "user"}]

# openai call
response = completion(model="gpt-3.5-turbo", messages=messages)

# cohere call
response = completion("command-nightly", messages)
print(response)