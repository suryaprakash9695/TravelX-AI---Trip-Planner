"""
Database module for TravelX AI
Handles trip history, user preferences, and saved itineraries
"""
import sqlite3
import json
from datetime import datetime
import os

DB_PATH = "travelx_data.db"

def init_db():
    """Initialize database with required tables"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Trip history table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS trip_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source TEXT NOT NULL,
            destination TEXT NOT NULL,
            start_date TEXT NOT NULL,
            end_date TEXT NOT NULL,
            days INTEGER NOT NULL,
            itinerary TEXT NOT NULL,
            weather_data TEXT,
            route_data TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            rating INTEGER,
            notes TEXT
        )
    """)
    
    # User preferences table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_preferences (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            preference_key TEXT UNIQUE NOT NULL,
            preference_value TEXT NOT NULL,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Favorite destinations table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS favorite_destinations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            destination TEXT NOT NULL,
            reason TEXT,
            added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    conn.commit()
    conn.close()

def save_trip(source, destination, start_date, end_date, days, itinerary, weather_data=None, route_data=None):
    """Save a trip to history"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO trip_history 
        (source, destination, start_date, end_date, days, itinerary, weather_data, route_data)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        source, destination, start_date, end_date, days, itinerary,
        json.dumps(weather_data) if weather_data else None,
        json.dumps(route_data) if route_data else None
    ))
    
    trip_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return trip_id

def get_trip_history(limit=10):
    """Get recent trip history"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT * FROM trip_history 
        ORDER BY created_at DESC 
        LIMIT ?
    """, (limit,))
    
    trips = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return trips

def get_trip_by_id(trip_id):
    """Get a specific trip by ID"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM trip_history WHERE id = ?", (trip_id,))
    trip = cursor.fetchone()
    conn.close()
    
    if trip:
        trip_dict = dict(trip)
        if trip_dict.get('weather_data'):
            trip_dict['weather_data'] = json.loads(trip_dict['weather_data'])
        if trip_dict.get('route_data'):
            trip_dict['route_data'] = json.loads(trip_dict['route_data'])
        return trip_dict
    return None

def update_trip_rating(trip_id, rating, notes=None):
    """Update trip rating and notes"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        UPDATE trip_history 
        SET rating = ?, notes = ?
        WHERE id = ?
    """, (rating, notes, trip_id))
    
    conn.commit()
    conn.close()

def delete_trip(trip_id):
    """Delete a trip from history"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("DELETE FROM trip_history WHERE id = ?", (trip_id,))
    
    conn.commit()
    conn.close()

def save_preference(key, value):
    """Save or update user preference"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT OR REPLACE INTO user_preferences (preference_key, preference_value, updated_at)
        VALUES (?, ?, CURRENT_TIMESTAMP)
    """, (key, value))
    
    conn.commit()
    conn.close()

def get_preference(key, default=None):
    """Get user preference"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("SELECT preference_value FROM user_preferences WHERE preference_key = ?", (key,))
    result = cursor.fetchone()
    conn.close()
    
    return result[0] if result else default

def add_favorite_destination(destination, reason=None):
    """Add destination to favorites"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO favorite_destinations (destination, reason)
        VALUES (?, ?)
    """, (destination, reason))
    
    conn.commit()
    conn.close()

def get_favorite_destinations():
    """Get all favorite destinations"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM favorite_destinations ORDER BY added_at DESC")
    favorites = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return favorites

def get_trip_statistics():
    """Get trip statistics"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    stats = {}
    
    # Total trips
    cursor.execute("SELECT COUNT(*) FROM trip_history")
    stats['total_trips'] = cursor.fetchone()[0]
    
    # Total days traveled
    cursor.execute("SELECT SUM(days) FROM trip_history")
    result = cursor.fetchone()[0]
    stats['total_days'] = result if result else 0
    
    # Most visited destination
    cursor.execute("""
        SELECT destination, COUNT(*) as count 
        FROM trip_history 
        GROUP BY destination 
        ORDER BY count DESC 
        LIMIT 1
    """)
    result = cursor.fetchone()
    stats['most_visited'] = result[0] if result else None
    
    # Average trip rating
    cursor.execute("SELECT AVG(rating) FROM trip_history WHERE rating IS NOT NULL")
    result = cursor.fetchone()[0]
    stats['avg_rating'] = round(result, 1) if result else None
    
    conn.close()
    return stats

# Initialize database on module import
init_db()
