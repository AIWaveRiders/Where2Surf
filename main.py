#!/usr/bin/env python3
"""
Where2Surf LLM Orchestrator using MagenticOneGroupChat
Helps users find the best surf spots and provides real-time surf-related assistance.
"""

import asyncio
from autogen_agentchat.ui import Console
from autogen_agentchat.conditions import TextMentionTermination
from autogen_agentchat.teams import MagenticOneGroupChat
from autogen_agentchat.agents import UserProxyAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from surfline_agent import SurflineAgent  # Import SurflineAgent

async def main() -> None:
    # Initialize the model client
    model_client = OpenAIChatCompletionClient(model="gpt-4o")

    # Initialize the UserProxyAgent
    user_proxy = UserProxyAgent(
        name="UserProxy",
        description="Human user who can provide additional information and feedback",
        input_func=input
    )

    # Initialize the SurflineAgent
    surfline_agent = SurflineAgent(
        name="SurflineAgent"
    )

    # Create the team with all agents
    team = MagenticOneGroupChat(
        participants=[user_proxy, surfline_agent],
        model_client=model_client,
        termination_condition=TextMentionTermination("TERMINATE"),
    )

    # Task to activate the SurflineAgent
    task_text = (
        "Ask the user where they are and what surf-related information they need. "
        "Use the SurflineAgent to provide surf conditions or recommendations."
    )

    # Stream the conversation
    stream = team.run_stream(task=task_text)
    await Console(stream)

if __name__ == "__main__":
    asyncio.run(main())
