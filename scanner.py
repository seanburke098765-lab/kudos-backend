import asyncio
import time
import requests
import warnings
from urllib3.exceptions import NotOpenSSLWarning
from bleak import BleakScanner

warnings.filterwarnings("ignore", category=NotOpenSSLWarning)

API_URL = "http://127.0.0.1:8005/api/v1/sync"
RSSI_THRESHOLD = -70  
SYNC_COOLDOWN = 10     

last_synced_devices = {}

def detect_local_gesture():
    # Simulated validation event trigger (True = gesture validated)
    return True

def process_ble_packet(device_address, rssi, name):
    current_time = time.time()
    
    if rssi < RSSI_THRESHOLD:
        return

    if device_address in last_synced_devices:
        if current_time - last_synced_devices[device_address] < SYNC_COOLDOWN:
            return

    # Match the 5-field schema expected by the FastAPI Pydantic Model
    data = {
        "device_id": device_address,
        "rssi": int(rssi),
        "name": name or "Unknown Device",
        "current_user_id": "user_macbook",  # Explicit identifier for this system node
        "gesture_triggered": detect_local_gesture()
    }
    
    try:
        response = requests.post(API_URL, json=data)
        if response.status_code == 200:
            print(f"Sighting validated & transmitted -> {device_address}")
            last_synced_devices[device_address] = current_time
        else:
            print(f"Server rejected payload with status code: {response.status_code}")
    except requests.exceptions.RequestException:
        pass

async def run_scanner():
    print("Phone is actively scanning for Kudos devices with kinetic verification schemas...")
    
    def callback(device, advertisement_data):
        process_ble_packet(device.address, advertisement_data.rssi, device.name)

    async with BleakScanner(callback):
        while True:
            await asyncio.sleep(1.0)

if __name__ == "__main__":
    try:
        asyncio.run(run_scanner())
    except KeyboardInterrupt:
        print("\nScanner stopped.")
