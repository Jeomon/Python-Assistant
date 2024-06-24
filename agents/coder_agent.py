from prompts.coder_agent_promt import prompt
from state.agent_state import State
from agents.agent import create_agent
from langchain_core.messages import HumanMessage
from tools.agent_tools import write_tool,documentation_tool,read_tool

def coder_agent_node(state:State,llm):
    agent=create_agent(prompt.name,prompt.description,prompt.instructions,[read_tool,write_tool],llm)
    response=agent.invoke(state)
    return {**state, 'messages':[HumanMessage(response['output'],name=agent.name)]}