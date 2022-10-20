from fastapi import FastAPI
import http3

client = http3.AsyncClient()
app = FastAPI()

@app.get("/")
async def home():

    response = await client.get("http://localhost:5001/predictions")   
    if(response.status_code == 200):
        return {"output": response.json()}

    else:
        return {"Hello": "Error"}