
import json
from dataclasses import dataclass
from http import HTTPStatus

import requests
from pydantic import BaseModel

from eco_tracker.weight_estimation.exceptions import WeightEstimationFailed
from eco_tracker.weight_estimation.weight_estimation_interface import WeightEstimator


@dataclass
class EstimatedWeight(BaseModel):
  weight: float

class GroqWeightEstimator(WeightEstimator):

  def __init__(self, api_key: str):
    self.api_key = api_key
    self.authorization_headers = {"Authorization": f"Bearer {self.api_key}"}

  def estimate_weight(self, product_description: str) -> float:
    url = "https://api.groq.com/openai/v1/chat/completions"
    system_prompt = """
      You are an assistant that estimates the weight of a product.
      I need to estimate the weight of the product with packaging from the manufacturer.
      Provide the weight of the product in kilograms.
      always respond with valid JSON objects that match this structure:
      {
        "weight": "float"
      }
      """

    body = {
      "model": "llama-3.3-70b-versatile",
      "messages": [
        { "role": "system", "content": system_prompt },
        { "role": "user", "content": product_description }
      ]
    }

    response = requests.post(url, json=body, headers=self.authorization_headers)
    if response.status_code != HTTPStatus.OK:
      raise WeightEstimationFailed(product_description)

    body = response.json()
    response_message = body['choices'][0]['message']['content']
    weight = json.loads(response_message)["weight"]
    return weight

  def estimate_weight_of_quantity(self, product_description: str, quantity: float) -> float:
    return self.estimate_weight(product_description) * quantity
