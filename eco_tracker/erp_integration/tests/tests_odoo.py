from eco_tracker.erp_integration.odoo import Odoo
import pytest


@pytest.fixture
def odoo_instance() -> Odoo:
		return Odoo()

@pytest.fixture
def odoo_authenticated_instance(odoo_instance) -> Odoo:
		odoo_instance.authenticate()
		return odoo_instance

# ATTENTION: ecotracker-odoo has to run in order to successfully run the tests!
def test_authentication(odoo_instance):
		odoo_instance.authenticate()
		assert odoo_instance.session_id is not None

def test_get_items(odoo_authenticated_instance):
		items = odoo_authenticated_instance.get_items()
		assert len(items) > 0

def test_get_supplier_address(odoo_authenticated_instance):
		address = odoo_authenticated_instance.get_supplier_address(300022)
		assert address is not None

def test_fetch_data_from_source(odoo_authenticated_instance):
		data = odoo_authenticated_instance.fetch_data_from_source()
		assert data is not None
		assert len(data.data) > 0
		assert data.source == "odoo"