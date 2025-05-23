import os
from datetime import datetime

from eco_tracker.categorization.breact.breact_categorization import BreactCategorizer
from eco_tracker.categorization.breact.breact_fe_categorization_filter import BreactFrontendCategorizationFilter
from eco_tracker.categorization.breact.breact_reorder_categorization_filter import CategoryReorderFilter
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

logger = get_logger(__name__)

class FullPipeline:
    def __init__(self, climatiq_api_key: str, llm_api_key: str, breact_api_key: str, open_route_service_api_key: str):
        self.climatiq_api_key = climatiq_api_key
        self.llm_api_key = llm_api_key
        self.breact_api_key = breact_api_key
        self.open_route_service_api_key = open_route_service_api_key
        
    def calculate_emissions(self, erp_url: str, start_date: datetime | None = None, end_date: datetime | None = None):
        
        groq_categorizer: Categorizer = ClimatiqCategorizer(self.llm_api_key)
        breact_categorizer: Categorizer = BreactCategorizer(self.breact_api_key)
        climatiq: EmissionFactorsFetcher = Climatiq(self.climatiq_api_key)
        basic_purchase_estimator: PurchaseEmissionsEstimator = BasicPurchaseEmissionsEstimator()
        
        open_route_distance_estimator: DistanceEstimator = OpenRouteService(self.open_route_service_api_key)
        emission_factors_transportation_fetcher: EmissionFactorsTransportationFetcher = BasicEmissionFactorsTransportationFetcher()
        groq_weight_estimator: WeightEstimator = GroqWeightEstimator(self.llm_api_key)
        distance_based_method: DistanceBasedMethod = DistanceBasedMethod()

        # Define product pipeline
        pipeline: Pipeline[Product] = Pipeline(
            ClimatiqCategorizerFilter(groq_categorizer),
            CategoryReorderFilter(breact_categorizer),
            EmissionFactorsFilter(climatiq, "^21"),
            BreactFrontendCategorizationFilter(breact_categorizer),
            PurchaseEmissionsEstimatorFilter(basic_purchase_estimator),
            
            DistanceEstimationFilter(open_route_distance_estimator),
            EmissionFactorsTransportationFilter(emission_factors_transportation_fetcher),
            WeightEstimationFilter(groq_weight_estimator),
            DeliveryEmissionsEstimatorFilter(distance_based_method)
        )

        odoo: DataFetcher = Odoo(api_base_url=erp_url)
        odoo_data = odoo.fetch_data_from_source(start_date, end_date)

        if odoo_data.data is None:
            logger.error("No products found in Odoo data")
            raise ValueError("No products found")

        enriched_products = []
        for product in odoo_data.data:
            pipeline(product)
            enriched_products.append(product)

        return enriched_products
