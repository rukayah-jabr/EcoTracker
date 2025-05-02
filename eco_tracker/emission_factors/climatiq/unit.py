# https://www.climatiq.io/docs/api-reference/unit-types
# TODO: add all available unit types
from eco_tracker.emission_factors.exceptions import UnsupportedUnit


def return_unit(unit_type: str) -> dict[str, str] | None:

	match unit_type.lower():
		case "area":
			return {
				'area_unit': 'm2'
			}
		case "areaovertime":
			return {
				'mass_unit': 'kg',
				'time_unit': 'h'
			}
		case 'containeroverdistance':
			return {
				'distance_unit': 'km',
			}
		case 'data':
			return {
				'data_unit': 'GB'
			}
		case 'dataovertime':
			return {
				'data_unit': 'GB',
				'time_unit': 'hour'
			}
		case "distance":
			return {
				'distance_unit': 'km'
			}
		case 'distanceovertime':
			return {
				'distance_unit': 'km',
				'time_unit': 'hour'
			}
		case 'energy':
			return {
				'energy_unit': 'kWh'
			}
		case "money":
			return {
				'money_unit': 'eur'
			}
		case "number":
			return {}
		case 'numberovertime':
			return {
				'time_unit': 'h'
			}
		case 'pasesengeroverdistance':
			return {
				'distance_unit': 'km',
			}
		case 'power':
			return {
				'power_unit': 'kW'
			}
		case 'time':
			return {
				'time_unit': 'hour'
			}
		case 'volume':
			return {
				'volume_unit': 'l'
			}
		case 'weight':
			return {
				'weight_unit': 'kg'
			}
		case 'weightoverdistance':
			return {
				'distance_unit': 'km',
				'weight_unit': 'kg'
			}
		case 'weightovertime':
			return {
				'time_unit': 'hour',
				'weight_unit': 'kg'
			}
		case "":
			return None

	raise UnsupportedUnit(unit_type)
