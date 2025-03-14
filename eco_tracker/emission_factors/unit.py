# https://www.climatiq.io/docs/api-reference/unit-types
# TODO: add all available unit types
def return_unit(unit_type: str) -> dict[str, str] | None:

	match unit_type.lower():
		case "weight":
			return {
				'mass_unit': 'kg'
			}
		case "money":
			return {
				'money_unit': 'eur'
			}
		case "area":
			return {
				'area_unit': 'm2'
			}
		case "distance":
			return {
				'distance_unit': 'km'
			}
