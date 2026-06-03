import asyncio
from llama_index.llms.mistralai import MistralAI
from llama_index.core.agent.workflow import ReActAgent
from llama_index.core.tools import FunctionTool

import os
from dotenv import load_dotenv
import asyncio

load_dotenv()
api_key = os.getenv("MISTRAL_API_KEY")


def multiply(a: int, b: int) -> int:
    """Multiply two integers and returns the result integer"""
    return a * b


def add(a: int, b: int) -> int:
    """Add two integers and returns the result integer"""
    return a + b


add_tool = FunctionTool.from_defaults(fn=add)
multiply_tool = FunctionTool.from_defaults(fn=multiply)

llm = MistralAI(model="mistral-medium-latest", max_tokens=1000, api_key=api_key)

workflow = ReActAgent(
    tools=[add_tool, multiply_tool],
    llm=llm,
    system_prompt="you are a helpful assistant. use the tools you are provided to assist the user.",
)


async def main():
    response = await workflow.run(user_msg="what is 10 + 20 time 40.")
    return response


if __name__ == "__main__":
    response = asyncio.run(main())
    print(response)
