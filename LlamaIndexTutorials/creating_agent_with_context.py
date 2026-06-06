import asyncio
import os
from dotenv import load_dotenv
from llama_index.core.agent.workflow import FunctionAgent
from llama_index.core.workflow import Context, JsonSerializer
from llama_index.llms.mistralai import MistralAI

load_dotenv()

api_key = os.getenv("MISTRAL_API_KEY")

llm = MistralAI(model="mistral-large-latest", max_tokens=5000, api_key=api_key)

workflow = FunctionAgent(
    llm=llm, system_prompt="You are an helpful agent.", streaming=False
)
ctx = Context(workflow)


async def chat(ctx, user_message=None):
    if user_message is None:
        user_message = input("Human : ")

    while user_message.strip().lower() != "exit":
        result = await workflow.run(user_msg=user_message, ctx=ctx)
        print("AI :", result)
        user_message = input("Human : ")

    ctx_dict = ctx.to_dict(JsonSerializer())
    return ctx_dict


async def main():

    print("--- Starting Session 1 (Type 'exit' to pause) ---")
    response = await chat(ctx=ctx)
    print("\n--- Restoring Session Context ---")
    restored_ctx = Context.from_dict(
        workflow, response, serializer=JsonSerializer()
    )

    user_input = input("Ask anything from previous talk: ")
    response2 = await chat(ctx=restored_ctx, user_message=user_input)
    print("\nFinal Context State Saved.")


if __name__ == "__main__":
    asyncio.run(main())