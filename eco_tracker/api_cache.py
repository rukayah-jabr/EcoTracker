import hashlib
import json
import os
import sqlite3
from collections.abc import Callable
from datetime import datetime, timedelta

# Set cache expiry in seconds (e.g. 30 days = 2592000)
CACHE_EXPIRY_SECONDS = 2592000

# Connect to SQLite DB (creates it if it doesn't exist)
db_path = os.path.join(os.path.dirname(__file__), "api_cache.db")
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Create the cache table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS api_cache (
        key TEXT PRIMARY KEY,
        response TEXT,
        timestamp DATETIME
    )
''')
conn.commit()

# Generates a hashed key out of the API request URL and unique request data
# (e.g. single parameter like "product" or a request body)
def generate_cache_key(url: str, request: str) -> str:
    key_string = url + request
    return hashlib.sha256(key_string.encode()).hexdigest()

# Looks up cache records based on key, returns nothing if expired (> 30 days) and removes expired entry
def get_from_cache(key: str) -> str | None:
    cursor.execute("SELECT response, timestamp FROM api_cache WHERE key = ?", (key,))
    row = cursor.fetchone()
    if row:
        response, timestamp_str = row
        timestamp = datetime.fromisoformat(timestamp_str)
        # Check if not expired
        if datetime.now() - timestamp < timedelta(seconds=CACHE_EXPIRY_SECONDS):
            return response
        # Remove expired entry
        else:
            cursor.execute("DELETE FROM api_cache WHERE key = ?", (key,))
    return None
    
# Insert API response into cache db (adds new or replaces expired existing)
def save_to_cache(url: str, request: str, response: str):
    key = generate_cache_key(url, request)
    now = datetime.now().isoformat()
    cursor.execute(
        "INSERT OR REPLACE INTO api_cache (key, response, timestamp) VALUES (?, ?, ?)",
        (key, response, now)
    )
    conn.commit()

def cached_api_call(url:str, request: str) -> dict | None:
    key = generate_cache_key(url, request)
    cached = get_from_cache(key)

    if cached:
        return json.loads(cached)
    else:
        return None

# Temporary helper function while developing to check full cache
# def get_all_from_cache() -> list:
#      cursor.execute("SELECT key, response, timestamp FROM api_cache")
#      data = cursor.fetchall()
#      return data

def execute_or_get_from_cache(url: str, request: str) -> Callable:
    def decorator(function: Callable):
        def wrapper(*args, **kwargs):
            # Check for cached API response first; if none, make fresh API call
            cache = cached_api_call(url, request)
            if cache == None:
                response = function(*args, **kwargs)
                save_to_cache(url, request, json.dumps(response))
                return response
            else:
                return cache
        
        return wrapper
    return decorator
    