import time
from flask import Flask, jsonify

app = Flask(__name__)


@app.route('/api/time', methods=['GET'])
def get_current_time():
  return {'time': time.time()}


itinerary = [
    {
        "id": 1,
        "picture": "hort-park.jpg",
        "name": "Hort Park",
        "travelTime": "20 mins (Grab)",
        "description":
        "Hort Park is a one-stop gardening resource hub that brings together gardening-related, recreational, educational, research and retail activities under one big canopy in a park setting. It also serves as a knowledge centre on plants and gardening, providing planting ideas and solutions, and offering a platform for the horticulture industry to share best practices and showcase garden designs, products and services.",
    },
    {
        "id": 2,
        "picture": "mount-faber.jpg",
        "name": "Mount Faber Park",
        "travelTime": "15 mins (Grab)",
        "description":
        "Mount Faber, originally known as Telok Blangah Hill is Singapore's second-highest hill and the park atop the hill is named as Mount Faber Park after Captain Charles Edward Faber in July 1845. It is among the oldest parks of Singapore and a major tourist attraction for nature lovers. Standing at an elevation of 105 metres Mount Faber is nestled inside the Bukit Merah town in Central Singapore overlooking Telok Blangah hill and the western region of the Central Area.",
    },
    {
        "id": 3,
        "picture": "telok-blangah-food-centre.jpg",
        "name": "Telok Blangah Food Centre",
        "travelTime": "10 mins (Walk)",
        "description":
        "Enjoy cheap and delicious food at Telok Blangah Food Centre. Favourites include Su Yuan Vegetarian, Song Heng Fishball Noodles and of course an all time great Uncle Lee's Hong Kong Noodle & Rice.",
    }
]


@app.route('/api/itinerary', methods=['GET'])
def get_itinerary():

  return jsonify(itinerary)
