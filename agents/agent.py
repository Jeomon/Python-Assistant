from langchain.agents import create_structured_chat_agent,AgentExecutor
from prompts.agent_prompt import system_prompt,user_prompt
from langchain_core.prompts.chat import ChatPromptTemplate
from state.agent_state import State
from platform import system
from getpass import getuser
from os import getcwd

def create_agent(name,description,instructions,tools,llm):
    prompt=ChatPromptTemplate.from_messages([
        ('system',system_prompt),
        ('user',user_prompt)
    ]).partial(name=name,description=description,
    instructions='\n'.join(instructions),operating_system=system(),user=getuser(),cwd=getcwd())
    agent=create_structured_chat_agent(llm,tools,prompt)
    return AgentExecutor(name=name,agent=agent,tools=tools,verbose=True,handle_parsing_errors=True)