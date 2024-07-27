from langchain_community.tools import tool
from pydantic.v1 import BaseModel,Field
from duckduckgo_search import DDGS
from typing import Optional,List
from bs4 import BeautifulSoup
import shlex
import subprocess
import os
import requests

class Write(BaseModel):
    directory: str = Field(..., description="The directory where the file should be saved.")
    file_name: str = Field(..., description="The name of the file to write the content in.")
    content: str = Field(..., description="The content to be written to the file.")
@tool('Write Tool',args_schema=Write)
def write_tool(directory, file_name, content):
    """
    Write the given content to a specified file within a given directory.
    example: write_tool('./bar','abc.py','Hello World')
    """
    if not os.path.exists(directory):
        os.makedirs(directory)
    file_path = os.path.join(directory, file_name)
    with open(file_path, 'w') as file:
        file.write(content)
    return f"The {file_name} successfully saved to {file_path}"

class Read(BaseModel):
    directory: str = Field(..., description="The directory where the file is located.")
    file_name: str = Field(..., description="The name of the file to read the content from.")

@tool('Read Tool',args_schema=Read)
def read_tool(directory,file_name):
    """
    Read the content from a specified file within a given directory.
    example: read_tool('foo/bar','abc.py')
    """
    file_path = os.path.join(directory, file_name)
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist.")
    with open(file_path, 'r') as file:
        content = file.read()
    print(f"Content successfully read from {file_path}")
    return content

class Shell(BaseModel):
    command: str = Field(..., description="The shell command to be executed.")
    script_args: Optional[List[str]] = Field(description="Optional arguments for the shell command.")
    user_inputs: Optional[str] = Field(description="User inputs for the python script.")

@tool('Shell Tool',args_schema=Shell)
def shell_tool(command, script_args,user_inputs) -> str:
    """
    Execute the shell command, python scripts then return their output.
    """
    try:
        safe_command = shlex.split(command)
        if script_args:
            safe_command.extend(script_args)
        result = subprocess.run(safe_command, capture_output=True, text=True,input=user_inputs)
        if result.returncode != 0:
            return f"Error: {result.stderr.strip()}"
        return result.stdout.strip()
    except Exception as e:
        return f"Exception occurred: {str(e)}"