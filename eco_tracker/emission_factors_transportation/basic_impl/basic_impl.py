
from eco_tracker.emission_factors_transportation.emission_factors_transportation_interface import EmissionFactorsTransportationFetcher
from eco_tracker.product import EmissionFactor


class BasicEmissionFactorsTransportationFetcher(EmissionFactorsTransportationFetcher):

  def fetch_emission_factors_transportation(self, transportation_type: str = "road") -> EmissionFactor:
    return EmissionFactor(
      co2e=0.000062,
      co2e_unit="kg",
      activity_unit="kg-km",
      name="Basic Emission Factor for Road Transportation",
      description="Basic Emission Factor for Road Transportation taken from https://www.ecta.com/wp-content/uploads/2021/03/ECTA-CEFIC-GUIDELINE-FOR-MEASURING-AND-MANAGING-CO2-ISSUE-1.pdf"
    )