import eco_tracker.emission_factors.climatiq as climatiq

import os
import pytest
from dotenv import load_dotenv

from eco_tracker.emission_factors.exceptions import EmissionFactorNotFound


@pytest.fixture
def api_key() -> str:
    load_dotenv()
    return os.getenv("CLIMATIQ_API_KEY")

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
        data_version='^20',
    )

def test_fetch_emission_factor_info_not_found(climatiq_instance):
    with pytest.raises(climatiq.EmissionFactorInfoNotFound):
        climatiq_instance.fetch_emission_factor_info(query="air filter", data_version="^20")

def test_fetch_emission_factor_info_success(climatiq_instance):
    best_matching_factor = climatiq_instance.fetch_emission_factor_info(query="air purification", data_version="^20")
    assert best_matching_factor.activity_id is not None
    assert best_matching_factor.id is not None
    assert best_matching_factor.unit_type is not None
    assert best_matching_factor.unit is not None
    assert best_matching_factor.source_lca_activity is not None
    assert best_matching_factor.data_version is not None

def test_fetch_emission_factor_factor_not_found(climatiq_instance, emission_factor_info):
    emission_factor_info.activity_id = 'not-correct'
    emission_factor_info.id = 'not-correct'
    with pytest.raises(EmissionFactorNotFound):
        climatiq_instance.fetch_emission_factor(emission_factor_info)

# success
def test_fetch_emission_factor_success(climatiq_instance, emission_factor_info):
    emission_factor = climatiq_instance.fetch_emission_factor(emission_factor_info)
    assert emission_factor.co2e is not None