import os
from unittest.mock import patch

import pytest
import requests
from dotenv import load_dotenv

import eco_tracker.emission_factors.climatiq.climatiq as climatiq
from eco_tracker.emission_factors.exceptions import EmissionFactorInfoNotFound, EmissionFactorNotFound


@pytest.fixture
def api_key() -> str:
    load_dotenv()
    api_key = os.getenv("CLIMATIQ_API_KEY")
    if api_key is None:
        raise ValueError("CLIMATIQ_API_KEY is not set")
    return api_key

@pytest.fixture
def climatiq_instance(api_key) -> climatiq.Climatiq:
    return climatiq.Climatiq(api_key=api_key)

@pytest.fixture
def emission_factor_info():
    return climatiq.EmissionFactorInfo(
        activity_id='machinery-type_industrial_and_commercial_fans_blowers_and_air_purification_equipment',
        id='7b1e48e4-d596-4b2f-946f-118dab178dbb',
        unit_type='Money',
        unit='kg/cad',
        source_lca_activity='cradle_to_gate',
        data_version='^21',
        name='Air purification',
        description='Air purification'
    )

def test_fetch_emission_factor_info_not_found(climatiq_instance):
    with pytest.raises(EmissionFactorInfoNotFound):
        climatiq_instance.fetch_emission_factor_info(query="air filter", unit_type="Money", data_version="^21")

def test_fetch_emission_factor_info_success(climatiq_instance):
    best_matching_factor = climatiq_instance.fetch_emission_factor_info(query="air purification", unit_type="Money", data_version="^21")
    assert best_matching_factor.activity_id is not None
    assert best_matching_factor.id is not None
    assert best_matching_factor.unit_type is not None
    assert best_matching_factor.unit is not None
    assert best_matching_factor.source_lca_activity is not None
    assert best_matching_factor.data_version is not None
    assert best_matching_factor.name is not None
    assert best_matching_factor.description is not None

def test_fetch_emission_factor_info_success_another(climatiq_instance):
    best_matching_factor = climatiq_instance.fetch_emission_factor_info(query="laptop", unit_type="Number", data_version="^21")
    assert best_matching_factor.activity_id is not None

def test_fetch_emission_factor_info_request_exception(climatiq_instance):
    with patch('requests.get') as mock_get:
        # time out exception
        mock_get.side_effect = requests.exceptions.RequestException("Mocked request exception")
        with pytest.raises(Exception):
            climatiq_instance.fetch_emission_factor_info(query="laptop", unit_type="Number", data_version="^21")

def test_fetch_emission_factor_info_error_code(climatiq_instance):
    with patch('requests.get') as mock_get:
        mock_get.return_value.status_code = 400
        mock_get.return_value.ok = False
        with pytest.raises(EmissionFactorInfoNotFound):
            climatiq_instance.fetch_emission_factor_info(query="laptop", unit_type="Number", data_version="^21")

def test_fetch_emission_factor_info_no_results(climatiq_instance):
    with patch('requests.get') as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {"total_results": 0}
        with pytest.raises(EmissionFactorInfoNotFound):
            climatiq_instance.fetch_emission_factor_info(query="laptop", unit_type="Number", data_version="^21")

@patch('eco_tracker.api_cache.cached_api_call')
@patch('requests.post')
def test_fetch_emission_factor_error_code(mock_post, mock_cached_api_call, climatiq_instance, emission_factor_info):
    mock_cached_api_call.return_value = None
    mock_post.return_value.status_code = 400
    mock_post.return_value.ok = False
    with pytest.raises(EmissionFactorNotFound):
        climatiq_instance.fetch_emission_factor(emission_factor_info)
            
def test_fetch_emission_factor_factor_not_found(climatiq_instance, emission_factor_info):
    emission_factor_info.activity_id = 'not-correct'
    emission_factor_info.id = 'not-correct'
    with pytest.raises(EmissionFactorNotFound):
        climatiq_instance.fetch_emission_factor(emission_factor_info)

# success
def test_fetch_emission_factor_success(climatiq_instance, emission_factor_info):
    emission_factor = climatiq_instance.fetch_emission_factor(emission_factor_info)
    assert emission_factor.co2e is not None

def test_fetch_emission_factor_from_query_number_unit(climatiq_instance):
    emission_factor = climatiq_instance.fetch_emission_factor_from_query(query="air purification", unit="number", data_version="^21")
    assert emission_factor.co2e is not None
    assert emission_factor.co2e_unit is not None
    assert emission_factor.activity_unit is not None

# there is no emission factor for this query with unit_type "Volume", only "Time"
def test_fetch_emission_factor_from_query_time_unit(climatiq_instance):
    query = "Homeworking - Office Equipment"
    unit = "liter"
    
    with pytest.raises(EmissionFactorNotFound):
        climatiq_instance.fetch_emission_factor_from_query(query=query, unit=unit)
    
    unit = "hour"
    emission_factor = climatiq_instance.fetch_emission_factor_from_query(query=query, unit=unit)
    assert emission_factor.co2e is not None
    assert emission_factor.co2e_unit is not None
    assert emission_factor.activity_unit is not None
    
# there is no emission factor for this query with unit_type "Number", only "Volume"
def test_fetch_emission_factor_from_query_volume_unit(climatiq_instance):
    query = "Ethanol - 100%"
    unit = "number"
    
    with pytest.raises(EmissionFactorNotFound):
        climatiq_instance.fetch_emission_factor_from_query(query=query, unit=unit)
    
    unit = "liter"
    emission_factor = climatiq_instance.fetch_emission_factor_from_query(query=query, unit=unit)
    assert emission_factor.co2e is not None
    assert emission_factor.co2e_unit is not None
    assert emission_factor.activity_unit is not None
