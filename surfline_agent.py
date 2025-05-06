from typing import Sequence
from pydantic import BaseModel
from autogen_agentchat.agents import BaseChatAgent
from autogen_agentchat.base import Response
from autogen_agentchat.messages import BaseChatMessage, TextMessage
from autogen_core import CancellationToken
from autogen_core.tools import BaseTool

# Tool Argument and Return Types
class SurflineQueryArgs(BaseModel):
    query: str  # The query to send to Surfline (e.g., location or surf conditions)

class SurflineQueryReturn(BaseModel):
    success: bool
    message: str  # The response message
    data: dict | None = None  # Optional: Store additional data from Surfline

# SurflineQuery Tool
class SurflineQueryTool(BaseTool[SurflineQueryArgs, SurflineQueryReturn]):
    def __init__(self):
        super().__init__(
            args_type=SurflineQueryArgs,
            return_type=SurflineQueryReturn,
            name="SurflineQuery",
            description="Queries Surfline for surf conditions or recommendations."
        )

    async def run(self, args: SurflineQueryArgs, cancellation_token: CancellationToken = None) -> SurflineQueryReturn:
        """
        Queries Surfline for surf conditions or recommendations.

        Args:
            args (SurflineQueryArgs): The query arguments.
            cancellation_token (CancellationToken): The cancellation token for the operation.

        Returns:
            SurflineQueryReturn: The result of the query.
        """
        # Placeholder for custom logic to query Surfline
        # Replace this with actual API calls or scraping logic
        query = args.query
        print(f"[DEBUG] Querying Surfline with: {query}")

        # Simulate a successful response
        response_data = {
            "location": "San Diego",
            "wave_height": "3-4 ft",
            "wind": "Light offshore",
            "water_temp": "58°F"
        }

        return SurflineQueryReturn(
            success=True,
            message=f"Surf conditions for {query}: {response_data}",
            data=response_data
        )

# Surfline Agent
class SurflineAgent(BaseChatAgent):
    def __init__(self, name: str):
        super().__init__(name, "An agent that queries Surfline for surf conditions and recommendations.")
        self.tools = [SurflineQueryTool()]

    @property
    def produced_message_types(self) -> Sequence[type[BaseChatMessage]]:
        return (TextMessage,)

    async def on_messages(self, messages: Sequence[BaseChatMessage], cancellation_token: CancellationToken) -> Response:
        """
        Handle incoming messages and query Surfline.

        Args:
            messages (Sequence[BaseChatMessage]): The incoming chat messages.
            cancellation_token (CancellationToken): The cancellation token for the operation.

        Returns:
            Response: The response from the Surfline query.
        """
        last_message = messages[-1].content
        print(f"[DEBUG] Received message: {last_message}")

        # Always invoke the Surfline query tool
        query_tool: SurflineQueryTool = self.tools[0]
        result_obj = await query_tool.run(SurflineQueryArgs(query=last_message), cancellation_token)
        reply = result_obj.message

        return Response(chat_message=TextMessage(content=reply, source=self.name))

    async def on_reset(self, cancellation_token: CancellationToken) -> None:
        """
        Reset the agent's state.

        Args:
            cancellation_token (CancellationToken): The cancellation token for the operation.
        """
        print("[DEBUG] Resetting SurflineAgent state.")