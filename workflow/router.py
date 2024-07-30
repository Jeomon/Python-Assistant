from src.router.llm_router import create_llm_router
from langchain.schema.language_model import BaseLanguageModel
from workflow.state import State

def main_router(state:State,llm:BaseLanguageModel):
    routes=[
        {'name':'DEBUG','description':'If the user input is a code block or a filename on a specified directory and stating and issuse or an error within the script.'},
        {'name':'CODE','description':'If the user input is to write a code block for a given query and save that script in the specified directory.'},
        {'name':'MISC','description':'If the user input is related to provide a documentation, docstring, review,...etc for a code block.'},
    ]
    route=create_llm_router(state['input'],routes,llm)
    return {**state,'route':route}

    