from dotenv import load_dotenv
from langchain_mistralai import ChatMistralAI
from langchain.tools import tool
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.graph import StateGraph, START, END
from typing import Annotated
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage, HumanMessage

if load_dotenv():
    print("loaded ENV files successfully.")


class mainstate:
    messages: Annotated[list[BaseMessage], add_messages]


@tool
def Simple_calculator(expression) -> str:
    """
    This tool is used to perform math operations.
    """
    return eval(expression)


@tool
def weather_report(city: str) -> str:
    """
    This tool is to see the weather reports.
    """
    return "Sunny he weather in Surat"


model = ChatMistralAI(model="mistral-medium-latest")

tools = [Simple_calculator, weather_report]

tool_node = ToolNode(tools)

model_with_tools = model.bind_tools(tools)


def chat_node(state: mainstate) -> dict:
    messages = state["messages"]
    response = model_with_tools.invoke(messages)
    return {"messages": [response]}


graph = StateGraph(mainstate)

graph.add_node("chat_node", chat_node)
graph.add_node("tools", tool_node)

graph.add_edge(START, "chat_node")
graph.add_conditional_edges(
    "chat_node", tools_condition, {"tools": "tools", "__end__": END}
)
graph.add_edge("tools", "chat_node")


workflow = graph.compile()

initial_state = {"messages": [HumanMessage(content="subtract 10 out of 17")]}

output = workflow.invoke(initial_state)
print(output)
