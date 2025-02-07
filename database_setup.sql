-- -- Create the weather database
-- CREATE DATABASE weather_monitoring;

-- -- Connect to the weather database
-- \c weather_monitoring

-- -- Create the weather_data table
-- CREATE TABLE weather_data (
--     id SERIAL PRIMARY KEY,
--     city VARCHAR(100) NOT NULL,
--     temperature NUMERIC(5,2) NOT NULL,
--     humidity INTEGER NOT NULL,
--     weather_description VARCHAR(200) NOT NULL,
--     timestamp TIMESTAMP NOT NULL
-- );

-- -- Create an index on the timestamp column for better query performance
-- CREATE INDEX idx_timestamp ON weather_data(timestamp);

-- -- Create an index on the city column for faster filtering
-- CREATE INDEX idx_city ON weather_data(city);


-- -- Create the metabase database
-- CREATE DATABASE metabase;

-- -- Connect to weather_monitoring database
-- \c weather_monitoring;

-- -- Create the weather_data table
-- CREATE TABLE IF NOT EXISTS weather_data (
--     id SERIAL PRIMARY KEY,
--     city VARCHAR(100) NOT NULL,
--     temperature NUMERIC(5,2) NOT NULL,
--     humidity INTEGER NOT NULL,
--     weather_description VARCHAR(200) NOT NULL,
--     timestamp TIMESTAMP NOT NULL
-- );

-- -- Create indexes
-- CREATE INDEX IF NOT EXISTS idx_timestamp ON weather_data(timestamp);
-- CREATE INDEX IF NOT EXISTS idx_city ON weather_data(city);

-- Create the metabase database
CREATE DATABASE metabase;

-- Grant privileges to weather_user for Metabase
\c metabase;
GRANT ALL PRIVILEGES ON DATABASE metabase TO weather_user;

-- Connect to weather_monitoring database
\c weather_monitoring;

-- Grant privileges to weather_user for weather_monitoring (if needed)
GRANT ALL PRIVILEGES ON DATABASE weather_monitoring TO weather_user;

-- Create the weather_data table
CREATE TABLE IF NOT EXISTS weather_data (
    id SERIAL PRIMARY KEY,
    city VARCHAR(100) NOT NULL,
    temperature NUMERIC(5,2) NOT NULL,
    humidity INTEGER NOT NULL,
    weather_description VARCHAR(200) NOT NULL,
    timestamp TIMESTAMP NOT NULL
);

-- Create indexes
CREATE INDEX IF NOT EXISTS idx_timestamp ON weather_data(timestamp);
CREATE INDEX IF NOT EXISTS idx_city ON weather_data(city);
