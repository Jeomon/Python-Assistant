from workflow.graph import python_assistant
from rich.markdown import Markdown
from rich.console import Console

console=Console()

if input:=input('Enter the query: '):
    response=python_assistant.invoke({'input':input}) 
    output=response['output']
    md=Markdown(output)
    console.print(md)