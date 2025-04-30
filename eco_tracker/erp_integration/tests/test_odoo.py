import pytest
from eco_tracker.erp_integration.odoo import Odoo
from eco_tracker.erp_integration import exceptions


def test_odoo():
    odoo = Odoo()
    assert odoo is not None

def test_odoo_authentication():
    assert Odoo().authenticate() is True

def test_odoo_get_items():
    odoo = Odoo()
    odoo.authenticate()
    items = odoo.get_items()
    assert items is not None

def test_odoo_get_supplier_address():
    odoo = Odoo()
    odoo.authenticate()
    address = odoo.get_supplier_address(475)
    assert address is not None

    with pytest.raises(exceptions.SupplierNotFound):
        odoo.get_supplier_address(000)

def test_odoo_standardize_unit():
    odoo = Odoo()
    assert odoo.standardize_unit("STK") == 'number'

def test_odoo_fetch_data_from_source():
    odoo = Odoo()
    data = odoo.fetch_data_from_source
    assert data is not None