from graph import python_ai_assistant

if input:=input('Enter the Query: '):
    response=python_ai_assistant.invoke({'input':input}) 
    print(response)