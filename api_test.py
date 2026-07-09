import os
from fastapi import FastAPI, HTTPException, Security, Depends
from fastapi.security import APIKeyHeader

# Use the environment variable, or default to the fallback key
SECRET_API_KEY = os.getenv("API_KEY", "fallback_local_key")
API_KEY_NAME = "X-API-KEY"

api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

def verify_api_key(api_key: str = Security(api_key_header)):
    if api_key == SECRET_API_KEY:
        return api_key
    raise HTTPException(
        status_code=401,
        detail="Invalid or missing API Key",
    )

app = FastAPI(dependencies=[Depends(verify_api_key)])

@app.get("/")
def home():
    return {"message": "Welcome to my first API!"}

@app.get("/tasks")
def get_tasks():
    return [{"id": 1, "task": "Learn how to build an API", "completed": False}]
