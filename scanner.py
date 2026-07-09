import asyncio
import requests
from bleak import BleakScanner

# Change this if your API is on a different port
BACKEND_URL = "http://127.0.0.1:8005/api/v1/sync"

async def detection_callback(device, advertising_data):
    # We look for the Kudos wearable ID
    if device.address:
        print(f"Detected: {device.address} ({device.name})")

        # Simple payload to sync with your backend
        payload = {
            "host_device_uuid": "kudos-phone-001",
            "interactions": [{
                "guest_device_uuid": device.address,
                "interacted_at": "2026-07-08T21:30:00"
            }]
        }
        try:
            # This hits your API
            response = requests.post(BACKEND_URL, json=payload)
            print(f"Sync Result: {response.status_code}")
        except Exception as e:
            print(f"Sync failed: {e}")

async def run_scanner():
    print("Phone is actively scanning for Kudos devices...")
    scanner = BleakScanner(detection_callback)
    await scanner.start()
    await asyncio.sleep(60) # Scan for 60 seconds
    await scanner.stop()

if __name__ == "__main__":
    asyncio.run(run_scanner())
