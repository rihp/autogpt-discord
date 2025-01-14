"""This is a template for Auto-GPT plugins."""
import abc
from typing import Any, Dict, List, Optional, Tuple, TypeVar, TypedDict

from abstract_singleton import AbstractSingleton, Singleton

PromptGenerator = TypeVar("PromptGenerator")


class Message(TypedDict):
    role: str
    content: str


class AutoGPTPluginTemplate(AbstractSingleton, metaclass=Singleton):
    """
    This is a template for Auto-GPT plugins.
    """

    def __init__(self):
        super().__init__()
        self._name = "Auto-GPT-Plugin-Template"
        self._version = "0.1.0"
        self._description = "This is a template for Auto-GPT plugins."

    @abc.abstractmethod
    def can_handle_on_response(self) -> bool:
        """This method is called to check that the plugin can
        handle the on_response method.

        Returns:
            bool: True if the plugin can handle the on_response method."""
        return False

    @abc.abstractmethod
    def on_response(self, response: str, *args, **kwargs) -> str:
        """This method is called when a response is received from the model."""
        pass

    @abc.abstractmethod
    def can_handle_post_prompt(self) -> bool:
        """This method is called to check that the plugin can
        handle the post_prompt method.

        Returns:
            bool: True if the plugin can handle the post_prompt method."""
        return False

    @abc.abstractmethod
    def post_prompt(self, prompt: PromptGenerator) -> PromptGenerator:
        """This method is called just after the generate_prompt is called,
            but actually before the prompt is generated.

        Args:
            prompt (PromptGenerator): The prompt generator.

        Returns:
            PromptGenerator: The prompt generator.
        """
        pass

    @abc.abstractmethod
    def can_handle_on_planning(self) -> bool:
        """This method is called to check that the plugin can
        handle the on_planning method.

        Returns:
            bool: True if the plugin can handle the on_planning method."""
        return False

    @abc.abstractmethod
    def on_planning(
        self, prompt: PromptGenerator, messages: List[Message]
    ) -> Optional[str]:
        """This method is called before the planning chat completion is done.

        Args:
            prompt (PromptGenerator): The prompt generator.
            messages (List[str]): The list of messages.
        """
        pass

    @abc.abstractmethod
    def can_handle_post_planning(self) -> bool:
        """This method is called to check that the plugin can
        handle the post_planning method.

        Returns:
            bool: True if the plugin can handle the post_planning method."""
        return False

    @abc.abstractmethod
    def post_planning(self, response: str) -> str:
        """This method is called after the planning chat completion is done.

        Args:
            response (str): The response.

        Returns:
            str: The resulting response.
        """
        pass

    @abc.abstractmethod
    def can_handle_pre_instruction(self) -> bool:
        """This method is called to check that the plugin can
        handle the pre_instruction method.

        Returns:
            bool: True if the plugin can handle the pre_instruction method."""
        return False

    @abc.abstractmethod
    def pre_instruction(self, messages: List[Message]) -> List[Message]:
        """This method is called before the instruction chat is done.

        Args:
            messages (List[Message]): The list of context messages.

        Returns:
            List[Message]: The resulting list of messages.
        """
        pass

    @abc.abstractmethod
    def can_handle_on_instruction(self) -> bool:
        """This method is called to check that the plugin can
        handle the on_instruction method.

        Returns:
            bool: True if the plugin can handle the on_instruction method."""
        return False

    @abc.abstractmethod
    def on_instruction(self, messages: List[Message]) -> Optional[str]:
        """This method is called when the instruction chat is done.

        Args:
            messages (List[Message]): The list of context messages.

        Returns:
            Optional[str]: The resulting message.
        """
        pass

    @abc.abstractmethod
    def can_handle_post_instruction(self) -> bool:
        """This method is called to check that the plugin can
        handle the post_instruction method.

        Returns:
            bool: True if the plugin can handle the post_instruction method."""
        return False

    @abc.abstractmethod
    def post_instruction(self, response: str) -> str:
        """This method is called after the instruction chat is done.

        Args:
            response (str): The response.

        Returns:
            str: The resulting response.
        """
        pass

    @abc.abstractmethod
    def can_handle_pre_command(self) -> bool:
        """This method is called to check that the plugin can
        handle the pre_command method.

        Returns:
            bool: True if the plugin can handle the pre_command method."""
        return False

    @abc.abstractmethod
    def pre_command(
        self, command_name: str, arguments: Dict[str, Any]
    ) -> Tuple[str, Dict[str, Any]]:
        """This method is called before the command is executed.

        Args:
            command_name (str): The command name.
            arguments (Dict[str, Any]): The arguments.

        Returns:
            Tuple[str, Dict[str, Any]]: The command name and the arguments.
        """
        pass

    @abc.abstractmethod
    def can_handle_post_command(self) -> bool:
        """This method is called to check that the plugin can
        handle the post_command method.

        Returns:
            bool: True if the plugin can handle the post_command method."""
        return False

    @abc.abstractmethod
    def post_command(self, command_name: str, response: str) -> str:
        """This method is called after the command is executed.

        Args:
            command_name (str): The command name.
            response (str): The response.

        Returns:
            str: The resulting response.
        """
        pass

    @abc.abstractmethod
    def can_handle_chat_completion(
        self, messages: Dict[Any, Any], model: str, temperature: float, max_tokens: int
    ) -> bool:
        """This method is called to check that the plugin can
          handle the chat_completion method.

        Args:
            messages (List[Message]): The messages.
            model (str): The model name.
            temperature (float): The temperature.
            max_tokens (int): The max tokens.

          Returns:
              bool: True if the plugin can handle the chat_completion method."""
        return False

    @abc.abstractmethod
    def handle_chat_completion(
        self, messages: List[Message], model: str, temperature: float, max_tokens: int
    ) -> str:
        """This method is called when the chat completion is done.

        Args:
            messages (List[Message]): The messages.
            model (str): The model name.
            temperature (float): The temperature.
            max_tokens (int): The max tokens.

        Returns:
            str: The resulting response.
        """
        pass

