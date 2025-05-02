class NotSupportedMeasurementUnit(Exception):
    def __init__(self, unit: str):
        self.unit = unit
        super().__init__(f"Measurement unit {unit} not supported")

class PurchaseEmissionFactorNotSet(Exception):
    def __init__(self, product_id: str):
        self.product_id = product_id
        super().__init__(f"Purchase emission factor not set for product: {product_id}")