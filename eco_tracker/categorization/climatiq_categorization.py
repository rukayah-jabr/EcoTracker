from http import HTTPStatus

import requests

from eco_tracker import exceptions


class ClimatiqCategorization:
	def __init__(self, llm_api_key: str):
		self.llm_api_key = llm_api_key

		self.authorization_headers = {"Authorization": f"Bearer {self.llm_api_key}"}


	def generate_categorization(self, product: str, num_of_categories: int = 10) -> list:
		url = "https://api.groq.com/openai/v1/chat/completions"
		content = f"""
				I have a product called ${product}.
				I need to match it with an emission factor from a database (climatiq.io), but exact matches are rare.
				Please provide ${num_of_categories} different, concise terms (1-3 words each) that broadly describe the product,
				avoiding excessive repetition of the same key terms.
				Terms must be in english and lowercase.
				Just return the terms in a enumerated list (1., 2., 3. and so on).
				Every entry must be in a new line.
				Skip any introduction like "Sure, here is the list ..." and so on.  
				"""

		body = {
			"model": "llama-3.3-70b-versatile",
			"messages": [{
				"content": content,
				"role": "system",
			}]
		}

		response = requests.post(url, json=body, headers=self.authorization_headers)
		if response.status_code != HTTPStatus.OK:
			raise exceptions.HTTPException(response.status_code, response.text)

		body = response.json()
		response_message = body['choices'][0]['message']['content']
		categories = parse_generated_categories(response_message)
		return categories

def parse_generated_categories(llm_categories: str) -> list:
	categories = []
	for category in llm_categories.split("\n"):
		without_enumeration = category.split(".")[1].strip()
		categories.append(without_enumeration)
	return categories
