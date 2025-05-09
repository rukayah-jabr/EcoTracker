class WrongActivityUnitException(Exception):
  def __init__(self, activity_unit: str):
    super().__init__(f"Activity unit must be kg-km to match the distance and weight units, but got {activity_unit}")
