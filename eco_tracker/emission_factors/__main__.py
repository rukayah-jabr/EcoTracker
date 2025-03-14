import os
from dotenv import load_dotenv
from .climatiq import Climatiq

if __name__ == "__main__":
    load_dotenv()
    CLIMATIQ_API_KEY = os.getenv("CLIMATIQ_API_KEY")

    climatiq = Climatiq(api_key=CLIMATIQ_API_KEY)

    best_matching_factor = climatiq.fetch_emission_factor_info(query="air purification", data_version="^20")
    print(best_matching_factor)

    emission_factor = climatiq.fetch_emission_factor(best_matching_factor)
    print(emission_factor)
    # print(response['results'][0].keys())