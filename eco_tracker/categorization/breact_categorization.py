import time
from http import HTTPStatus

import requests

from eco_tracker import exceptions
from eco_tracker.categorization.categorizer_interface import Categorizer


class BreactCategorizer(Categorizer):
	def __init__(self, breact_api_key: str):
		self.breact_api_key = breact_api_key
		self.headers = {
			"x-api-key": self.breact_api_key,
			"Content-Type": "application/json"
		}

	#implemet the method from interface	(Categorizer)
	def generate_categorization(self, product: str, num_of_categories: int = 10) -> list:
		api_url_post = 'https://api-os.breact.ai/api/v1/services/classifier/process'
		api_url_get = 'https://api-os.breact.ai/api/v1/services/result'

		request_data = {
			"content": product,
			"context": {
				"classificationType": "products",
				"allowedClasses": [
					"Haushaltsgeraete", "Kaffee & Zubehoer", "Reinigung & Waschmittel",
					"Batterien & Akkus", "Beleuchtung", "Elektronik",
					"Ersatzteile & Zubehoer", "Service", "Lieferservice", "Kuechengeraete"
				],
				"multiClass": False
			},
			"config": {
				"modelId": "mistral-large-2411",
				"temperature": 0.5,
				"maxTokens": 1000
			}
		}

		#make the post request
		response_post = requests.post(api_url_post, json=request_data, headers=self.headers)

		if response_post.status_code != HTTPStatus.OK:
			raise exceptions.HTTPException(response_post.status_code, response_post.text)

		#Parse response from post to extract access_token and process_id
		post_response_data = response_post.json()
		access_token = post_response_data.get('access_token')
		process_id = post_response_data.get('process_id')

		#the get request
		get_url = f'{api_url_get}/{process_id}?access_token={access_token}'
		get_response_data = self._poll_for_result(get_url)

		#extract confidence
		inner_result = get_response_data.get('result', {}).get('result', {})
		confidence = inner_result.get('confidence', 0)

		#confidence threshold 0.7
		if confidence < 0.7:
			categories = ["others"]  #fallback

		else:
			predicted_class = get_response_data['result']['result']['class']
			categories = [predicted_class]

		return categories

	def _poll_for_result(self, url: str, timeout: int = 30, interval: int = 2) -> dict:
		#Polls the GET endpoint
		start_time = time.time()
		while time.time() - start_time < timeout:
			response = requests.get(url, headers=self.headers)
			if response.status_code == HTTPStatus.OK:
				data = response.json()
				if 'result' in data and 'result' in data['result']:
					return data
			time.sleep(interval)
		raise exceptions.HTTPException(504, "Timeout while polling for result.")