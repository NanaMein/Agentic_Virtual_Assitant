import os
# from functools import lru_cache
from typing import Any
from dotenv import load_dotenv
from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from groq import Groq
from typing import Type
from groq.types.chat import (
    ChatCompletionUserMessageParam,
    ChatCompletionAssistantMessageParam,
    ChatCompletionSystemMessageParam
)
from .agents_personality import query_engine_chat
from Flow_Crew_AI.Llama_RAG_Engine.llama_index_rag_engine import query_engine_big as rag_query_tool
from Flow_Crew_AI.Llama_RAG_Engine.llama_index_rag_engine import query_engine_small as backup_tool


print('TOOL FOR CREW LOADING')
load_dotenv()


class BaseCompoundBeta(BaseModel):
    argument: str = Field(..., description="Input for what you want to search in the web")
# @lru_cache(maxsize=50)
class CompoundBeta(BaseTool):
    name: str = "Web search query tool"
    description: str = "Tool for searching the web"
    args_schema: Type[BaseModel] = BaseCompoundBeta

    def _run(
            self,
            argument: str,
            *args: Any,
            **kwargs: Any,
    ) -> Any:
        client = Groq(api_key=os.environ.get('API_KEY'))
        completion = client.chat.completions.create(
            messages=[
                ChatCompletionAssistantMessageParam(
                    role="assistant",
                    content="You are a very helpful ai assistant tool",
                ),
                ChatCompletionUserMessageParam(
                    role="user",
                    content=argument,
                ),
            ],
            model="compound-beta-mini",
        )

        return completion.choices[0].message.content





# user = f"what is {random_season}?"
# assistant = "you are a helpful assistant"
# systems = ("You will roleplay as a little girl with childish and cute personality"
#            f"Generate {random_int} sentence/s")
# async_obj = asyncio.run(groq_async(user=user, assistant=assistant, system=systems))
#
# print(async_obj)


class ToolInput(BaseModel):
    message: str = Field(...,description="query for what is being searched in the web")

# @lru_cache(maxsize=50)
class CompoundBetaTool(BaseTool):

    name: str = "Web Search Tool"
    description: str = """ This is a tool used to search in the web if the Character Lore Tool is not enough.
                        This is also for other complex stuffs, events and situation that Character Lore Tool
                        cant provide. Also it can be used to search in the web for other useful stuffs"""
    args_schema : Type[BaseModel] = ToolInput

    def _run(
        self,
        message: str,
        *args: Any,
        **kwargs: Any,
    ) -> Any:
        return tool_llm(message)

def tool_llm(argument: str)->str:
    """Web search tool that answers questions using Groq LLM."""
    client = Groq(api_key=os.environ.get('API_KEY'))
    completion = client.chat.completions.create(
        messages=[
            ChatCompletionSystemMessageParam(
                role="system",
                content="""
                You will be used as a Web Search Tool. Please gather relevant information
                and follow instructions
                """
            ),
            ChatCompletionAssistantMessageParam(
                role="assistant",
                content="You are a very helpful ai assistant tool",
            ),
            ChatCompletionUserMessageParam(
                role="user",
                content=argument,
            ),
        ],
        model="compound-beta",
    )
    return completion.choices[0].message.content















class RagQueryInput(BaseModel):
    input_query: str = Field(..., description="query for what is being searched in the context provided")

# @lru_cache(maxsize=50)
class RagTool(BaseTool):
    name: str = "Character Lore Tool"
    description: str = "Character biography, history, personality, and description of Fu Xuan and Xianzhou Alliance"
    args_schema: Type[BaseModel] = RagQueryInput

    def _run(
            self,
            input_query: str,
            *args: Any,
            **kwargs: Any,
    ) -> Any:
        """ RAG LLAMA FUNCTION HERE"""
        try:
            output = rag_query_tool(input_query=input_query)
            return output
        except Exception as e:
            print(f"Error for QUERY BIG LLAMA, WILL USE LLAMA SMALL INSTEAD{e}")
            final = backup_tool(input_query=input_query)
            return final











class CharacterPersonalityInput(BaseModel):
    input_query: str = Field(..., description="query for what is being searched in the context provided")

# @lru_cache(maxsize=50)
class CharacterRolePlay(BaseTool):
    name: str = "Character description tool"
    description: str = """Character biography, history, personality, relationship and 
        Fionica, the virtual daughter"""
    args_schema: Type[BaseModel] = CharacterPersonalityInput

    def _run(
            self,
            input_query: str,
            *args: Any,
            **kwargs: Any,
    ) -> Any:
        """ RAG LLAMA FUNCTION HERE"""
        try:
            output = query_engine_chat(inputs=input_query)
            return output
        except Exception as e:
            print(f"Error for QUERY BIG LLAMA, WILL USE LLAMA SMALL INSTEAD{e}")
            final = backup_tool(input_query=input_query)
            return final
