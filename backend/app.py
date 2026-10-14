from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)

# --- IN-MEMORY DATA STORAGE ---
BUSES = {
    1: {"id": 1, "bus_name": "Route 1 - North Campus", "driver_name": "Vikram", "capacity": 40},
    2: {"id": 2, "bus_name": "Route 2 - South Campus", "driver_name": "Suresh", "capacity": 45}
}
next_bus_id = 3

# Stores the latest live location per bus: {bus_id: {latitude, longitude, speed, updated_at}}
BUS_LOCATIONS = {}

# --- ROUTE 1: GET ALL BUSES ---
@app.route("/api/buses", methods=["GET"])
def get_all_buses():
    """Returns a list of all buses."""
    # Convert dictionary values to a list: list(BUSES.values())
    return jsonify({
        "buses": list(BUSES.values()),
        "total": len(BUSES)
    }), 200


# --- ROUTE 2: GET A SPECIFIC BUS ---
@app.route("/api/buses/<int:bus_id>", methods=["GET"])
def get_single_bus(bus_id):
    """Returns details of a single bus by ID."""
    if bus_id not in BUSES:
        return jsonify({"error": f"Bus {bus_id} not found"}), 404
    
    return jsonify({"bus": BUSES[bus_id]}), 200


# --- ROUTE 3: CREATE A NEW BUS ---
@app.route("/api/buses", methods=["POST"])
def create_bus():
    """Allows creating a new bus."""
    global next_bus_id
    data = request.get_json()

    # Validation: Make sure bus_name is provided
    if not data or "bus_name" not in data:
        return jsonify({"error": "'bus_name' is required"}), 400

    new_bus = {
        "id": next_bus_id,
        "bus_name": data["bus_name"],
        "driver_name": data.get("driver_name", "Unassigned"),
        "capacity": data.get("capacity", 50)
    }

    BUSES[next_bus_id] = new_bus
    next_bus_id += 1

    return jsonify({
        "message": "Bus created successfully",
        "bus": new_bus
    }), 201

# --- ROUTE 4: DRIVER SENDS GPS COORDINATES ---
@app.route("/api/buses/<int:bus_id>/location", methods=["POST"])
def update_bus_location(bus_id):
    """
    Called by the Driver App to transmit live GPS coordinates.
    """
    # 1. Make sure the bus actually exists in our fleet
    if bus_id not in BUSES:
        return jsonify({"error": f"Bus {bus_id} does not exist in the fleet"}), 404

    # 2. Extract JSON payload
    data = request.get_json()

    # 3. Input Validation
    if not data or "latitude" not in data or "longitude" not in data:
        
        return jsonify({"error": "'latitude' and 'longitude' are required fields"}), 400

    try:
        lat = float(data["latitude"])
        lng = float(data["longitude"])
        speed = float(data.get("speed", 0.0))

    except (ValueError, TypeError):

        return jsonify({"error": "Latitude, longitude, and speed must be valid numbers"}), 400

    # 4. Save the latest location record with an ISO timestamp
    location_record = {
        "bus_id": bus_id,
        "latitude": lat,
        "longitude": lng,
        "speed": speed,
        "updated_at": datetime.now().isoformat()
    }
    BUS_LOCATIONS[bus_id] = location_record

    return jsonify({
        "message": "Location updated successfully",
        "location": location_record
    }), 201


# --- ROUTE 5: STUDENT CHECKS LIVE LOCATION ---
@app.route("/api/buses/<int:bus_id>/location", methods=["GET"])
def get_bus_location(bus_id):
    """
    Called by the Student App to view where the bus is right now.
    """
    # 1. Check if bus exists
    if bus_id not in BUSES:
        return jsonify({"error": f"Bus {bus_id} not found"}), 404

    # 2. Check if the driver has transmitted any location yet
    if bus_id not in BUS_LOCATIONS:
        return jsonify({
            "bus_id": bus_id,
            "status": "offline",
            "message": "Bus has not transmitted any location data yet"
        }), 404

    # 3. Return the latest live location
    return jsonify({
        "bus_id": bus_id,
        "status": "live",
        "location": BUS_LOCATIONS[bus_id]
    }), 200

if __name__ == "__main__":
    app.run(debug=True, port=5000)