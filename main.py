import asyncio
from autogen_agentchat.agents import UserProxyAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.ui import Console
from chatgroup import MagenticOneGroupChat

async def main() -> None:
    model_client = OpenAIChatCompletionClient(model="gpt-4o")

    user_proxy = UserProxyAgent(
        name="UserProxy",
        description="Human user who can provide additional information and feedback",
        input_func=input
    )

    team = MagenticOneGroupChat([user_proxy], model_client=model_client)
    await Console(team.run_stream(task="Where should I surf today?"))

asyncio.run(main())