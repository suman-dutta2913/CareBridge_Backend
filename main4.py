from fastapi import FastAPI, HTTPException
import requests

app = FastAPI()

GOOGLE_MAPS_API_KEY = "YOUR_API_KEY"

@app.get("/nearest_hospital")
async def nearest_hospital(latitude: float, longitude: float):
    url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={latitude},{longitude}&radius=5000&type=hospital&key={GOOGLE_MAPS_API_KEY}"
    
    response = requests.get(url)
    data = response.json()
    
    if data["status"] == "OK":
        if len(data["results"]) > 0:
            nearest_hospital = data["results"][0]
            nearest_hospital_name = nearest_hospital["name"]
            nearest_hospital_location = nearest_hospital["geometry"]["location"]
            hospital_latitude = nearest_hospital_location["lat"]
            hospital_longitude = nearest_hospital_location["lng"]
            
            directions_url = f"https://www.google.com/maps/dir/?api=1&origin={latitude},{longitude}&destination={hospital_latitude},{hospital_longitude}&travelmode=driving"
            
            return {"nearest_hospital_name": nearest_hospital_name, "directions_url": directions_url}
        else:
            raise HTTPException(status_code=404, detail="No hospitals found within 5000 meters.")
    else:
        raise HTTPException(status_code=500, detail="Error retrieving data from Google Maps API.")
