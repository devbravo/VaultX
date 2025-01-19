"""Define a custom Reasoning and Action agent.

Works with a chat model with tool calling support.
"""

from datetime import datetime, timezone
from typing import Dict, List, Literal, cast

import httpx
from langchain_core.messages import AIMessage, HumanMessage, RemoveMessage
from langchain_core.runnables import RunnableConfig
from langgraph.checkpoint.memory import MemorySaver
from langgraph.constants import START
from langgraph.graph import StateGraph

from react_agent.configuration import Configuration
from react_agent.models.pii import Encrypted, Decrypted, PlaceHolder
from react_agent.state import InputState, State
from react_agent.tools import TOOLS
from react_agent.utils import load_chat_model


# Define the function that calls the model
def summarize_conversation(state):
    # First, we summarize the conversation
    summary = state.summary if state.summary else ""
    if summary:
        # If a summary already exists, we use a different system prompt
        # to summarize it than if one didn't
        summary_message = (
            f"This is summary of the conversation to date: {summary}\n\n"
            "Extend the summary by taking into account the new messages above:"
            "add all the PII available below to the summary "
            "add all the encrypted PII available"
            "never store any actual PII in the summary"
            "the pii is encrypted"
            "and will be used for decryption later"
            "PII: [phone-number]"
            f"{state.encrypted_pii.encrypted_pii}"
        )
    else:
        summary_message = (
            "Create a summary of the conversation above:"
            "add all the encrypted PII available"
            "never store any actual PII in the summary"
            " below to the summary the pii is encrypted"
            "and will be used for decryption later"
            "PII: [phone-number]"
            f"{state.encrypted_pii.encrypted_pii}"
        )

    messages = state.messages + [HumanMessage(content=summary_message)]
    llm = load_chat_model("openai/gpt-4o-mini")
    response = llm.invoke(messages)
    # We now need to delete messages that we no longer want to show up
    # I will delete all but the last two messages, but you can change this
    delete_messages = [RemoveMessage(id=m.id) for m in state.messages[:-2]]
    return {"summary": response.content, "messages": delete_messages}


async def encrypt(state):
    async with httpx.AsyncClient() as client:
        message = state.messages[-1].content
        data = {"text": message}
        print(data)
        response = await client.post("http://localhost:8000/encrypt/", json=data)
        encrypted: Encrypted = Encrypted.parse_obj(response.json())

    return {
        "record_id": encrypted.record_id if not None else encrypted.record_id,
        "encrypted_pii": encrypted,
        "message": encrypted.processed_text if encrypted.processed_text else message,
    }


async def decrypt(state):
    message = state.messages[-1].content
    if state.encrypted_pii:
        async with httpx.AsyncClient() as client:
            data = {"record_id": state.record_id, "text": message}
            response = await client.post("http://localhost:8000/decrypt/", json=data)
            decrypted: Decrypted = Decrypted.parse_obj(response.json())

    return {"decrypted_pii": decrypted}


async def call_model(
        state: State, config: RunnableConfig
) -> Dict[str, List[AIMessage]]:
    """Call the LLM powering our "agent".

    This function prepares the prompt, initializes the model, and processes the response.

    Args:
        state (State): The current state of the conversation.
        config (RunnableConfig): Configuration for the model run.

    Returns:
        dict: A dictionary containing the model's response message.
    """
    configuration = Configuration.from_runnable_config(config)

    # Initialize the model with tool binding. Change the model or add more tools here.
    model = load_chat_model(configuration.model).bind_tools(TOOLS)

    # Format the system prompt. Customize this to change the agent's behavior.
    system_message = configuration.system_prompt.format(
        system_time=datetime.now(tz=timezone.utc).isoformat()
    )

    # Get the model's response
    response = cast(
        AIMessage,
        await model.ainvoke(
            [
                {"role": "system", "content": system_message},
                {"role": "ai", "content": state.summary},
                {"role": "human", "content": state.message}], config
        ),
    )

    # Handle the case when it's the last step and the model still wants to use a tool
    if state.is_last_step and response.tool_calls:
        return {
            "messages": [
                AIMessage(
                    id=response.id,
                    content="Sorry, I could not find an answer to your question in the specified number of steps.",
                )
            ]
        }

    # Return the model's response as a list to be added to existing messages
    return {"messages": [response]}


def route_model_output(state: State) -> Literal["__end__", "decrypt"]:
    """Determine the next node based on the model's output.

    This function checks if the model's last message contains tool calls.

    Args:
        state (State): The current state of the conversation.

    Returns:
        str: The name of the next node to call ("__end__" or "decrypt").
    """

    last_message = state.messages[-1]

    if not isinstance(last_message, AIMessage):
        raise ValueError(
            f"Expected AIMessage in output edges, but got {type(last_message).__name__}"
        )

    for key, value in vars(PlaceHolder).items():
        if not key.startswith('__'):
            if value in last_message.content:
                return "decrypt"

    return "__end__"


# Define a new graph

builder = StateGraph(State, input=InputState, config_schema=Configuration)

# Define the two nodes we will cycle between
builder.add_node(call_model)
builder.add_node("summarize", summarize_conversation)
builder.add_node("encrypt", encrypt)
builder.add_node("decrypt", decrypt)

# Set the entrypoint as `call_model`
# This means that this node is the first one called
builder.add_edge(START, "encrypt")
builder.add_edge("encrypt", "call_model")
builder.add_conditional_edges("call_model", route_model_output)
builder.add_edge("call_model", "summarize")

# Compile the builder into an executable graph
# You can customize this by adding interrupt points for state updates
graph = builder.compile(
    interrupt_before=[],  # Add node names here to update state before they're called
    interrupt_after=[],
    checkpointer=MemorySaver()  # Add node names here to update state after they're called
)
graph.name = "VaultX Agent"  # This customizes the name in LangSmith
