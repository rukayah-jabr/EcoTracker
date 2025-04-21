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

		#api needs time
		time.sleep(5)

		#make the get request
		get_url = f'{api_url_get}/{process_id}?access_token={access_token}'
		response_get = requests.get(get_url, headers=self.headers)
		if response_get.status_code != HTTPStatus.OK:
			raise exceptions.HTTPException(response_get.status_code, response_get.text)

		get_response_data = response_get.json()
		confidence = get_response_data['result']['result']['confidence']

		#confidence threshold 0.7
		if confidence < 0.7:
			categories = ["others"]  #fallback

		else:
			predicted_class = get_response_data['result']['result']['class']
			categories = [predicted_class]

		return categories