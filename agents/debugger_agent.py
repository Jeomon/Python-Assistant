from prompts.debugger_agent_prompt import prompt
from state.agent_state import State
from agents.agent import create_agent
from langchain_core.messages import HumanMessage
from tools.agent_tools import shell_tool,read_tool,write_tool,documentation_tool

def debugger_agent_node(state:State,llm):
    agent=create_agent(prompt.name,prompt.description,prompt.instructions,[read_tool,write_tool,shell_tool],llm)
    response=agent.invoke(state)
    return {**state, 'messages':[HumanMessage(response['output'],name=agent.name)]}