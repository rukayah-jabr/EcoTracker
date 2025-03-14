import eco_tracker.emission_factors.unit as unit

def test_return_unit():
	assert unit.return_unit("weight") == {'mass_unit': 'kg'}
	assert unit.return_unit("money") == {'money_unit': 'eur'}
	assert unit.return_unit("area") == {'area_unit': 'm2'}