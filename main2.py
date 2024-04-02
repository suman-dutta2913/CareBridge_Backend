from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel
import requests

app = FastAPI()

class ImageToTextResponse(BaseModel):
    detected_text: str

class TranslationRequest(BaseModel):
    text: str
    target_language: str


google_translation_api_key = 'YOUR_GOOGLE_TRANSLATION_API_KEY'

@app.post("/imagetotext/")
async def image_to_text(upload_file: UploadFile = File(...)):
    try:
        # Save the uploaded image file temporarily
        with open(upload_file.filename, 'wb') as image_file:
            image_file.write(upload_file.file.read())
        
        # Send the image to the API-Ninjas endpoint for text extraction
        with open(upload_file.filename, 'rb') as image_file:
            files = {'image': image_file}
            response = requests.post('https://api.api-ninjas.com/v1/imagetotext', files=files)
        
        
        detected_text = response.json().get('detected_text', '')
        
        return {"detected_text": detected_text}
    
    except Exception as e:
        return {"error": str(e)}

@app.post("/translate/")
async def translate_text(translation_request: TranslationRequest):
    try:
        
        response = requests.post(
            f'https://translation.googleapis.com/language/translate/v2?key={google_translation_api_key}',
            json={
                "q": translation_request.text,
                "target": translation_request.target_language
            }
        )
        translated_text = response.json()['data']['translations'][0]['translatedText']
        
        return {"translated_text": translated_text}
    
    except Exception as e:
        return {"error": str(e)}
