from workflow.graph import python_ai_assistant

if input:=input('Enter the query: '):
    response=python_ai_assistant.invoke({'input':input}) 
    print(response['output'])