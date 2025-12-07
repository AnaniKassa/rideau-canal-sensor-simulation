# sensor_simulator.py
import os
import time
import json
import random
from datetime import datetime, timezone
from dotenv import load_dotenv
from azure.iot.device import IoTHubDeviceClient

load_dotenv()

SEND_INTERVAL = int(os.getenv("SEND_INTERVAL", "10"))

# device connection strings from env
DEVICES = {
    "dowslake": os.getenv("DEVICE_CONNSTR_DOWS_LAKE"),
    "fifthave": os.getenv("DEVICE_CONNSTR_FIFTH_AVE"),
    "nac": os.getenv("DEVICE_CONNSTR_NAC")
}

# load config file
CONFIG_PATH = os.path.join(os.path.dirname(__file__), "config", "sensor_config.json")
with open(CONFIG_PATH, "r") as fh:
    config = json.load(fh)

ranges = config["telemetry_ranges"]

def rand_range(k):
    return random.uniform(ranges[k]["min"], ranges[k]["max"])

def build_payload(location_id):
    payload = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "location": location_id,
        "ice_thickness": round(rand_range("ice_thickness_cm"), 2),
        "surface_temperature": round(rand_range("surface_temperature_c"), 2),
        "snow_accumulation": round(rand_range("snow_accumulation_cm"), 2),
        "external_temperature": round(rand_range("external_temperature_c"), 2)
    }
    return payload

def run_device(device_id, conn_str):
    if not conn_str:
        print(f"[WARN] No connection string provided for {device_id} — skipping")
        return
    client = IoTHubDeviceClient.create_from_connection_string(conn_str)
    try:
        client.connect()
        print(f"[INFO] {device_id} connected to IoT Hub.")
        while True:
            payload = build_payload(device_id)
            msg_text = json.dumps(payload)
            # If you want, set message properties
            msg = msg_text
            client.send_message(msg)
            print(f"[SENT] {device_id} -> {msg_text}")
            time.sleep(SEND_INTERVAL)
    except KeyboardInterrupt:
        print("Exiting simulator.")
    except Exception as e:
        print("Error:", e)
    finally:
        try:
            client.disconnect()
        except:
            pass

if __name__ == "__main__":
    # Simple: run all three in separate threads
    import threading
    threads = []
    for device_id, conn in DEVICES.items():
        t = threading.Thread(target=run_device, args=(device_id, conn), daemon=True)
        t.start()
        threads.append(t)
    # keep main thread alive
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Stopped by user.")
