-- 1. DRIVERS TABLE
CREATE TABLE IF NOT EXISTS drivers (
    driver_id SERIAL PRIMARY KEY,
    driver_name VARCHAR(100) NOT NULL,
    license VARCHAR(50),
    ph_no VARCHAR(15)
);

-- 2. BUSES TABLE
CREATE TABLE IF NOT EXISTS buses (
    id SERIAL PRIMARY KEY,
    bus_name VARCHAR(100) NOT NULL,
    driver_id INTEGER REFERENCES drivers(driver_id) ON DELETE SET NULL,
    capacity INTEGER DEFAULT 50
);

-- 3. STUDENTS TABLE
CREATE TABLE IF NOT EXISTS students (
    student_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    student_class VARCHAR(50),
    roll_no INTEGER,
    bus_id INTEGER REFERENCES buses(id) ON DELETE SET NULL
);

-- 4. BUS LOCATION HISTORY (Appends every coordinate for live display & ML training)
CREATE TABLE IF NOT EXISTS bus_location (
    id SERIAL PRIMARY KEY,
    bus_id INTEGER REFERENCES buses(id) ON DELETE CASCADE,
    latitude DOUBLE PRECISION NOT NULL,
    longitude DOUBLE PRECISION NOT NULL,
    speed DOUBLE PRECISION DEFAULT 0.0,
    recorded TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 5. INDEX FOR FAST LOOKUPS (Crucial for live tracking performance!)
CREATE INDEX IF NOT EXISTS idx_bus_location_time ON bus_location (bus_id, recorded DESC);