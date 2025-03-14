import requests
from dataclasses import dataclass

from .exceptions import EmissionFactorInfoNotFound
from .unit import return_unit
from eco_tracker.emission_factors import exceptions

@dataclass
class EmissionFactorInfo:
    activity_id: str
    id: str
    unit_type: str
    unit: str
    source_lca_activity: str
    data_version: str

@dataclass
class EmissionFactor:
    co2e: float
    co2e_unit: str
    activity_unit: str


def set_correct_unit_in_req_body(unit_type: str, req_body: dict):
    unit = return_unit(unit_type)
    for key, value in unit.items():
        req_body['parameters'][key] = value

# This function is necessary,
# since even if we estimated the emission factor in EUR and the result will be correctly scaled (e.g. from CAD)
# the unit in the response will be still the original unit (e.g. CAD) with the exchange rate applied.
# It means the response unit is (CAD, 1.55) instead of (EUR, 1).
def get_our_activity_unit(unit_type: str) -> str:
    activity_unit = ""

    unit = return_unit(unit_type)
    last_key = list(unit.keys())[-1]
    for key, value in unit.items():
        activity_unit += value
        if key == last_key:
            break
        activity_unit += "-"

    return activity_unit

class Climatiq:
    def __init__(self, api_key: str):
        self.api_key = api_key

        # You must always specify your AUTH token in the "Authorization" header like this.
        self.authorization_headers = {"Authorization": f"Bearer {self.api_key}"}

    # Example from climatiq tutorials: https://www.climatiq.io/docs/guides/how-tos/using-python
    def fetch_emission_factor_info(self, query, data_version = '^20') -> EmissionFactorInfo :
        url = "https://api.climatiq.io/data/v1/search"

        query_params = {
            "query": query,
            "data_version": data_version,
        }

        found_emission_factors = requests.get(url, params=query_params, headers=self.authorization_headers).json()
        if found_emission_factors['total_results'] == 0:
            raise EmissionFactorInfoNotFound(query)


        best_matching_factor = found_emission_factors['results'][0]

        return EmissionFactorInfo(
            activity_id=best_matching_factor['activity_id'],
            id=best_matching_factor['id'],
            unit_type=best_matching_factor['unit_type'],
            unit=best_matching_factor['unit'],
            source_lca_activity=best_matching_factor['source_lca_activity'],
            data_version=data_version
        )

    def fetch_emission_factor(self, ef_info: EmissionFactorInfo) -> EmissionFactor:
        url = 'https://api.climatiq.io/data/v1/estimate'

        # https://www.climatiq.io/docs/api-reference/estimate
        req_body = {
            "emission_factor": {
                "id": ef_info.id,
            },
            "parameters": {
                f"{ef_info.unit_type.lower()}": 1
            }
        }

        set_correct_unit_in_req_body(ef_info.unit_type, req_body)

        response = requests.post(url, json=req_body, headers=self.authorization_headers)
        if not response.ok:
            raise exceptions.EmissionFactorNotFound(ef_info.activity_id)

        response_json = response.json()
        return EmissionFactor(
            co2e=response_json['co2e'],
            co2e_unit=response_json['co2e_unit'],
            activity_unit=get_our_activity_unit(ef_info.unit_type),
        )
