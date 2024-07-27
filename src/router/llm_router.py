
from langchain_core.prompts.chat import ChatPromptTemplate
from langchain.schema.language_model import BaseLanguageModel
from src.router.prompt import router_prompt
from pydantic import BaseModel,Field

class Route(BaseModel):
    route:str=Field(...,description="The name of the route.")

def create_llm_router(query:str,routes:list[dict],llm:BaseLanguageModel):
    routes='\n\n'.join([f"route_name: {route['name']}\nroute_description: {route['description']}" for route in routes])
    prompt=ChatPromptTemplate.from_template(router_prompt).partial(routes=routes)
    chain=prompt|llm.with_structured_output(Route)
    response=chain.invoke({'input':query})
    return response['route']