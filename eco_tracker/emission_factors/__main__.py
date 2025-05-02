import os

from dotenv import load_dotenv

from eco_tracker.emission_factors.climatiq import Climatiq
from eco_tracker.categorization.categorizer_interface import Categorizer
from eco_tracker.categorization.breact_categorization import BreactCategorizer


if __name__ == "__main__":
    load_dotenv()
    CLIMATIQ_API_KEY = os.getenv("CLIMATIQ_API_KEY")
    BREACT_API_KEY = os.getenv("BREACT_API_KEY")

    climatiq = Climatiq(api_key=CLIMATIQ_API_KEY)

    #best_matching_factor = climatiq.fetch_emission_factor_info(query="air purification", data_version="^20")
    #print(best_matching_factor)

    #emission_factor = climatiq.fetch_emission_factor(best_matching_factor)
    #print(emission_factor)
    # print(response['results'][0].keys())

    breact_categorizer: Categorizer = BreactCategorizer(BREACT_API_KEY)

    product_to_test = "Philips Akku 25,2V-2400MAH LI-ION Staubsauger Akku Alternative W192021"
    breact_categories = breact_categorizer.generate_categorization(product_to_test)
    print(f"[Breact] Categorization: {breact_categories[0]}")
    breact_confidence = breact_categorizer.get_confidence_for_class(product_to_test, breact_categories[0])
    print(f"[Breact] confidenceis {breact_confidence}")

