from src.models.zone_types import CampusZone

def test_campus_zone_enums():
    assert CampusZone.HOSTEL_BLOCK.value == "Hostel Block"
    assert CampusZone.ACADEMIC_BLOCK.value == "Academic Block"
