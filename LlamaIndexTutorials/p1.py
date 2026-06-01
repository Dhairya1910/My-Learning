import os
from dotenv import load_dotenv

from llama_index.llms.mistralai import MistralAI
from llama_index.core.llms import ChatMessage

load_dotenv()

api_key = os.getenv("MISTRAL_API_KEY")


llm = MistralAI(model="mistral-small-latest", api_key=api_key)

messages = [
    ChatMessage(role="system", content="You are a helpful assistant."),
    ChatMessage(role="user", content="Tell me a joke."),
]
chat_response = llm.stream_chat(messages)
for token in chat_response:
    print(token.delta, end="", flush=True)
