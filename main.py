import openai
from dotenv import load_dotenv
import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from langchain.llms import OpenAI
from langchain.prompts import OpenAI
from langchain.chains import SimpleSequentialChain

app = FastAPI()


openai.api_key = 'your_openai_api_key_here'

class HealthIssueRequest(BaseModel):
    issue: str

@app.post("/diagnose/")
async def diagnose_health_issue(issue_request: HealthIssueRequest):
    
    prompt = f"I am experiencing {issue_request.issue}. Can you please provide a probable diagnosis?"
    
    try:
        
        response = openai.Completion.create(
            engine="text-davinci-003",  
            prompt=prompt,
            temperature=0.7,
            max_tokens=100,
            n=3  
        )
        
        
        diagnoses = [choice.text.strip() for choice in response.choices]
        
        return {"diagnoses": diagnoses}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

      