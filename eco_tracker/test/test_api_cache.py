import json
import sqlite3

import pytest

from eco_tracker import api_cache

url = "http://test-api-call.com/api"
request = "Test Request"
response = ["this", "is", "a", "test"]

def test_get_db_connection():
    db_connection = api_cache.get_db_connection()
    cursor = db_connection.cursor()
    cursor.execute("SELECT 1")
    row = cursor.fetchone()
    assert row is not None
    
def test_get_db_cursor():
    with api_cache.get_db_cursor() as cursor:
        cursor.execute("SELECT 1")
        row = cursor.fetchone()
        assert row is not None

def test_generate_cache_key():
    assert api_cache.generate_cache_key(url, request) is not None

def test_api_cache_success():
    cache = api_cache.cached_api_call(url, request)
    if cache == None:
        api_cache.save_to_cache(url, request, json.dumps(response))
        assert api_cache.cached_api_call(url, request) is not None
    else:
        assert cache is not None

# test if error when passing a non-string
def test_api_cache_error():
    cache = api_cache.cached_api_call(url, request)
    if cache == None:
        with pytest.raises(sqlite3.ProgrammingError):
            api_cache.save_to_cache(url, request, response)