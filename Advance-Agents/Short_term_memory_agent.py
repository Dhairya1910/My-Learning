from langchain_core.outputs import chat_result
from langchain_core.outputs import chat_result
from langchain_core.outputs import chat_result
from langchain_core.outputs import chat_result
from langchain_core.outputs import chat_result
from langchain_core.outputs import chat_result
from langchain.agents import create_agent, AgentState
from pydantic import Field, HttpUrl
from typing import List
from langchain_mistralai import ChatMistralAI
from langgraph.checkpoint.memory import InMemorySaver
from langchain.tools import tool, ToolRuntime
from dotenv import load_dotenv
from fastapi import FastAPI

# app = FastAPI()


class data(AgentState):
    name: str
    age: int
    place: str


load_dotenv()


@tool(
    "readUserInfo",
    description="Use to read user personlized info such as location, name, age.",
)
def read_info(runtime: ToolRuntime):
    """
    Use to read user personlized info such as location, name, age.
    """
    name = runtime.state["name"]
    age = runtime.state["age"]
    place = runtime.state["place"]
    writer = runtime.stream_writer
    writer("reading location")
    writer("reading name")
    return f"this is user information that can help you personalize the user experience : name : {name}, age : {age}, place : {place}"


model = ChatMistralAI(name="mistral-small-2506", temperature=0.7)

agent = create_agent(
    model, state_schema=data, checkpointer=InMemorySaver(), tools=[read_info]
)

user_input = input("please ask you question : ")
while user_input != "Exit":
    result = agent.stream_events(
        {
            "messages": [{"role": "user", "content": user_input}],
            "name": "Dhairya",
            "age": 22,
            "place": "Surat",
        },
        {"configurable": {"thread_id": "1"}},
        version="v3",
    )

    for messages in result.messages:
        for delta in messages.text:
            print(delta, end="", flush=True)

    user_input = input("Human : ")


# @app.get("/")
# def call_agent(user_input: str):
#     result = agent.invoke(
#         {
#             "messages": [{"role": "user", "content": user_input}],
#             "name": "Dhairya",
#             "age": 22,
#             "place": "Surat",
#         },
#         {"configurable": {"thread_id": "1"}},
#     )

#     return result["messages"][-1].content
