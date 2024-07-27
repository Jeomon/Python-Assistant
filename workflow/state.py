from typing import TypedDict,Annotated
from operator import add
from langchain.schema.messages import BaseMessage

class State(TypedDict):
    input:str
    route:str
    messages:Annotated[list[BaseMessage],add]
    output:str
