import os

from dotenv import load_dotenv

from eco_tracker.categorization.breact.breact_categorization import BreactCategorizer
from eco_tracker.categorization.breact.breact_reorder_categorization import CategoryReorderFilter
from eco_tracker.categorization.categorizer_interface import Categorizer
from eco_tracker.categorization.climatiq_categorization_filter import ClimatiqCategorizerFilter
from eco_tracker.categorization.groq.groq_categorizer import ClimatiqCategorizer
from eco_tracker.delivery_emissions.delivery_emissions_estimator_filter import DeliveryEmissionsEstimatorFilter
from eco_tracker.delivery_emissions.distance_based_method.distance_based_method import DistanceBasedMethod
from eco_tracker.distance_estimation.distance_estimation_filter import DistanceEstimationFilter
from eco_tracker.distance_estimation.distance_estimation_interface import DistanceEstimator
from eco_tracker.distance_estimation.open_route_service.open_route_service import OpenRouteService
from eco_tracker.emission_factors.climatiq.climatiq import Climatiq
from eco_tracker.emission_factors.emission_factors_filter import EmissionFactorsFilter
from eco_tracker.emission_factors.emission_factors_interface import EmissionFactorsFetcher
from eco_tracker.emission_factors_transportation.basic_impl.basic_impl import BasicEmissionFactorsTransportationFetcher
from eco_tracker.emission_factors_transportation.emission_factors_transportation_filter import EmissionFactorsTransportationFilter
from eco_tracker.emission_factors_transportation.emission_factors_transportation_interface import EmissionFactorsTransportationFetcher
from eco_tracker.erp_integration.fetch_data_filter import FetchDataFilter
from eco_tracker.erp_integration.fetch_data_interface import DataFetcher
from eco_tracker.erp_integration.odoo import Odoo
from eco_tracker.pipeline import Pipeline
from eco_tracker.product import Product
from eco_tracker.purchase_emissions.basic_estimator.basic_estimator import BasicPurchaseEmissionsEstimator
from eco_tracker.purchase_emissions.purchase_estimator_filter import PurchaseEmissionsEstimatorFilter
from eco_tracker.purchase_emissions.purchase_estimator_interface import PurchaseEmissionsEstimator
from eco_tracker.utils.log import get_logger
from eco_tracker.weight_estimation.groq.groq import GroqWeightEstimator
from eco_tracker.weight_estimation.weight_estimation_filter import WeightEstimationFilter
from eco_tracker.weight_estimation.weight_estimation_interface import WeightEstimator

logger = get_logger("main")

load_dotenv()
CLIMATIQ_API_KEY=os.getenv("CLIMATIQ_API_KEY")
LLM_API_KEY=os.getenv("LLM_API_KEY")
BREACT_API_KEY=os.getenv("BREACT_API_KEY")
OPEN_ROUTE_SERVICE_API_KEY=os.getenv("OPEN_ROUTE_SERVICE_API_KEY")

def main():
    
    if not CLIMATIQ_API_KEY:
        raise ValueError("CLIMATIQ_API_KEY is not set")

    if not LLM_API_KEY:
        raise ValueError("LLM_API_KEY is not set")

    if not BREACT_API_KEY:
        raise ValueError("BREACT_API_KEY is not set")

    if not OPEN_ROUTE_SERVICE_API_KEY:
        raise ValueError("OPEN_ROUTE_SERVICE_API_KEY is not set")

    odoo: DataFetcher = Odoo(api_base_url="http://localhost:8069")    
    groq_categorizer: Categorizer = ClimatiqCategorizer(LLM_API_KEY)
    breact_categorizer: Categorizer = BreactCategorizer(BREACT_API_KEY)
    climatiq: EmissionFactorsFetcher = Climatiq(CLIMATIQ_API_KEY)
    basic_purchase_estimator: PurchaseEmissionsEstimator = BasicPurchaseEmissionsEstimator()
    
    open_route_distance_estimator: DistanceEstimator = OpenRouteService(OPEN_ROUTE_SERVICE_API_KEY)
    emission_factors_transportation_fetcher: EmissionFactorsTransportationFetcher = BasicEmissionFactorsTransportationFetcher()
    groq_weight_estimator: WeightEstimator = GroqWeightEstimator(LLM_API_KEY)
    distance_based_method: DistanceBasedMethod = DistanceBasedMethod()

    # Define product pipeline
    pipeline: Pipeline[Product] = Pipeline(
        ClimatiqCategorizerFilter(groq_categorizer),
        CategoryReorderFilter(breact_categorizer),
        EmissionFactorsFilter(climatiq, "^21"),
        PurchaseEmissionsEstimatorFilter(basic_purchase_estimator),
        
        DistanceEstimationFilter(open_route_distance_estimator),
        EmissionFactorsTransportationFilter(emission_factors_transportation_fetcher),
        WeightEstimationFilter(groq_weight_estimator),
        DeliveryEmissionsEstimatorFilter(distance_based_method)
    )

    # Get data
    odoo_data = odoo.fetch_data_from_source()

    # Run pipeline over each item in data
    # TODO: adapt the FetchDataFilter to work within the pipeline?

    if odoo_data.data is None:
        logger.error("No products found in Odoo data")
        raise ValueError("No products found")

    for index, product in enumerate(odoo_data.data):
        if index == 2: # limit for testing purposes
            break

        # Run pipeline
        pipeline(product)

        # show returned categories and emissions factors
        print("Product:", product.description)
        print("Generated categories to match with emission factor (Climatiq):", product.climatiq_categories)
        print("Matched category with emission factor (Climatiq):", product.climatiq_matched_category if product.climatiq_matched_category else "None") #this should be sorted now
        print("Emission factor:", product.emission_factor.name if product.emission_factor else "None")

        #a small try out for the breact categorizer
        breact_categories = breact_categorizer.generate_categorization(product.description)
        print(f"[Breact] Categorization for '{product.description}': {breact_categories[0]}")
        breact_confidence = breact_categorizer.get_confidence_for_class(product.description, breact_categories[0])
        print(f"[Breact] Confidence for '{breact_categories[0]}': {breact_confidence}")

        print("Purchase emissions:", product.co2_purchase)
        # show cleaned supplier addresses and get distance calculation
        print(product.supplier_address)
        print(f"Distance: {product.delivery_distance}km")
        print("Weight of the product(s) (in kg):", product.weight)
        print("Delivery emissions:", product.co2_transport)
        print("==================")

        
if __name__ == "__main__":
    main()