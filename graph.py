from langgraph.graph import StateGraph,END
from agents.coder_agent import coder_agent_node
from agents.executor_agent import executor_agent_node
from agents.debugger_agent import debugger_agent_node
from state.agent_state import State
from langchain_groq.chat_models import ChatGroq
from dotenv import load_dotenv
from os import environ

load_dotenv()
api_key=environ.get('GROQ_API_KEY')
llm=ChatGroq(temperature=0,api_key=api_key,model='llama3-70b-8192')

decision=lambda state: 'end' if "SUCCESS" in state['messages'][-1].content else 'continue'
mapping={'end':END,'continue':'debugger'}

graph=StateGraph(State)
graph.add_node('coder',lambda state: coder_agent_node(state,llm))
graph.add_node('executor',lambda state: executor_agent_node(state,llm))
graph.add_node('debugger',lambda state: debugger_agent_node(state,llm))

graph.set_entry_point('coder')
graph.add_edge('coder','executor')
graph.add_conditional_edges('executor',decision,mapping)
graph.add_edge('debugger','executor')

python_ai_assistant=graph.compile(debug=True)