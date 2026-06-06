from llama_index.llms.mistralai import MistralAI
from llama_index.core.workflow import Context
from llama_index.core.agent.workflow import FunctionAgent
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("MISTRAL_API_KEY")

llm = MistralAI(model="mistral-large-latest", max_tokens=5000, api_key=api_key)

workflow = FunctionAgent(
    llm=llm, system_prompt="You are an helpful agent.", streaming=False
)
ctx = Context(workflow)

async def chat():
    user_message = input("Human : ")

    while user_message.strip().lower() != "exit":
        result = await workflow.run(user_msg=user_message, ctx=ctx)
        print("AI :", result)
        user_message = input("Human : ")

    return 0

if __name__ == "__main__":
    response = asyncio.run(chat())
    if response == 0:
        print("AI : Thanks")
