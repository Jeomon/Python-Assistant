from typing import TypedDict,Annotated
from operator import add
from langchain.schema.messages import BaseMessage

class State(TypedDict):
    input:str
    messages:Annotated[list[BaseMessage],add]=[]
