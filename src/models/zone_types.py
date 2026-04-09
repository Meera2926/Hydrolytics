from enum import Enum

class CampusZone(str, Enum):
    HOSTEL_BLOCK = "Hostel Block"
    ACADEMIC_BLOCK = "Academic Block"
    CAFETERIA = "Cafeteria / Mess"
    SPORTS_COMPLEX = "Sports Complex & Pool"
    ADMIN_BUILDING = "Administration Building"
    FACULTY_HOUSING = "Faculty Housing"
