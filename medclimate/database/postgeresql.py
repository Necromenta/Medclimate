# database/postgresql.py
from typing import Dict, List, Optional
from datetime import datetime
import psycopg2
from psycopg2.extras import RealDictCursor
from medclimate.config.settings import DATABASE_CONFIG

class WeatherDatabase:
    """
    A class to handle interactions with the weather records database.

    This class provides methods to connect to a PostgreSQL database and perform
    operations related to weather data storage and retrieval. It uses connection
    parameters from DATABASE_CONFIG.

    Attributes:
        connection_params (dict): Database connection parameters loaded from settings

    Example:
        >>> db = WeatherDatabase()
        >>> db.create_tables()  # Set up database tables
    """
    
    def __init__(self):
        """
        Initialize database connection parameters from settings.
        Usage:
            db = WeatherDatabase()
        """
        self.connection_params = DATABASE_CONFIG

    def connect(self):
        """
        Create and return a database connection.
        Used internally by other methods.
        
        Returns:
            psycopg2 connection object
        
        Usage:
            with self.connect() as conn:
                # do something with connection
        """
        return psycopg2.connect(**self.connection_params)

    def create_tables(self):
        """
        Create the weather_records table if it doesn't exist.
        Should be run once when setting up the database.
        
        Usage:
            db = WeatherDatabase()
            db.create_tables()
        """
        create_table_query = """
        CREATE TABLE IF NOT EXISTS weather_records (
            id SERIAL PRIMARY KEY,                    -- Auto-incrementing ID
            timestamp TIMESTAMP NOT NULL,             -- When the measurement was taken
            temperature FLOAT,                        -- Temperature in Celsius
            humidity FLOAT,                           -- Humidity percentage
            precipitation FLOAT,                      -- Precipitation in mm
            location VARCHAR(100),                    -- Location name
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP  -- Record creation time
        );
        
        CREATE INDEX IF NOT EXISTS idx_weather_location_timestamp 
        ON weather_records(location, timestamp);
        """
        
        with self.connect() as conn:
            with conn.cursor() as cur:
                cur.execute(create_table_query)
            conn.commit()

    def insert_weather_record(self, record: Dict) -> int:
        """
        Insert a new weather record into the database.
        
        Args:
            record (dict): Dictionary containing weather data
                {
                    "timestamp": datetime object,
                    "temperature": float,
                    "humidity": float,
                    "precipitation": float,
                    "location": str
                }
        
        Returns:
            int: ID of the newly inserted record
        
        Usage:
            db.insert_weather_record({
                "timestamp": datetime.now(),
                "temperature": 23.5,
                "humidity": 65.0,
                "precipitation": 0.0,
                "location": "New York"
            })
        """
        query = """
        INSERT INTO weather_records (timestamp, temperature, humidity, precipitation, location)
        VALUES (%(timestamp)s, %(temperature)s, %(humidity)s, %(precipitation)s, %(location)s)
        RETURNING id;
        """
        
        with self.connect() as conn:
            with conn.cursor() as cur:
                cur.execute(query, record)
                record_id = cur.fetchone()[0]
            conn.commit()
        return record_id

    def get_records_by_location(self, location: str, start_date: Optional[datetime] = None) -> List[Dict]:
        """
        Retrieve weather records for a specific location.
        
        Args:
            location (str): Location name to filter by
            start_date (datetime, optional): Only get records after this date
        
        Returns:
            List[Dict]: List of weather records
        
        Usage:
            records = db.get_records_by_location("New York", 
                                               start_date=datetime(2024, 1, 1))
        """
        query = """
        SELECT id, timestamp, temperature, humidity, precipitation, location
        FROM weather_records
        WHERE location = %s
        """
        params = [location]
        
        if start_date:
            query += " AND timestamp >= %s"
            params.append(start_date)
            
        query += " ORDER BY timestamp DESC"
        
        with self.connect() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(query, params)
                return cur.fetchall()

    def get_average_temperatures(self, location: str, start_date: datetime, 
                               end_date: datetime) -> Dict:
        """
        Calculate temperature statistics for a location in a date range.
        
        Args:
            location (str): Location to analyze
            start_date (datetime): Start of date range
            end_date (datetime): End of date range
        
        Returns:
            Dict: Statistics including average, min, max temperatures
        
        Usage:
            stats = db.get_average_temperatures(
                "New York",
                datetime(2024, 1, 1),
                datetime(2024, 2, 1)
            )
        """
        query = """
        SELECT 
            location,
            AVG(temperature) as avg_temp,
            MIN(temperature) as min_temp,
            MAX(temperature) as max_temp,
            COUNT(*) as total_records
        FROM weather_records
        WHERE location = %s
        AND timestamp BETWEEN %s AND %s
        GROUP BY location;
        """
        
        with self.connect() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(query, (location, start_date, end_date))
                return cur.fetchone()

    def get_extreme_weather_events(self, threshold_temp: float = 35.0, 
                                 threshold_precip: float = 50.0) -> List[Dict]:
        """
        Find extreme weather events based on thresholds.
        
        Args:
            threshold_temp (float): Temperature threshold in Celsius
            threshold_precip (float): Precipitation threshold in mm
        
        Returns:
            List[Dict]: List of extreme weather records
        
        Usage:
            extreme_events = db.get_extreme_weather_events(
                threshold_temp=35.0,
                threshold_precip=50.0
            )
        """
        query = """
        SELECT *
        FROM weather_records
        WHERE temperature >= %s OR precipitation >= %s
        ORDER BY timestamp DESC;
        """
        
        with self.connect() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(query, (threshold_temp, threshold_precip))
                return cur.fetchall()

# Example usage
if __name__ == "__main__":
    # Test database connection and operations
    db = WeatherDatabase()
    
    # Create tables if they don't exist
    db.create_tables()
    
    # Insert test record
    test_record = {
        "timestamp": datetime.now(),
        "temperature": 23.5,
        "humidity": 65.0,
        "precipitation": 0.0,
        "location": "New York"
    }
    
    try:
        record_id = db.insert_weather_record(test_record)
        print(f"Successfully inserted test record with ID: {record_id}")
    except Exception as e:
        print(f"Error inserting test record: {e}")