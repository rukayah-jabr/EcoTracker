from eco_tracker.erp_integration.fetch_data_interface import DataFetcher
from eco_tracker.erp_integration.fetch_data_interface import Data

class FetchDataFilter:
    def __init__(self, data_fetcher: DataFetcher):
        self.data_fetcher = data_fetcher
        self.source = None
        self.data = None

    def __call__(self) -> Data:
        try: 
            data = self.data_fetcher.fetch_data_from_source()
            print(f'{len(data.data)} items fetched from {data.source}')
            self.source = data.source
            self.data = data.data
        except:
            # TO DO: create exception class
            print("Error fetching data from source")