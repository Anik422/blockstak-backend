from fastapi import FastAPI
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Blockstak Backend Running!", "api_key": os.getenv("NEWS_API_KEY")}
