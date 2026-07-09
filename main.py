from fastapi import FastAPI, APIRouter
from pydantic import BaseModel
from datetime import datetime, timedelta
from typing import Dict

app = FastAPI(title="Kudos Backend Ecosystem")
router = APIRouter(prefix="/api/v1", tags=["sync"])

class SyncPayload(BaseModel):
    device_id: str
    rssi: int
    name: str
    current_user_id: str
    gesture_triggered: bool

# Stores valid kinetic handshakes: { user_id: { spotted_device_id: timestamp } }
validated_matches: Dict[str, Dict[str, datetime]] = {}

MATCH_WINDOW_SECONDS = 5

@router.post("/sync")
async def sync_device(payload: SyncPayload):
    now = datetime.utcnow()
    user_id = payload.current_user_id
    spotted_id = payload.device_id

    # If local accelerometer hasn't fired yet, just log a quiet scanning trace
    if not payload.gesture_triggered:
        return {"status": "scanning", "message": "Proximity logged, awaiting local gesture confirmation."}

    # Record that THIS user performed the gesture targeting the spotted device
    if user_id not in validated_matches:
        validated_matches[user_id] = {}
    validated_matches[user_id][spotted_id] = now

    # Check for the reciprocal gesture validation window
    if spotted_id in validated_matches and user_id in validated_matches[spotted_id]:
        peer_gesture_time = validated_matches[spotted_id][user_id]
        
        # Core Verification: Did both trigger actions within 5 seconds of each other?
        if now - peer_gesture_time <= timedelta(seconds=MATCH_WINDOW_SECONDS):
            print(f"\n[MATCH VERIFIED] Successful Kudos exchange between {user_id} and {spotted_id}!\n")
            return {
                "status": "SUCCESS_MATCH_VERIFIED",
                "peer_id": spotted_id,
                "message": "Kudos profile exchange successful!"
            }

    return {"status": "pending_peer_gesture", "message": "Your gesture logged. Waiting for peer device action."}

app.include_router(router)
