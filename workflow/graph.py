from langgraph.graph import StateGraph,END
from workflow.node import (coder_agent_node,executor_agent_node,
debugger_agent_node,misc_node,summarizer_node)
from workflow.router import main_router
from workflow.state import State
from langchain_groq.chat_models import ChatGroq
from dotenv import load_dotenv
from os import environ

load_dotenv()
api_key=environ.get('GROQ_API_KEY')
llm=ChatGroq(temperature=0,api_key=api_key,model='llama3-70b-8192')

graph=StateGraph(State)

graph.add_node('router',lambda state:main_router(state,llm))
graph.add_node('misc',lambda state: misc_node(state,llm))
graph.add_node('coder',lambda state: coder_agent_node(state,llm))
graph.add_node('executor',lambda state: executor_agent_node(state,llm))
graph.add_node('debugger',lambda state: debugger_agent_node(state,llm))
graph.add_node('summarizer',lambda state: summarizer_node(state,llm))

graph.set_entry_point('router')
graph.add_conditional_edges('router',lambda state: state['route'].lower(),{'code':'coder','debug':'debugger','misc':'misc'})
graph.add_edge('coder','executor')
graph.add_conditional_edges('executor',lambda state: "summarizer" if "success" in state['messages'][-1].content.lower() else "debugger")
graph.add_edge('debugger','executor')
graph.set_finish_point('summarizer')
graph.set_finish_point('misc')

python_assistant=graph.compile(debug=True)