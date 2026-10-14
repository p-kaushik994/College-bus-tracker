import requests
import time
import random

# The URL of your running Flask server
SERVER_URL = "http://localhost:5000/api/buses/1/location"

# Starting GPS Coordinate (e.g., Near College Campus)
latitude = 17.385044
longitude = 78.486671

print("🚌 Starting Virtual Driver for Bus #1...")
print(f"📡 Transmitting to {SERVER_URL}")
print("Press Ctrl+C at any time to stop the bus.\n")

step = 1

while True:
    # 1. Simulate varying city driving speed (0 to 45 km/h)
    # Every 5th step, simulate waiting at a red traffic light (speed = 0)
    if step % 5 == 0:
        speed = 0.0
        print("🚦 Stopped at a traffic signal...")
    else:
        speed = round(random.uniform(25.0, 42.0), 1)
        # Nudge coordinates slightly North-East along the street (~30-50 meters)
        latitude += 0.000300
        longitude += 0.000250

    # 2. Package the JSON payload
    payload = {
        "latitude": round(latitude, 6),
        "longitude": round(longitude, 6),
        "speed": speed
    }

    # 3. Transmit the HTTP POST request to Flask
    try:
        response = requests.post(SERVER_URL, json=payload, timeout=5)

        if response.status_code == 201:

            data = response.json()
            loc = data["location"]

            print(f"[{loc['updated_at'][11:19]}] Step {step} | Lat: {loc['latitude']} | Lng: {loc['longitude']} | Speed: {loc['speed']} km/h -> Server: 201 OK")

        else:

            print(f"⚠️ Server returned error {response.status_code}: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to Flask. Is 'python app.py' running in another terminal?")

    step += 1
    # 4. Wait 4 seconds before transmitting the next coordinate
    time.sleep(4)