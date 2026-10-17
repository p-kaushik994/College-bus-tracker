import os
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime

load_dotenv()

app = Flask(__name__)
CORS(app)

# 2. Database connection helper
def get_db_connection():
    """Establishes and returns a connection to PostgreSQL."""
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=os.getenv("DB_PORT", "5432"),
        database=os.getenv("DB_NAME", "bus_tracker_db"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD"),
        cursor_factory=RealDictCursor  # Returns rows as Python dicts!
    )


# --- ROUTE 1: GET ALL BUSES ---
@app.route("/api/buses", methods=["GET"])
def get_all_buses():
    """Fetches all buses from PostgreSQL."""
    conn = None
    cur = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, bus_name, driver_id, capacity FROM buses ORDER BY id ASC;")
        buses = cur.fetchall()
        return jsonify({
            "buses": buses,
            "total": len(buses)
        }), 200
    
    except Exception as e:
        return jsonify({"error": f"Database error: {str(e)}"}), 500
    
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()


# --- ROUTE 2: GET A SPECIFIC BUS ---
@app.route("/api/buses/<int:bus_id>", methods=["GET"])
def get_single_bus(bus_id):
    """Fetches a single bus by ID from PostgreSQL."""
    conn = None
    cur = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, bus_name, driver_id, capacity FROM buses WHERE id = %s;", (bus_id,))
        bus = cur.fetchone()
        if not bus:
            return jsonify({"error": f"Bus {bus_id} not found"}), 404
        return jsonify({"bus": bus}), 200
    except Exception as e:
        return jsonify({"error": f"Database error: {str(e)}"}), 500
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()


# --- ROUTE 3: CREATE A NEW BUS ---
@app.route("/api/buses", methods=["POST"])
def create_bus():
    """Inserts a new bus into PostgreSQL."""
    data = request.get_json()
    if not data or "bus_name" not in data:
        return jsonify({"error": "'bus_name' is required"}), 400
    bus_name = data["bus_name"]
    capacity = data.get("capacity", 50)
    conn = None
    cur = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # INSERT and immediately retrieve the newly generated row using RETURNING *
        cur.execute(
            "INSERT INTO buses (bus_name, capacity) VALUES (%s, %s) RETURNING id, bus_name, driver_id, capacity;",
            (bus_name, capacity)
        )
        new_bus = cur.fetchone()
        
        # Permanently commit to disk!
        conn.commit()
        return jsonify({
            "message": "Bus created successfully in database",
            "bus": new_bus
        }), 201
    except Exception as e:
        if conn:
            conn.rollback()
        return jsonify({"error": f"Database error: {str(e)}"}), 500
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

# # --- ROUTE 4: DRIVER SENDS GPS COORDINATES ---
# @app.route("/api/buses/<int:bus_id>/location", methods=["POST"])
# def update_bus_location(bus_id):
#     """
#     Called by the Driver App to transmit live GPS coordinates.
#     """
#     # 1. Make sure the bus actually exists in our fleet
#     if bus_id not in BUSES:
#         return jsonify({"error": f"Bus {bus_id} does not exist in the fleet"}), 404

#     # 2. Extract JSON payload
#     data = request.get_json()

#     # 3. Input Validation
#     if not data or "latitude" not in data or "longitude" not in data:
        
#         return jsonify({"error": "'latitude' and 'longitude' are required fields"}), 400

#     try:
#         lat = float(data["latitude"])
#         lng = float(data["longitude"])
#         speed = float(data.get("speed", 0.0))

#     except (ValueError, TypeError):

#         return jsonify({"error": "Latitude, longitude, and speed must be valid numbers"}), 400

#     # 4. Save the latest location record with an ISO timestamp
#     location_record = {
#         "bus_id": bus_id,
#         "latitude": lat,
#         "longitude": lng,
#         "speed": speed,
#         "updated_at": datetime.now().isoformat()
#     }
#     BUS_LOCATIONS[bus_id] = location_record

#     return jsonify({
#         "message": "Location updated successfully",
#         "location": location_record
#     }), 201


# # --- ROUTE 5: STUDENT CHECKS LIVE LOCATION ---
# @app.route("/api/buses/<int:bus_id>/location", methods=["GET"])
# def get_bus_location(bus_id):
#     """
#     Called by the Student App to view where the bus is right now.
#     """
#     # 1. Check if bus exists
#     if bus_id not in BUSES:
#         return jsonify({"error": f"Bus {bus_id} not found"}), 404

#     # 2. Check if the driver has transmitted any location yet
#     if bus_id not in BUS_LOCATIONS:
#         return jsonify({
#             "bus_id": bus_id,
#             "status": "offline",
#             "message": "Bus has not transmitted any location data yet"
#         }), 404

#     # 3. Return the latest live location
#     return jsonify({
#         "bus_id": bus_id,
#         "status": "live",
#         "location": BUS_LOCATIONS[bus_id]
 #   }), 200

if __name__ == "__main__":
    app.run(debug=True, port=5000)