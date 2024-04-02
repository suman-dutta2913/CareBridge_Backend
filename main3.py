from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import openai

app = FastAPI()

openai.api_key = 'your_openai_api_key_here'

class DiseaseRequest(BaseModel):
    disease_name: str

@app.post("/diagnose/")
async def diagnose_disease(disease_request: DiseaseRequest):
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",  
            prompt=f"I am experiencing symptoms of {disease_request.disease_name}. Can you please list common symptoms for this condition?",
            temperature=0.7,
            max_tokens=100
        )
        symptoms = response.choices[0].text.strip().split("\n")

        # Suggest line of action based on disease
        if is_easily_treatable(disease_request.disease_name):
            action = f"This disease seems to be easily treatable. You can try the following medicines: [List of medicines]."
            response1 = openai.Completion.create(
                engine="text-davinci-003",  
                prompt=f"Give a medical prescription if someone is suffering from {disease_request.disease_name}. Also suggest the do's and dont's while someone is suffering from {disease_request.disease_name}. Make everything as concise as possible.",
                temperature=0.7,
                max_tokens=100
            )
            action += response1.choices[0].text.strip()
        else:
            action = "This disease might require professional medical attention. We recommend booking an appointment with a doctor."

        return {"action": action, "symptoms": symptoms }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def is_easily_treatable(disease_name):
    easily_treatable_diseases = [
        "Common cold",
        "Fever",
        "Viral Fever",
        "Influenza (flu)",
        "Mild allergies",
        "Urinary tract infection (UTI)",
        "Acute sinusitis",
        "Strep throat",
        "Conjunctivitis (pink eye)",
        "Minor skin infections",
        "Muscle strains or sprains",
        "Mild food poisoning",
        "Simple urinary stones",
        "Ear infections",
        "Fungal skin infections (such as athlete's foot)",
        "Headaches (non-migraine)",
        "Minor cuts and scrapes",
        "Mild sunburn",
        "Bruises"
    ]
    return disease_name.lower() in easily_treatable_diseases