from discord.ext import commands
from typing import Any, Dict, List, Optional, Tuple, TypeVar, TypedDict
class DiscordPlugin(AutoGPTPluginTemplate):
    def __init__(self, bot_token: str):
        super().__init__()
        self._name = "Auto-GPT Discord Plugin"
        self._version = "0.1.0"
        self._description = "This plugin enables Auto-GPT to communicate over Discord"
        self._bot_token = bot_token
        self._bot = None
        self._command_prefix = "!"

    async def connect(self):
        self._bot = commands.Bot(command_prefix=self._command_prefix)
        await self._bot.login(self._bot_token)
        await self._bot.connect()

    async def on_response(self, response: str, *args, **kwargs) -> str:
        if self._bot is not None:
            channel_id = kwargs.get("channel_id")
            if channel_id:
                channel = self._bot.get_channel(channel_id)
                if channel:
                    await channel.send(response)
        return response

    def can_handle_pre_command(self) -> bool:
        return True

    def pre_command(
        self, command_name: str, arguments: Dict[str, Any]
    ) -> Tuple[str, Dict[str, Any]]:
        if command_name == "hello":
            return "say_hello", {}
        return command_name, arguments

    @commands.command()
    async def say_hello(self, ctx):
        await ctx.send("Hello, world!")

    async def run(self):
        await self.connect()
        self._bot.add_command(self.say_hello)
        await self._bot.wait_until_ready()

    def can_handle_chat_completion(self) -> bool:
        return False

    def can_handle_on_response(self) -> bool:
        return True

    def handle_chat_completion(
        self, prompt: str, completions: List[str]
    ) -> Union[str, List[str]]:
        return completions

    async def can_handle_on_instruction(
        self, instruction: str, *args, **kwargs
    ) -> bool:
        return False

    async def on_instruction(
        self, instruction: str, *args, **kwargs
    ) -> Optional[str]:
        return None

    async def can_handle_pre_instruction(
        self, instruction: str, *args, **kwargs
    ) -> bool:
        return False

    async def pre_instruction(
        self, instruction: str, *args, **kwargs
    ) -> Tuple[str, List[Union[str, Dict[str, Any]]]]:
        return instruction, []

    async def can_handle_post_instruction(
        self, instruction: str, response: str, *args, **kwargs
    ) -> bool:
        return False

    async def post_instruction(
        self, instruction: str, response: str, *args, **kwargs
    ) -> Optional[str]:
        return None

    async def can_handle_on_planning(
        self, prompt: str, *args, **kwargs
    ) -> bool:
        return False

    async def on_planning(
        self, prompt: str, *args, **kwargs
    ) -> Optional[str]:
        return None

    async def can_handle_pre_planning(
        self, prompt: str, *args, **kwargs
    ) -> bool:
        return False

    async def pre_planning(
        self, prompt: str, *args, **kwargs
    ) -> Tuple[str, Dict[str, Any]]:
        return prompt, {}

    async def can_handle_post_planning(
        self, prompt: str, response: str, *args, **kwargs
    ) -> bool:
        return False

   
