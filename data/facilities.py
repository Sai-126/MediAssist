DISTRICT_FACILITIES = {
    "Hyderabad": ["Gandhi Hospital, Secunderabad", "Osmania General Hospital, Hyderabad"],
    "Warangal": ["MGM Hospital, Warangal", "District Hospital, Hanamkonda"],
    "Karimnagar": ["Government General Hospital, Karimnagar"],
    "Nizamabad": ["Government General Hospital, Nizamabad"],
    "Khammam": ["Government General Hospital, Khammam"],
    "Vijayawada": ["Government General Hospital, Vijayawada"],
    "Visakhapatnam": ["King George Hospital, Visakhapatnam"],
    "Guntur": ["Government General Hospital, Guntur"],
    "Tirupati": ["Sri Venkateswara Ramnarain Ruia Government Hospital, Tirupati"],
    "Kurnool": ["Government General Hospital, Kurnool"],
    "Nellore": ["Government General Hospital, Nellore"],
    "Rajahmundry": ["Government General Hospital, Rajahmundry"],
}

def get_facilities(district: str) -> list:
    return DISTRICT_FACILITIES.get(district, ["No facility data available for this district yet."])