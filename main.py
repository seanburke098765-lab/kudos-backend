from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import sqlite3

# Initialize DB
conn = sqlite3.connect("kudos.db", check_same_thread=False)
cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS interactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        host_device TEXT,
        guest_device TEXT,
        timestamp TEXT
    )
""")
conn.commit()

app = FastAPI()

class Interaction(BaseModel):
    guest_device_uuid: str
    interacted_at: str

class SyncRequest(BaseModel):
    host_device_uuid: str
    interactions: List[Interaction]

@app.post("/api/v1/sync")
async def sync_kudos(payload: SyncRequest):
    for item in payload.interactions:
        cursor.execute(
            "INSERT INTO interactions (host_device, guest_device, timestamp) VALUES (?, ?, ?)",
            (payload.host_device_uuid, item.guest_device_uuid, item.interacted_at)
        )
    conn.commit()
    return {"status": "success"}

@app.get("/api/v1/kudos")
def get_kudos():
    cursor.execute("SELECT * FROM interactions")
    return {"data": cursor.fetchall()}
