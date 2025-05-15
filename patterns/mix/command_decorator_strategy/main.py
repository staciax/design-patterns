from __future__ import annotations

import asyncio
import os
import uuid
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from functools import partial
from typing import TYPE_CHECKING, Any, override

from pydantic_ai import Agent
from pydantic_ai.models.gemini import GeminiModel
from pydantic_settings import BaseSettings

if TYPE_CHECKING:
    from collections.abc import Sequence

    from pydantic_ai.agent import AgentRunResult
    from pydantic_ai.messages import ModelMessage
    from pydantic_ai.models import Model


assert os.getenv('GEMINI_API_KEY'), 'GEMINI_API_KEY not set in environment variables'

# TODO: fix generic type


class Settings(BaseSettings):
    # chat
    standard_model: partial[GeminiModel] = partial(GeminiModel, model_name='gemini-1.5-flash')
    advanced_model: partial[GeminiModel] = partial(GeminiModel, model_name='gemini-2.0-flash')
    expert_model: partial[GeminiModel] = partial(GeminiModel, model_name='gemini-2.5-pro-exp-03-25')

    # message limit
    maximum_subscribed_messages: int = 150
    maximum_unsubscribed_messages: int = 10


settings = Settings()


def _(text: str, color: str = 'white') -> str:
    colors = {
        'red': '\033[91m',
        'green': '\033[92m',
        'yellow': '\033[93m',
        'blue': '\033[94m',
    }
    reset = '\033[0m'
    if color not in colors:
        raise ValueError(f'Invalid color: {color}')
    return f'{colors[color]}{text}{reset}'


# strategy


def send_email(subject: str, email_to: str) -> str:
    return f'Sending email to {email_to!r} with subject {subject!r}'


def get_weather(city: str) -> str:
    return f'The weather in {city} is sunny'


class AgentContext:
    def __init__(self, strategy: AgentStrategy, system_prompt: str | Sequence[str] = ()) -> None:
        self._strategy = strategy
        self.system_prompt = system_prompt
        self._agent: Agent | None = None

    @property
    def strategy(self) -> AgentStrategy:
        return self._strategy

    @strategy.setter
    def strategy(self, strategy: AgentStrategy) -> None:
        self._strategy = strategy
        self._agent = None

    async def run(self, user_prompt: str, message_history: list[ModelMessage]) -> AgentRunResult[Any]:
        if not self._agent:
            self.agent = self._strategy.build_agent(self.system_prompt)
        result = await self.agent.run(user_prompt, message_history=message_history)
        return result


class AgentStrategy(ABC):
    @abstractmethod
    def build_agent(self, system_prompt: str | Sequence[str] = ()) -> Agent: ...


class StandardAgentStrategy(AgentStrategy):
    @override
    def build_agent(self, system_prompt: str | Sequence[str] = ()) -> Agent:
        model: Model = settings.standard_model()
        return Agent(model, system_prompt=system_prompt)


class AdvancedAgentStrategy(AgentStrategy):
    @override
    def build_agent(self, system_prompt: str | Sequence[str] = ()) -> Agent:
        model: Model = settings.advanced_model()
        return Agent(
            model,
            system_prompt=system_prompt,
            tools=[send_email],
        )


class ExpertAgentStrategy(AdvancedAgentStrategy):
    @override
    def build_agent(self, system_prompt: str | Sequence[str] = ()) -> Agent:
        model: Model = settings.expert_model()
        return Agent(
            model,
            system_prompt=system_prompt,
            tools=[send_email, get_weather],
        )


# command


class ICommand(ABC):
    @abstractmethod
    def execute(self) -> Any: ...


class BaseCommand(ICommand):
    @abstractmethod
    @override
    async def execute(self) -> Any: ...


# decorator


class BaseCommandDecorator(ICommand):
    def __init__[T: ICommand](self, command: T) -> None:
        self._command = command

    @property
    def command(self) -> ICommand:
        return self._command

    @override
    def execute(self) -> Any:
        return self._command.execute()

    def unwrap_command(self) -> ICommand:
        if isinstance(self._command, BaseCommandDecorator):
            return self._command.unwrap_command()
        return self._command


class LoggerCommandDecorator(BaseCommandDecorator):
    def __init__[T: ICommand](self, command: T, debug: bool = False) -> None:
        super().__init__(command)
        self.debug = debug

    @override
    def execute(self) -> Any:
        execute_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        command_name = self.unwrap_command().__class__.__name__

        message = _(f'[{execute_at}] executing command: {command_name}', 'green')
        if self.debug:
            attrs = {}
            command: ICommand = self
            if isinstance(self._command, BaseCommandDecorator):
                command = self._command.unwrap_command()
                attrs.update(command.__dict__)
            if attrs:
                message += _(f' with {attrs}', 'blue')

        print(message)

        return super().execute()


class ChatMessageLimitCommandDecorator(BaseCommandDecorator):
    def __init__[T: ICommand](self, command: T, chat: Chat) -> None:
        super().__init__(command)
        self.chat = chat

    @override
    def execute(self) -> Any:
        if self.chat.author.is_subscription_active():
            max_messages = settings.maximum_subscribed_messages
        else:
            max_messages = settings.maximum_unsubscribed_messages
        total_message_count = len(self.chat.messages)
        if total_message_count >= max_messages:
            raise ValueError(
                _(f'You have reached the maximum number of messages ({max_messages}) for this chat.', 'red')
            )
        return super().execute()


class RetryCommandDecorator(BaseCommandDecorator):
    def __init__[T: ICommand](self, command: T, max_retries: int = 3, delay: float = 1.0) -> None:
        super().__init__(command)
        self.max_retries = max_retries
        self.delay = delay

    @override
    async def execute(self) -> Any:
        for attempt in range(self.max_retries):
            try:
                return await super().execute()
            except Exception:
                if attempt == self.max_retries - 1:
                    raise
                await asyncio.sleep(self.delay)
        raise RuntimeError('Unknow error')


