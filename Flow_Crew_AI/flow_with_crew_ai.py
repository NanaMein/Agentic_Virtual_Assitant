import asyncio
import random
from crewai.flow.flow import Flow, listen, router, start, or_, and_
from pydantic import BaseModel
from Flow_Crew_AI.Llama_RAG_Engine.llama_index_rag_engine import query_engine_small, query_engine_big
from Groq_Chat_Completion_Engine.Chat_Completion_Pipeline import chat_completion, chat_groq
from Memory_Layer.memory_for_past_context import add_to_memory, get_memory_context_prompt, reseting_local_memory
from Crew_Engine.first_crew import AgenticRoleplayer
# from Memory_Layer.memory_for_past_context import a

from datetime import datetime
import pytz

print("FLOW ENGINE LOADING...")


class FionicaState(BaseModel):
    input_flow_query: str = ""
    message: str = ""
    time: str = ""
    # output: str = ""
    chat_history: str = ""


class FionicaFlow(Flow[FionicaState]):

    @start()
    def starting(self):
        try:
            self.state.chat_history = get_memory_context_prompt()
            self.state.time = datetime.now(pytz.timezone('Asia/Manila')).strftime('%Y-%m-%d %H:%M:%S %Z')
            return "yes"
        except Exception as e:
            self.state.chat_history = f"{e}"
            return "no"

    @listen(starting)
    async def ai_agent(self):
        sentences = random.randint(1,5)
        fu_xuan = AgenticRoleplayer()
        prompt = (f"### User: {self.state.input_flow_query}\n"
                  f"### Previous chat context: {self.state.chat_history}"
                  f"""
                  ### Instruction: Previous chat context will be used as reference for context.
                  Please provide an answer based on the query or user question. Reply and answer like
                  a conversational dialogue or a script. Generate {sentences} sentence/s as an output.
                  """)
        # message = fu_xuan.run_crew(input_msg=prompt)
        # message = asyncio.run(fu_xuan.run_crew(input_msg=prompt))
        message = await fu_xuan.run_crew(input_msg=prompt)
        self.state.message = message

    @listen(ai_agent)
    def adding_memories(self):
        add_to_memory(user_input=self.state.input_flow_query, ai_output=self.state.message)
        return f"""
                \nUser: {self.state.input_flow_query}\n
                Assistant: {self.state.message}
                """




async def flow_run(input_message: str) -> str:
    flow = FionicaFlow()
    # flow.()
    kickoff = await flow.kickoff_async(inputs={'input_flow_query': input_message})
    return str(kickoff)


print("FLOW ENGINE LOADING COMPLETE")


def run():
    while True:
        print("starting loop and looping again")
        input_message = input("Write something: \n\n")
        if input_message == "exitingloop":
            reseting_local_memory()
            break
        # flow = flow_run(input_message=input_message)
        flow =asyncio.run(flow_run(input_message=input_message))
        print(flow)
        print("\n*********************************ENDLINE**********************************\n\n")


if __name__ == '__main__':
    run()

