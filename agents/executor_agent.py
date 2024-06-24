from prompts.executor_agent_prompt import prompt
from state.agent_state import State
from agents.agent import create_agent
from langchain_core.messages import HumanMessage
from tools.agent_tools import shell_tool,read_tool

def executor_agent_node(state:State,llm):
    agent=create_agent(prompt.name,prompt.description,prompt.instructions,[shell_tool,read_tool],llm)
    response=agent.invoke(state)
    return {**state, 'messages':[HumanMessage(response['output'],name=agent.name)]}