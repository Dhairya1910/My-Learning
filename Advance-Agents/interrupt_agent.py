from langchain_core.runnables import graph_png
from typing import Optional
import uuid
from langgraph.checkpoint.memory import InMemorySaver
from langchain_mistralai import ChatMistralAI
from langgraph.types import interrupt, Command
from langgraph.graph import StateGraph, START, END
from pydantic import BaseModel, Field
from dotenv import load_dotenv

load_dotenv()
model = ChatMistralAI(model="mistral-small-latest")


class Dataclass(BaseModel):
    title: str = Field(description="Name of the topic")
    content_draft: Optional[str] = None
    final_draft: Optional[str] = None
    approved: Optional[bool] = False


# defining nodes
def generate_content(state: Dataclass) -> dict:
    user_input = state.title
    prompt = f"""
    You are an expert content writer your job is to write 150 words paragraph for provided topic
    topic : {user_input}
    """
    response = model.invoke(prompt).content

    return {"content_draft": response}


def check_content(state: Dataclass):
    print("-" * 50)
    user_response = interrupt(
        {"message": "Please review....", "Content": state.content_draft}
    )

    if user_response.get("action") == "approved":
        return {"approved": True}
    else:
        return {"approved": False}


def publish(state: Dataclass):
    if state.approved:
        return {"final_draft": state.content_draft}
    else:
        return {"final_draft": "User denied"}


workflow = StateGraph(Dataclass)
workflow.add_node("generate_content", generate_content)
workflow.add_node("check_content", check_content)
workflow.add_node("publish", publish)

workflow.add_edge(START, "generate_content")
workflow.add_edge("generate_content", "check_content")
workflow.add_edge("check_content", "publish")
workflow.add_edge("publish", END)

checkpointer = InMemorySaver()
graph = workflow.compile(checkpointer=checkpointer)


if __name__ == "__main__":
    config = {"configurable": {"thread_id": "1"}}
    inital_state = {"title": "Rohit Sharma"}
    output = graph.invoke(inital_state, config=config)
    checkpoints = graph.get_state(config)
    for task in checkpoints.tasks:
        for intr in task.interrupts:
            print(intr.value)
    user_input = input("Reject or Approve : ")
    output = graph.invoke(Command(resume={"action": user_input}), config)
    print(output["final_draft"])
