from dotenv import load_dotenv
from langchain_mistralai import ChatMistralAI
from langchain.tools import tool
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.graph import StateGraph, START, END
from typing import Annotated
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage, HumanMessage, ToolMessage
from langchain_mcp_adapters.client import MultiServerMCPClient

import asyncio
import json

if load_dotenv():
    print("loaded ENV files successfully.")


class mainstate:
    messages: Annotated[list[BaseMessage], add_messages]


model = ChatMistralAI(model="mistral-small-latest")


async def main():

    client = MultiServerMCPClient(
        {
            "math": {
                "transport": "stdio",
                "command": "python",
                "args": ["Langgraph/MCP/math_server.py"],
            }
        }
    )

    tools = await client.get_tools()
    tool_node = ToolNode(tools)
    model_with_tools = model.bind_tools(tools)

    async def chat_node(state: mainstate) -> dict:
        messages = state["messages"]

        cleaned_messages = []
        for msg in messages:
            if isinstance(msg, ToolMessage):
                if isinstance(msg.content, list):
                    text_content = ""
                    for block in msg.content:
                        if isinstance(block, dict) and "text" in block:
                            text_content += block["text"]
                        elif isinstance(block, str):
                            text_content += block
                    cleaned_messages.append(
                        ToolMessage(content=text_content, tool_call_id=msg.tool_call_id)
                    )
                else:
                    cleaned_messages.append(msg)
            else:
                cleaned_messages.append(msg)

        response = await model_with_tools.ainvoke(cleaned_messages)
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

    initial_state = {"messages": [HumanMessage(content="what is 100 + 50")]}

    output = await workflow.ainvoke(initial_state)
    return output


if __name__ == "__main__":
    output = asyncio.run(main())
    print(output)
