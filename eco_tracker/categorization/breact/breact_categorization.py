import time
from http import HTTPStatus

import requests
import json

from eco_tracker import exceptions
from eco_tracker.categorization.categorizer_interface import Categorizer
from eco_tracker import api_cache


class BreactCategorizer(Categorizer):
	def __init__(self, breact_api_key: str):
		self.breact_api_key = breact_api_key
		self.headers = {
			"x-api-key": self.breact_api_key,
			"Content-Type": "application/json"
		}

	# implement the method from interface (Categorizer)
	def generate_categorization(self, product: str, num_of_categories: int = 10) -> list:
		result = self._classify(product)
		confidence = result.get("confidence", 0)

		##confidence threshold 0.7
		if confidence < 0.7:
			return ["others"]
		return [result.get("class", "others")]

	# for one category
	def get_confidence_for_class(self, product: str, category: str) -> float:
		result = self._classify(product, allowed_classes=[category])
		print(result)
		if result is not None:
			if result.get("class") != category:
				return 0.0
			return result.get("confidence", 0.0)
		else:
			return 0.0

	#for multi cat
	def generate_confidences(self, product: str, allowed_classes: list[str] | None = None) -> dict[str, float]:

		result = self._classify(product, allowed_classes=allowed_classes, multi_class=True)
		classifications = result.get("classifications", [])

		# Optionally filter by allowed_classes
		if allowed_classes is not None:
			classifications = [
				item for item in classifications if item["class"] in allowed_classes
			]

		return {item["class"]: item["confidence"] for item in classifications}

	#actual call to API
	def _classify(
			self,
			product: str,
			allowed_classes: list[str] | None = None,
			multi_class: bool = False
	) -> dict:
		api_url_classifier = 'https://api-os.breact.ai/api/v1/services/classifier/process'
		api_url_result = 'https://api-os.breact.ai/api/v1/services/result'

		if allowed_classes is None:
			allowed_classes = [
				"Haushaltsgeraete", "Kaffee & Zubehoer", "Reinigung & Waschmittel",
				"Batterien & Akkus", "Beleuchtung", "Elektronik",
				"Ersatzteile & Zubehoer", "Service", "Lieferservice", "Kuechengeraete"
			]

		request_data = {
			"content": product,
			"context": {
				"classificationType": "products",
				"allowedClasses": allowed_classes,
				"multiClass": multi_class
			},
			"config": {
				"modelId": "mistral-large-2411",
				"temperature": 0.5,
				"maxTokens": 1000
			}
		}

		@api_cache.execute_or_get_from_cache(url=api_url_result, request=json.dumps(request_data))
		def fetch_response(body: dict) -> dict:
			response_post = requests.post(api_url_classifier, json=body, headers=self.headers)
			if response_post.status_code != HTTPStatus.OK:
				raise exceptions.HTTPException(response_post.status_code, response_post.text)

			# Parse response from post to extract access_token and process_id
			post_response_data = response_post.json()
			access_token = post_response_data.get('access_token')
			process_id = post_response_data.get('process_id')

			get_url = f'{api_url_result}/{process_id}?access_token={access_token}'
			get_response_data = self._poll_for_result(get_url)

			return get_response_data.get("result", {}).get("result", {})

		return fetch_response(request_data)

	def _poll_for_result(self, url: str, timeout: int = 45, interval: float = 3) -> dict:
		start_time = time.time()
		while time.time() - start_time < timeout:
			response = requests.get(url, headers=self.headers)
			if response.status_code == HTTPStatus.OK:
				data = response.json()
				if 'result' in data and 'result' in data['result']:
					return data
			time.sleep(interval)
		raise exceptions.HTTPException(504, "Timeout while polling for result.")