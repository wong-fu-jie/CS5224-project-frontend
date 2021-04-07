# For demo purposes, this dictionary will serve the function of a database in keeping
# locations to corresponding picture files stored in S3 server

location_pic_data = {
    'Hort Park': 'hort-park.jpg',
    'Mount Faber Park': 'mount-faber.jpg',
    'Telok Blangah Market': 'telok-blangah-food-centre.jpg',
    "Chinatown": "chinatown.jpg",
    "Chinatown Complex Food Centre": "chinatown-food-centre.jpg",
    "National Museum": "national-museum.jpg"
}


def get_location_pic_data():
    return location_pic_data
