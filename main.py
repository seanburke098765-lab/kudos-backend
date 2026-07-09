from fastapi import FastAPI, Request

app = FastAPI()

@app.post("/api/v1/sync")
async def sync_kudos(request: Request):
    data = await request.json()
    print(f"Received data: {data}")
    return {"status": "success"}

@app.get("/")
def read_root():
    return {"message": "Server is running"}
