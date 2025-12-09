## Rideau Canal Sensor Simulation

### 1. Overview

The Rideau Canal Sensor Simulator generates realistic environmental and safety data for three monitored locations along the canal—Dow’s Lake, Fifth Avenue, and the NAC.
It continuously sends telemetry to Azure IoT Hub, mimicking real-world IoT devices measuring:

Ice thickness

Surface temperature

Snow accumulation

Safety status

Event timestamp

Technologies Used:

Python 3.x

Azure IoT Device SDK for Python

Asynchronous background data generation

Environment-based configuration

### 2. Prerequisites

Before running the simulator, ensure you have:

Python 3.9+

An active Azure IoT Hub

A registered IoT device with a connection string

pip installed

Internet connection for IoT Hub communication

### 3. Installation

- Clone the repository:

git clone https://github.com/AnaniKassa/rideau-canal-sensor-simulation
cd rideau-canal-sensor-simulation

- Install dependencies:

pip install -r requirements.txt

### 4. Configuration

- Create a .env file in the project root:

IOTHUB_DEVICE_CONNECTION_STRING="your-device-connection-string"
DEVICE_ID="rideau-sensor-01"
SEND_INTERVAL_SECONDS=300      # default 5 minutes

- You can add multiple device files if you’re simulating several sensors (optional).

### 5. Usage

- Run the simulator:

python sensor_simulator.py

- The script will:

Generate random-but-realistic sensor values

Package them into JSON

Send messages to Azure IoT Hub at the configured interval

Display logs of each event sent

- To run in background mode (Linux/macOS):

nohup python simulator.py &

### 6. Code Structure
```
rideau-canal-sensor-simulation/
├── sensor_simulator.py
├── config/
│   ├── sensor_config.json
├── .env
├── requirements.txt
└── README.md
```
- Main Components

sensor_simulator.py
Orchestrates telemetry generation and IoT Hub communication.

- Key Functions

generate_sensor_data(location) – Produces ice, temperature, snow, and safety metrics.

send_message(payload) – Publishes JSON data to IoT Hub.

run_simulator() – Main loop that schedules periodic data transmission.

### 7. Sensor Data Format
JSON Schema
```
{
  "device_id": "string",
  "location": "string",
  "event_time": "ISO-8601 timestamp",
  "avg_ice_thickness": "float",
  "avg_surface_temperature": "float",
  "max_snow_accumulation": "float",
  "safety_status": "Safe | Caution | Unsafe"
}
```

Example Output
```
{
  "device_id": "rideau-sensor-01",
  "location": "dowslake",
  "event_time": "2025-12-08T14:33:21Z",
  "avg_ice_thickness": 18.4,
  "avg_surface_temperature": -7.3,
  "max_snow_accumulation": 3.1,
  "safety_status": "Safe"
}
```
### 8. Troubleshooting
Connection issues

Ensure IoT Hub device connection string is correct.

Verify the device is enabled in Azure IoT Hub.

Check firewall or network restrictions that might block outbound MQTT/AMQP.

Python errors

Run pip install -r requirements.txt again.

Confirm Python version is 3.9 or newer.

No messages appearing in IoT Hub

Verify IoT Hub metrics → Messages received.

Check if the SEND_INTERVAL_SECONDS is too long.

Run the simulator with verbose logging enabled (add print statements).