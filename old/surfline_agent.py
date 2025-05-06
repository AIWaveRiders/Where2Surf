import os
import json
import traceback
from typing import List, Sequence, Tuple

from autogen_agentchat.agents import BaseChatAgent
from autogen_agentchat.base import Response
from autogen_agentchat.messages import BaseChatMessage, TextMessage
from autogen_core import CancellationToken, Component, ComponentModel
from autogen_core.models import AssistantMessage, ChatCompletionClient, LLMMessage, SystemMessage, UserMessage
from pydantic import BaseModel
from typing_extensions import Self


class SurflineAgentConfig(BaseModel):
    """Configuration for the custom agent."""
    name: str
    model_client: ComponentModel
    description: str | None = None


class SurflineAgent(BaseChatAgent, Component[SurflineAgentConfig]):
    """A custom agent that queries surfline.com for up-to-date surf conditions and recommendations."""

    component_config_schema = SurflineAgentConfig
    DEFAULT_DESCRIPTION = "A custom agent that queries surfline.com for up-to-date surf conditions and recommendations."

    def __init__(
        self,
        name: str,
        model_client: ChatCompletionClient,
        description: str = DEFAULT_DESCRIPTION,
    ) -> None:
        super().__init__(name, description)
        self._model_client = model_client
        self._chat_history: List[LLMMessage] = []

    @property
    def produced_message_types(self) -> Sequence[type[BaseChatMessage]]:
        """Define the types of messages this agent can produce."""
        return (TextMessage,)

    async def on_messages(self, messages: Sequence[BaseChatMessage], cancellation_token: CancellationToken) -> Response:
        """
        Handle incoming messages.

        Args:
            messages (Sequence[BaseChatMessage]): The incoming chat messages.
            cancellation_token (CancellationToken): The cancellation token for the operation.

        Returns:
            Response: The response from processing the incoming messages.
        """
        # Add incoming messages to chat history
        for chat_message in messages:
            self._chat_history.append(chat_message.to_model_message())

        try:
            # Generate a reply (custom logic can be added here)
            _, content = await self._generate_reply(cancellation_token=cancellation_token)
            self._chat_history.append(AssistantMessage(content=content, source=self.name))
            return Response(chat_message=TextMessage(content=content, source=self.name))

        except Exception:
            # Handle errors gracefully
            content = f"Error:\n\n{traceback.format_exc()}"
            self._chat_history.append(AssistantMessage(content=content, source=self.name))
            return Response(chat_message=TextMessage(content=content, source=self.name))

    async def on_reset(self, cancellation_token: CancellationToken) -> None:
        """
        Reset the agent's state.

        Args:
            cancellation_token (CancellationToken): The cancellation token for the operation.
        """
        self._chat_history.clear()

    async def _generate_reply(self, cancellation_token: CancellationToken) -> Tuple[bool, str]:
        """
        Generate a reply to the user's query.

        Args:
            cancellation_token (CancellationToken): The cancellation token for the operation.

        Returns:
            Tuple[bool, str]: A tuple indicating whether the response is final and the response content.
        """
        # Example: Use the last message as the task
        last_message = self._chat_history[-1]
        assert isinstance(last_message, UserMessage)

        task_content = last_message.content  # The last message from the user is the task

        # Custom logic for generating a reply can be added here
        response = f"Received your message: {task_content}"
        return False, response

    def _get_compatible_context(self, messages: List[LLMMessage]) -> List[LLMMessage]:
        """
        Ensure that the messages are compatible with the underlying client.

        Args:
            messages (List[LLMMessage]): The list of messages.

        Returns:
            List[LLMMessage]: The filtered list of messages.
        """
        # Example: Remove images if the model doesn't support vision
        if self._model_client.model_info.get("vision", False):
            return messages
        else:
            return [msg for msg in messages if not isinstance(msg, AssistantMessage) or "image" not in msg.content]

    def _to_config(self) -> SurflineAgentConfig:
        """
        Convert the agent to its configuration.

        Returns:
            SurflineAgentConfig: The configuration for the agent.
        """
        return SurflineAgentConfig(
            name=self.name,
            model_client=self._model_client.dump_component(),
            description=self.description,
        )

    @classmethod
    def _from_config(cls, config: SurflineAgentConfig) -> Self:
        """
        Create an instance of the agent from its configuration.

        Args:
            config (SurflineAgentConfig): The configuration for the agent.

        Returns:
            Self: An instance of the agent.
        """
        return cls(
            name=config.name,
            model_client=ChatCompletionClient.load_component(config.model_client),
            description=config.description or cls.DEFAULT_DESCRIPTION,
        )