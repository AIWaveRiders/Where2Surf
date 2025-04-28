import asyncio
from custom_agent import CustomFileSurfer
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.ui import Console
from custom_chatgroup import MagenticOneGroupChat

async def main() -> None:
    model_client = OpenAIChatCompletionClient(model="gpt-4o")
    # Note: you can also use  other agents in the team
    file_surfer = CustomFileSurfer( "FileSurfer",model_client=model_client)
    team = MagenticOneGroupChat([file_surfer], model_client=model_client)
    await Console(team.run_stream(task="What is the UV index in Melbourne today?"))

asyncio.run(main())