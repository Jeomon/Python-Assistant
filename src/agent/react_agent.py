from langchain.agents import create_structured_chat_agent,AgentExecutor
from src.agent.react_agent_prompt import system_prompt,user_prompt
from langchain_core.tools import BaseTool
from langchain.schema.language_model import BaseLanguageModel
from langchain_core.prompts.chat import ChatPromptTemplate
from platform import system
from getpass import getuser
from os import getcwd

def create_agent(name:str,description:str,instructions:list[str],tools:list[BaseTool],llm:BaseLanguageModel,verbose:bool=False):
    prompt=ChatPromptTemplate.from_messages([
        ('system',system_prompt),
        ('user',user_prompt)
    ]).partial(name=name,description=description,
    instructions='\n'.join(instructions),operating_system=system(),
    user=getuser(),cwd=getcwd())
    agent=create_structured_chat_agent(llm,tools,prompt)
    return AgentExecutor(name=name,agent=agent,tools=tools,verbose=verbose,handle_parsing_errors=True)