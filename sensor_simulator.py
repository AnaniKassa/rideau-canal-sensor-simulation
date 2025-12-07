import os
import asyncio
import signal
import uuid
from datetime import datetime, timezone
from azure.iot.device.aio import IoTHubDeviceClient
from dotenv import load_dotenv
import random
import logging

# Load .env variables
load_dotenv()
DEVICE_CONNECTIONS = {
    "dowslake": os.getenv("DEVICE_CONNSTR_DOWS_LAKE"),
    "fifthave": os.getenv("DEVICE_CONNSTR_FIFTH_AVE"),
    "nac": os.getenv("DEVICE_CONNSTR_NAC")
}

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')

# Graceful shutdown
STOP_EVENT = asyncio.Event()

def signal_handler():
    logging.info("Exiting simulation...")
    STOP_EVENT.set()

signal.signal(signal.SIGINT, lambda s, f: signal_handler())
signal.signal(signal.SIGTERM, lambda s, f: signal_handler())

# Generate sensor data
def generate_sensor_data(location):
    ice_thickness = round(random.uniform(5.0, 15.0), 2)
    surface_temp = round(random.uniform(-20.0, -10.0), 2)
    snow_accumulation = round(random.uniform(0.0, 5.0), 2)
    external_temp = round(random.uniform(-25.0, -5.0), 2)

    avg_ice = round((ice_thickness + 6 + 9) / 3, 2)  # sample average calculation
    avg_surface = round((surface_temp + -12 + -15) / 3, 2)
    max_snow = max(snow_accumulation, 2, 3)
    safety_status = "Safe" if ice_thickness > 8 else "Caution"

    return {
        "id": str(uuid.uuid4()),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "location": location,
        "ice_thickness": ice_thickness,
        "surface_temperature": surface_temp,
        "snow_accumulation": snow_accumulation,
        "external_temperature": external_temp,
        "avgIceThickness": avg_ice,
        "avgSurfaceTemperature": avg_surface,
        "maxSnowAccumulation": max_snow,
        "safetyStatus": safety_status,
        "windowEndTime": datetime.now(timezone.utc).isoformat()
    }

async def send_data(client: IoTHubDeviceClient, location: str):
    await client.connect()
    logging.info(f"{location} client ready")
    try:
        while not STOP_EVENT.is_set():
            data = generate_sensor_data(location)
            try:
                await client.send_message(str(data))
                logging.info(f"SENT IoT Hub] {location} -> {data}")
            except Exception as e:
                logging.error(f"Failed to send message for {location}: {e}")
            await asyncio.sleep(5)  # send every 5 seconds
    finally:
        await client.shutdown()
        logging.info(f"{location} client disconnected")

async def main():
    clients = {}
    for loc, conn_str in DEVICE_CONNECTIONS.items():
        if not conn_str:
            logging.error(f"No connection string found for {loc}")
            continue
        clients[loc] = IoTHubDeviceClient.create_from_connection_string(conn_str)

    # Start sending data concurrently for all clients
    tasks = [send_data(client, loc) for loc, client in clients.items()]
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())