class NewChatCommand(BaseCommand):
    def __init__(self, app: App, user: User, system_prompt: str | Sequence[str] = ()) -> None:
        self.app = app
        self.user = user
        self.system_prompt = system_prompt

    @override
    async def execute(self) -> Chat:
        chat = self.app.new_chat(self.user)
        return chat


class RemoveChatCommand(BaseCommand):
    def __init__(self, app: App, chat: Chat, user: User) -> None:
        self.app = app
        self.chat = chat
        self.user = user

    @override
    async def execute(self) -> None:
        if self.chat.author != self.user:
            raise ValueError('You are not allowed to remove this chat')
        self.app.remove_chat(self.chat)


class PromptCommand(BaseCommand):
    def __init__(self, chat: Chat, user_prompt: str) -> None:
        self.chat = chat
        self.user_prompt = user_prompt

    @override
    async def execute(self) -> AgentRunResult[Any]:
        result = await self.chat.prompt(self.user_prompt)
        return result


class SwitchModelCommand(BaseCommand):
    def __init__(self, chat: Chat, agent_strategy: AgentStrategy) -> None:
        self.chat = chat
        self.agent_strategy = agent_strategy

    @override
    async def execute(self) -> None:
        user = self.chat.author
        if not user.is_subscription_active() and isinstance(self.agent_strategy, ExpertAgentStrategy):
            raise ValueError('Cannot switch to expert model for unsubscribed user')
        self.chat.agent_context.strategy = self.agent_strategy


class Invoker:
    def __init__(self, app: App) -> None:
        self.app = app
        self._command: ICommand | None = None

    def set_command[T: ICommand](self, command: T) -> None:
        self._command = command

    async def execute_command(self) -> Any:
        if self._command is None:
            raise ValueError('Command not set')

        try:
            result = await self._command.execute()
            return result
        except Exception as e:
            self.app.on_error(e)


@dataclass
class User:
    id: int
    name: str
    subscription_end_date: datetime | None = None

    def is_subscription_active(self) -> bool:
        return self.subscription_end_date is not None and self.subscription_end_date > datetime.now()

    def __repr__(self) -> str:
        return f'User(id={self.id!r}, name={self.name!r})'


class Chat:
    def __init__(self, id: str, user: User, agent_context: AgentContext) -> None:
        self.id = id
        self.author = user
        self.agent_context = agent_context
        self.messages: list[ModelMessage] = []

    def __repr__(self) -> str:
        return f'Chat(id={self.id!r}, author={self.author!r})'

    async def prompt(self, user_prompt: str) -> AgentRunResult[Any]:
        result = await self.agent_context.run(user_prompt, message_history=self.messages)
        self.messages.extend(result.new_messages())
        return result


class App:
    def __init__(self) -> None:
        self.chats: dict[str, Chat] = {}

    def new_chat(self, user: User) -> Chat:
        chat_id = str(uuid.uuid4().hex)
        agent_context = AgentContext(StandardAgentStrategy())
        chat = Chat(chat_id, user, agent_context)
        self.chats[chat_id] = chat
        return chat

    def remove_chat(self, chat: Chat) -> None:
        try:
            self.chats.pop(chat.id)
        except KeyError:
            pass

    def get_chat(self, chat_id: str) -> Chat | None:
        return self.chats.get(chat_id)

    def get_chats(self) -> list[Chat]:
        return list(self.chats.values())

    def on_error(self, error: Exception) -> None:
        print(_(f'app error: {error}', 'red'))


async def main() -> None:
    app = App()
    invoker = Invoker(app)

    user = User(id=1, name='STACiA', subscription_end_date=datetime(2025, 5, 1))
    # user.subscription_end_date = None

    # new chat
    new_chat_command: ICommand = NewChatCommand(
        app=app,
        user=user,
        system_prompt='You are a helpful assistant. and answer the user with thai language',
    )
    new_chat_command = LoggerCommandDecorator(new_chat_command, debug=True)
    invoker.set_command(new_chat_command)
    chat1 = await invoker.execute_command()
    print(_(f'chat created: {chat1}', 'yellow'))

    # prompt
    prompt_command: ICommand = PromptCommand(chat1, user_prompt='hi hi')
    prompt_command = ChatMessageLimitCommandDecorator(prompt_command, chat1)
    prompt_command = LoggerCommandDecorator(prompt_command, debug=True)
    invoker.set_command(prompt_command)
    result = await invoker.execute_command()
    print(_(f'result: {result.data.strip()}', 'yellow'))

    # switch agent
    new_agent_strategy = AdvancedAgentStrategy()
    # new_agent_strategy = ExpertAgentStrategy()
    switch_model_command: ICommand = SwitchModelCommand(
        chat=chat1,
        agent_strategy=new_agent_strategy,
    )
    switch_model_command = LoggerCommandDecorator(switch_model_command, debug=True)
    invoker.set_command(switch_model_command)
    await invoker.execute_command()

    # prompt again
    prompt_command2: ICommand = PromptCommand(chat1, user_prompt='hi hi')
    prompt_command2 = ChatMessageLimitCommandDecorator(prompt_command2, chat1)
    prompt_command2 = RetryCommandDecorator(prompt_command2, max_retries=3, delay=0.5)
    prompt_command2 = LoggerCommandDecorator(prompt_command2)
    invoker.set_command(prompt_command2)
    result = await invoker.execute_command()
    print(_(f'result: {result.data.strip()}', 'yellow'))


if __name__ == '__main__':
    asyncio.run(main())
