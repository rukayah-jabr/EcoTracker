from eco_tracker.erp_integration.exceptions import FetchingDataFailed
from eco_tracker.erp_integration.fetch_data_interface import DataFetcher


class FetchDataFilter:
    def __init__(self, data_fetcher: DataFetcher):
        self.data_fetcher = data_fetcher
        self.source = None
        self.data = None

    def __call__(self) -> None:
        try: 
            data = self.data_fetcher.fetch_data_from_source()
            print(f'{len(data.data)} items fetched from {data.source}')
            self.source = data.source
            self.data = data.data
        except Exception:
            raise FetchingDataFailed(url=self.source)