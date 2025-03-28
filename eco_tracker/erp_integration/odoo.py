import json
import pandas as pd
from dotenv import load_dotenv
import os
import requests

from eco_tracker.erp_integration.fetch_data_interface import DataFetcher, Data

load_dotenv()

class Odoo(DataFetcher):
    def __init__(self):
        # Odoo database authorization fields
        self.database = "ecotracker"
        self.username = 'admin'
        self.password = os.getenv("ODOO_PASSWORD")

        # Odoo API request settings; session_id is provided from
        # successful authorization and is REQUIRED to make requests
        self.session_id = None
        self.api_base_url = 'http://localhost:8069'
        self.headers= {"Content-Type": "application/json"}

    def authenticate(self):
        url = self.api_base_url + "/web/session/authenticate"
        data = {
            "jsonrpc": "2.0",
            "params": {
                "db": self.database,
                "login": self.username,
                "password": self.password
            }
        }
        body = json.dumps(data)

        try:
            response = requests.post(url=url, headers=self.headers, data=body)
            response.raise_for_status() # Raise HTTPError if not successful
            
            # Parse result and store the session_id
            result = response.json()
            self.session_id = result['result']['session_id']
            print(f"Authenticated with session ID: {self.session_id}")
        except requests.exceptions.HTTPError as err:
            print(f"Authentication failed: {err}")

    def get_items(self) -> list:
        url = self.api_base_url + "/web/dataset/call_kw/stock.move/search_read"
        data = {
            "jsonrpc": "2.0",
            "params": {
                "model": "stock.move",
                "method": "search_read",
                "args": [[]],
                "kwargs": {
                    "fields": ["date", "partner_id", "name", "product_uom_qty", "price_unit"],
                },
                "context": {
                    "session_id": self.session_id
                }
           }
        }
        body = json.dumps(data)

        try:
            response = requests.post(url=url, headers=self.headers, data=body)
            response.raise_for_status() # Raise HTTPError if not successful
            
            # Parse result and return list of delivered items
            result = response.json()
            return result['result']
        except requests.exceptions.HTTPError as err:
            print(f"Request failed: {err}")

    # !! Does not completely work yet !!
    def get_supplier_address(self, supplier_id) -> list:
        url = self.api_base_url + "/web/dataset/call_kw/res.partner/search_read"
        data = {
            "jsonrpc": "2.0",
            "params": {
                "model": "res.partner",
                "method": "search_read",
                "args": [[]], # TO DO: get this filter to work returning a single id as argument
                "kwargs": {
                    "fields": ["name", "street", "zip", "city", "country_id"],
                },
                "context": {
                    "session_id": self.session_id
                }
           }
        }
        body = json.dumps(data)

        try:
            response = requests.post(url=url, headers=self.headers, data=body)
            response.raise_for_status() # Raise HTTPError if not successful
            
            # Parse result and return supplier location
            result = response.json()
            return result['result']
        except requests.exceptions.HTTPError as err:
            print(f"Request failed: {err}")

    # Implemented function used in FetchDataFilter
    def fetch_data_from_source(self) -> Data:
        self.authenticate()

        # Initialize empty data object
        data = Data("odoo", {})

        # Get data
        data.data = self.get_items()

        # TO DO: standardize data to match product schema
        return data

