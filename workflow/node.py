from workflow.prompt import (coder_prompt,executor_prompt,debugger_prompt,
summarize_prompt,misc_prompt)
from workflow.state import State
from langchain.schema.language_model import BaseLanguageModel
from src.agent.react_agent import create_agent
from langchain_core.messages import HumanMessage
from langchain_core.prompts.chat import ChatPromptTemplate
from pydantic.v1 import BaseModel,Field
from langchain_core.output_parsers import StrOutputParser

def coder_agent_node(state:State,llm:BaseLanguageModel):
    name=coder_prompt.name
    description=coder_prompt.description
    instructions=coder_prompt.instructions
    tools=coder_prompt.tools
    agent=create_agent(name,description,instructions,tools,llm)
    response=agent.invoke(state)
    return {**state, 'messages':[HumanMessage(response['output'],name=agent.name)]}

def executor_agent_node(state:State,llm:BaseLanguageModel):
    name=executor_prompt.name
    description=executor_prompt.description
    instructions=executor_prompt.instructions
    tools=executor_prompt.tools
    agent=create_agent(name,description,instructions,tools,llm)
    response=agent.invoke(state)
    return {**state, 'messages':[HumanMessage(response['output'],name=agent.name)]}

def debugger_agent_node(state:State,llm:BaseLanguageModel):
    name=debugger_prompt.name
    description=debugger_prompt.description
    instructions=debugger_prompt.instructions
    tools=debugger_prompt.tools
    route=state['route'].lower()
    agent=create_agent(name,description,instructions[route],tools[route],llm)
    response=agent.invoke(state)
    return {**state, 'messages':[HumanMessage(response['output'],name=agent.name)]}

def misc_node(state:State,llm:BaseLanguageModel):
    prompt=ChatPromptTemplate.from_template(misc_prompt)
    parser=StrOutputParser()
    chain=prompt|llm|parser
    response=chain.invoke({'query':state['input']})
    return {**state, 'output':response}

def summarize_node(state:State,llm:BaseLanguageModel):
    class Summarize(BaseModel):
        summary:str=Field(...,description="The summary of the workflow.")

    prompt=ChatPromptTemplate.from_template(summarize_prompt)
    chain=prompt|llm.with_structured_output(Summarize)
    response=chain.invoke({'context':state['messages']})
    return {**state, 'output':response.summary}