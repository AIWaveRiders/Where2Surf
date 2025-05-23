import json
import os
import traceback
from typing import List, Sequence, Tuple

from autogen_agentchat.agents import BaseChatAgent
from autogen_agentchat.base import Response
from autogen_agentchat.messages import (
    BaseChatMessage,
    TextMessage,
)
from autogen_agentchat.utils import remove_images
from autogen_core import CancellationToken, Component, ComponentModel, FunctionCall
from autogen_core.models import (
    AssistantMessage,
    ChatCompletionClient,
    LLMMessage,
    SystemMessage,
    UserMessage,
)
from pydantic import BaseModel
from typing_extensions import Self

from autogen_ext.agents.file_surfer._markdown_file_browser import MarkdownFileBrowser

# from typing_extensions import Annotated
from autogen_ext.agents.file_surfer._tool_definitions import (
    TOOL_FIND_NEXT,
    TOOL_FIND_ON_PAGE_CTRL_F,
    TOOL_OPEN_PATH,
    TOOL_PAGE_DOWN,
    TOOL_PAGE_UP,
)

class CustomSurferConfig(BaseModel):
    """Configuration for FileSurfer agent"""

    name: str
    model_client: ComponentModel
    description: str | None = None

class CustomFileSurfer(BaseChatAgent, Component[CustomSurferConfig]):
    """An agent, used by MagenticOne, that acts as a local file previewer. FileSurfer can open and read a variety of common file types, and can navigate the local file hierarchy.

    Installation:

    .. code-block:: bash

        pip install "autogen-ext[file-surfer]"

    Args:
        name (str): The agent's name
        model_client (ChatCompletionClient): The model to use (must be tool-use enabled)
        description (str): The agent's description used by the team. Defaults to DEFAULT_DESCRIPTION
        base_path (str): The base path to use for the file browser. Defaults to the current working directory.

    """

    component_config_schema = CustomSurferConfig
    component_provider_override = "autogen_ext.agents.file_surfer.FileSurfer"

    DEFAULT_DESCRIPTION = "An agent that can handle local files."

    DEFAULT_SYSTEM_MESSAGES = [
        SystemMessage(
            content="""
        You are a helpful AI Assistant.
        When given a user query, use available functions to help the user with their request."""
        ),
    ]

    def __init__(
        self,
        name: str,
        model_client: ChatCompletionClient,
        description: str = DEFAULT_DESCRIPTION,
        base_path: str = os.getcwd(),
    ) -> None:
        super().__init__(name, description)
        self._model_client = model_client
        self._chat_history: List[LLMMessage] = []
        self._browser = MarkdownFileBrowser(viewport_size=1024 * 5, base_path=base_path)

    @property
    def produced_message_types(self) -> Sequence[type[BaseChatMessage]]:
        return (TextMessage,)


    async def on_messages(self, messages: Sequence[BaseChatMessage], cancellation_token: CancellationToken) -> Response:
        """YOUR CODE HERE: how to handle incoming messages
         This is the main entry point for the agent to process incoming messages.

        Args:
            messages (Sequence[BaseChatMessage]): The incoming chat messages.
            cancellation_token (CancellationToken): The cancellation token for the operation.

        Returns:
            Response: The response from processing the incoming messages.
        """
        for chat_message in messages:
            self._chat_history.append(chat_message.to_model_message())
        try:
            _, content = await self._generate_reply(cancellation_token=cancellation_token)
            self._chat_history.append(AssistantMessage(content=content, source=self.name))
            return Response(chat_message=TextMessage(content=content, source=self.name))

        except BaseException:
            content = f"File surfing error:\n\n{traceback.format_exc()}"
            self._chat_history.append(AssistantMessage(content=content, source=self.name))
            return Response(chat_message=TextMessage(content=content, source=self.name))



    async def on_reset(self, cancellation_token: CancellationToken) -> None:
        self._chat_history.clear()


    def _get_browser_state(self) -> Tuple[str, str]:
        """
        Get the current state of the browser, including the header and content.
        """
        header = f"Path: {self._browser.path}\n"

        if self._browser.page_title is not None:
            header += f"Title: {self._browser.page_title}\n"

        current_page = self._browser.viewport_current_page
        total_pages = len(self._browser.viewport_pages)
        header += f"Viewport position: Showing page {current_page+1} of {total_pages}.\n"

        return (header, self._browser.viewport)

    async def _generate_reply(self, cancellation_token: CancellationToken) -> Tuple[bool, str]:
        # TODO: write to redis
        history = self._chat_history[0:-1]
        last_message = self._chat_history[-1]
        assert isinstance(last_message, UserMessage)

        task_content = last_message.content  # the last message from the sender is the task

        assert self._browser is not None

        context_message = UserMessage(
            source="user",
            content=f"Your file viewer is currently open to the file or directory '{self._browser.page_title}' with path '{self._browser.path}'.",
        )

        task_message = UserMessage(
            source="user",
            content=task_content,
        )

        create_result = await self._model_client.create(
            messages=self._get_compatible_context(history + [context_message, task_message]),
            tools=[
                TOOL_OPEN_PATH,
                TOOL_PAGE_DOWN,
                TOOL_PAGE_UP,
                TOOL_FIND_NEXT,
                TOOL_FIND_ON_PAGE_CTRL_F,
            ],
            cancellation_token=cancellation_token,
        )

        response = create_result.content

        if isinstance(response, str):
            # Answer directly.
            return False, response

        elif isinstance(response, list) and all(isinstance(item, FunctionCall) for item in response):
            function_calls = response
            for function_call in function_calls:
                tool_name = function_call.name

                try:
                    arguments = json.loads(function_call.arguments)
                except json.JSONDecodeError as e:
                    error_str = f"File surfer encountered an error decoding JSON arguments: {e}"
                    return False, error_str

                if tool_name == "open_path":
                    path = arguments["path"]
                    self._browser.open_path(path)
                elif tool_name == "page_up":
                    self._browser.page_up()
                elif tool_name == "page_down":
                    self._browser.page_down()
                elif tool_name == "find_on_page_ctrl_f":
                    search_string = arguments["search_string"]
                    self._browser.find_on_page(search_string)
                elif tool_name == "find_next":
                    self._browser.find_next()
            header, content = self._get_browser_state()
            final_response = header.strip() + "\n=======================\n" + content
            return False, final_response

        final_response = "TERMINATE"
        return False, final_response

    def _get_compatible_context(self, messages: List[LLMMessage]) -> List[LLMMessage]:
        """Ensure that the messages are compatible with the underlying client, by removing images if needed."""
        if self._model_client.model_info["vision"]:
            return messages
        else:
            return remove_images(messages)


    def _to_config(self) -> CustomSurferConfig:
        """Only change CustomSurferConfig to your component config class 

        Returns:
            CustomSurferConfig: The configuration for the CustomSurfer component.
        """
        return CustomSurferConfig(
            name=self.name,
            model_client=self._model_client.dump_component(),
            description=self.description,
        )

    @classmethod
    def _from_config(cls, config: CustomSurferConfig) -> Self:
        """Create an instance of the class from a CustomSurferConfig. Only change CustomSurferConfig to your component config class 

        Args:
            config (CustomSurferConfig): The configuration for the CustomSurfer component.

        Returns:
            Self: An instance of the class.
        """
        return cls(
            name=config.name,
            model_client=ChatCompletionClient.load_component(config.model_client),
            description=config.description or cls.DEFAULT_DESCRIPTION,
        )