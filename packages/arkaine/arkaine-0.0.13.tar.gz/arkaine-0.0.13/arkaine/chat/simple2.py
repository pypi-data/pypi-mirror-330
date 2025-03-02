import json
import pathlib
from datetime import datetime, timedelta
from os import path
from threading import Lock
from typing import Any, List, Optional, Tuple, Union

from arkaine.backends.ollama import Ollama
from arkaine.chat.chat import Chat
from arkaine.chat.conversation import Conversation, ConversationStore, Message
from arkaine.chat.parse_react_chat import parse_react_chat
from arkaine.llms.llm import LLM
from arkaine.llms.openai import OpenAI
from arkaine.tools import Tool
from arkaine.tools.argument import Argument
from arkaine.tools.result import Result
from arkaine.tools.tool import Context, Tool
from arkaine.tools.types import ToolCalls
from arkaine.utils.templater import PromptTemplate
from arkaine.utils.tool_format import openai as openai_tool_format


class Simple(Chat):
    """
    Simple is a simplistic chat agent, that can have multiple conversations,
    each with their own isolated history, tools, and state. It is simple in two
    ways:

    1. It follows the chat pattern of message->response - tit for tat - with no
        context sharing between conversations, no initiative. There is only the
        user and the agent.

    2. Its tool calling is handled in a simple manner (and is likely the aspect
        that children classes will want to override).

    If the LLM passed is OpenAI or Ollama, which have their own tool calling
    format/support, then the tool calling is handled by the LLM directly rather
    than arkaine parsing code.
    """

    def __init__(
        self,
        llm: LLM,
        tools: List[Tool],
        store: ConversationStore,
        agent_name: str = "Arkaine",
        user_name: str = "User",
        conversation_auto_active: float = 60.0,
        personality: Optional[str] = None,
        tool_name: str = "chat_agent",
    ):
        super().__init__(
            llm=llm,
            store=store,
            tools=tools,
            agent_name=agent_name,
            user_name=user_name,
            conversation_auto_active=conversation_auto_active,
            name=tool_name,
        )

        self.__tools = tools
        self.__personality = personality

        if isinstance(self._llm, OpenAI):
            pass
        elif isinstance(self._llm, Ollama):
            pass
        else:
            pass

    def _parse(self, response: str) -> Tuple[str, List[Tuple[str, Any]], str]:
        return parse_react_chat(response)

    def __call_llm(
        self, context: Context, conversation: Conversation, history: List[str]
    ) -> str:
        prompt = PromptTemplate.from_file(
            path.join(
                pathlib.Path(__file__).parent,
                "prompts",
                "chat_react.prompt",
            )
        )
        personality = ""
        if self.__personality:
            personality = (
                "## Personality\nYour personality you must emulate is:\n"
                f"{self.__personality}"
            )

        progress = ""
        if len(history) > 0:
            progress = "## Progress\nThe current progress of your thoughts and tool calls so far:\n"
            progress += "\n".join([f"{message}\n" for message in history])
        [print(x) for x in progress.splitlines()]

        conversation_text = ""
        for message in conversation:
            conversation_text += (
                f"{message.author} @ {message.on}:\n"
                f"{message.content}\n---\n"
            )

        name = ""
        if self._agent_name:
            name = f"## Name\nYour name is: {self._agent_name}\n"

        # print(
        #     "prompt:",
        #     prompt.render(
        #         {
        #             "personality": personality,
        #             "conversation": conversation_text,
        #             "progress": progress,
        #             "agent_name": name,
        #         }
        #     ),
        # )

        return self._llm.completion(
            prompt.render(
                {
                    "personality": personality,
                    "conversation": conversation_text,
                    "progress": progress,
                    "agent_name": name,
                }
            )
        )

    def chat(
        self,
        message: Union[str, Message],
        conversation: Conversation,
        context: Optional[Context] = None,
    ) -> Message:
        if isinstance(message, str):
            message = Message(
                author=self._user_name,
                content=message,
            )

        conversation.append(message)

        history = []
        while True:
            raw_response = self.__call_llm(context, conversation, history)
            print(">>>", raw_response)
            response, tool_calls, thought = self._parse(raw_response)

            if "thoughts" not in context:
                context["thoughts"] = []
            context["thoughts"].append(thought)

            history.append(thought)

            if len(tool_calls) > 0:
                history.append(tool_calls)
                results = self._call_tools(tool_calls)
                for name, args, result in results:
                    text = f"The tool call {name}("
                    text += ", ".join([f"{k}={v}" for k, v in args.items()])
                    text += ") returned:"
                    history.append(text)
                    history.append(result)

            if len(tool_calls) == 0:
                break

        return response


class SimpleChatPrompts:
    _lock = Lock()
    _prompts = {}

    @classmethod
    def _load_prompt(cls, name: str) -> str:
        with cls._lock:
            if name not in cls._prompts:
                filepath = path.join(
                    pathlib.Path(__file__).parent,
                    "prompts",
                    f"{name}.prompt",
                )
                with open(filepath, "r") as f:
                    cls._prompts[name] = f.read()
            return cls._prompts[name]

    @classmethod
    def chat_react(cls) -> str:
        return cls._load_prompt("chat_react")
