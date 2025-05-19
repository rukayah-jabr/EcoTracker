import os
import re
from datetime import datetime

import requests
from dotenv import load_dotenv

from eco_tracker import product
from eco_tracker.erp_integration import exceptions
from eco_tracker.erp_integration.fetch_data_interface import Data, DataFetcher

load_dotenv()

class Odoo(DataFetcher):
    def __init__(self, api_base_url: str):
        # Odoo database authorization fields
        self.database = "ecotracker"
        self.username = 'admin'
        self.password = os.getenv("ODOO_PASSWORD")
        self.delivery_address = "Stadtwerkestr. 2 Amstetten 3300 AT"

        # Odoo API request settings; session_id is provided from
        # successful authorization and is REQUIRED to make requests
        self.session_id = None
        self.api_base_url = api_base_url
        self.headers= {"Content-Type": "application/json"}

    def authenticate(self) -> bool:
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
        return True

    def get_items(self, start_date: datetime | None = None, end_date: datetime | None = None) -> list:
        url = self.api_base_url + "/web/dataset/call_kw/stock.move/search_read"
        data = {
            "jsonrpc": "2.0",
            "params": {
                "model": "stock.move",
                "method": "search_read",
                "args": [[]],
                "kwargs": {
                    "fields": ["date", "partner_id", "name", "product_uom", "product_uom_qty", "price_unit"],
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
        result = result['result']
        
        result = self._filter_by_date(result, start_date, end_date)
        
        return result
    
    def _filter_by_date(self, items: list, start_date: datetime | None, end_date: datetime | None) -> list:
        if start_date:
            start_date_str = start_date.strftime("%Y-%m-%d")
            items = list(filter(lambda item: item['date'] >= start_date_str, items))
        if end_date:
            end_date_str = end_date.strftime("%Y-%m-%d")
            items = list(filter(lambda item: item['date'] <= end_date_str, items))
        
        return items

    def get_supplier_address(self, supplier_id: int) -> list:
        url = self.api_base_url + "/web/dataset/call_kw/res.partner/search_read"
        data = {
            "jsonrpc": "2.0",
            "params": {
                "model": "res.partner",
                "method": "search_read",
                "args": [[["id", "=", supplier_id]]],
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
        
    def standardize_unit(self, unit_type: str) -> str | None:

        match unit_type.upper():
            case "STK":
                return 'number'
            case "LT":
                return 'liter'
            case "STD":
                return 'hour'
            case "PA":
                return 'number'

        raise NotImplementedError

    # Implemented function used in FetchDataFilter
    def fetch_data_from_source(self, start_date: datetime | None = None, end_date: datetime | None = None) -> Data:
        self.authenticate()

        # Initialize empty data object
        data = Data("odoo", [])

        # Get data
        results = self.get_items(start_date, end_date)

        # Standardize data to match product schema
        for item in results:

            # Clean address
            address = self.get_supplier_address(item['id'])
            address = address[0]
            standardized_address = product.Address(
                street = re.split(r'\s{2,}', address['street'])[1], # remove the company name from street address by splitting on 2+ spaces
                city = address['city'],
                zip = address['zip'],
                country = address['country_id']
            )

            # Standarized unit
            unit = self.standardize_unit(item['product_uom'])

            standardized_item = product.Product(
                    delivered_date = item['date'],
                    description = item['name'],
                    unit = unit or "number",
                    quantity = item['product_uom_qty'],
                    unit_price = item['price_unit'],
                    supplier = item['partner_id'][1],
                    supplier_address= standardized_address,
                    delivery_address = product.Address(
                        street = "Stadtwerkestr. 2",
                        city = "Amstetten",
                        zip = "3300",
                        country = "AT"
                    ),
                    climatiq_categories = [],
                    climatiq_matched_category = None,
                    category = None,
                    emission_factor = None,
                    delivery_emission_factor = None,
                    delivery_distance = 0,
                    weight = 0,
                    delivery_transportation_type = None,
                    co2_purchase = 0,
                    co2_transport = 0,
                    failed_steps = product.FailedSteps(
                        estimate_categories = False,
                        emission_factor_fetching = False,
                        purchase_co2_calculation = False,
                        distance_estimation = False,
                        weight_estimation = False,
                        delivery_emissions_estimation = False
                    )
                )
            data.data.append(standardized_item)

        return data