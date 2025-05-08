import sqlite3
import hashlib
import json
from datetime import datetime, timedelta

# Set cache expiry in seconds (30 days)
CACHE_EXPIRY_SECONDS = 1200

# Connect to SQLite DB (creates it if it doesn't exist)
conn = sqlite3.connect("api_cache.db")
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
            print("Removed expired cache entry")
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
    print(f"Saved response to cache: {request} ({url})")

def cached_api_call(url:str, request: str) -> dict | None:
    key = generate_cache_key(url, request)
    cached = get_from_cache(key)

    if cached:
        print(f"Found in cache! -> {request} ({url})")
        return json.loads(cached)
    else:
        print(f"Not found in cache -> {request} {url}")
        return None
    
def get_all_from_cache() -> list:
     cursor.execute("SELECT key, response, timestamp FROM api_cache")
     data = cursor.fetchall()
     return data

def remove_all_from_cache() -> None:
     cursor.execute("DELETE FROM api_cache")
     conn.commit()

# url = "http://test-api-call.com/api"
# product = "Test Product Name2"
# fake_response = ["this", "is", "a", "test2"]

# cache = cached_api_call(url, product)
# if cache == None:
#     save_to_cache(url, product, json.dumps(fake_response))
#     print("Saved to cache!")
# else:
#     print(cache)
#remove_all_from_cache()
data = get_all_from_cache()
print(data)
