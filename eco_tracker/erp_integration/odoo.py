import json
from dotenv import load_dotenv
import os
import requests

from eco_tracker.erp_integration.fetch_data_interface import DataFetcher, Data
from eco_tracker.erp_integration import exceptions

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

        response = requests.post(url=url, headers=self.headers, json=data)

        if not response.ok:
            raise exceptions.AuthenticationFailed(url=url)
        
        # Parse result and store the session_id
        result = response.json()
        self.session_id = result['result']['session_id']
        print(f"Authenticated with session ID: {self.session_id}")

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

        response = requests.post(url=url, headers=self.headers, json=data)

        if not response.ok:
            raise exceptions.FetchingDataFailed(url=url)
        
        # Parse result and return list of delivered items
        result = response.json()
        return result['result']

    # !! Does not completely work yet !!
    def get_supplier_address(self, supplier_id: int) -> list:
        url = self.api_base_url + "/web/dataset/call_kw/res.partner/search_read"
        data = {
            "jsonrpc": "2.0",
            "params": {
                "model": "res.partner",
                "method": "search_read",
                "args": [[["ref", "=", supplier_id]]],
                "kwargs": {
                    "fields": ["name", "street", "zip", "city", "country_id"],
                },
                "context": {
                    "session_id": self.session_id
                }
           }
        }

        response = requests.post(url=url, headers=self.headers, json=data)

        if not response.ok:
            raise exceptions.FetchingDataFailed(url=url)
        
        # Parse result and return supplier location
        result = response.json()
        supplier_address = result['result']

        if len(supplier_address) > 0:
            return result['result']
        else:
            raise exceptions.SupplierNotFound(supplier_id)

    # Implemented function used in FetchDataFilter
    def fetch_data_from_source(self) -> Data:
        self.authenticate()

        # Initialize empty data object
        data = Data("odoo", {})

        # Get data
        data.data = self.get_items()

        # TODO: standardize data to match product schema
        return data