from datetime import datetime, timedelta

import pytest

from eco_tracker.erp_integration import exceptions
from eco_tracker.erp_integration.odoo import Odoo


@pytest.fixture
def odoo_instance() -> Odoo:
    return Odoo("http://localhost:8069")

@pytest.fixture
def odoo_authenticated_instance(odoo_instance) -> Odoo:
    odoo_instance.authenticate()
    return odoo_instance

# ATTENTION: ecotracker-odoo has to run in order to successfully run the tests!
def test_odoo(odoo_instance):
    assert odoo_instance is not None

def test_odoo_authentication(odoo_instance):
    assert odoo_instance.authenticate() is True
    assert odoo_instance.session_id is not None

def test_odoo_get_items_all(odoo_authenticated_instance):
    items = odoo_authenticated_instance.get_items()
    assert len(items) > 0
  
def test_odoo_get_items_filtered_by_date_range(odoo_authenticated_instance):
    items = odoo_authenticated_instance.get_items(datetime.fromisoformat("2024-08-22"), datetime.fromisoformat("2024-08-22"))
    assert len(items) > 0

def test_odoo_get_supplier_address(odoo_authenticated_instance):
    address = odoo_authenticated_instance.get_supplier_address(475)
    assert address is not None

    with pytest.raises(exceptions.SupplierNotFound):
        odoo_authenticated_instance.get_supplier_address(000)

def test_odoo_standardize_unit(odoo_instance):
    assert odoo_instance.standardize_unit("STK") == 'number'

def test_odoo_fetch_data_from_source(odoo_instance):
    data = odoo_instance.fetch_data_from_source()
    assert data is not None
    assert len(data.data) > 0
    assert data.source == "odoo"

def test_odoo_fetch_data_from_source_filtered_by_date_range(odoo_instance):
    start_date_str = "2024-08-22"
    end_date_str = "2024-08-22"
    start_date = datetime.fromisoformat(start_date_str)
    end_date = datetime.fromisoformat(end_date_str)
    
    data = odoo_instance.fetch_data_from_source(start_date, end_date)
    assert data is not None
    assert len(data.data) > 0
    assert data.source == "odoo"
    
    for item in data.data:
        assert item.delivered_date >= start_date_str
        assert item.delivered_date <= end_date_str
