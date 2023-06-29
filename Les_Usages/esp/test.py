from flask import Flask, json
from flask_cors import CORS
import json
animals = json.load(open('animals.json', 'r'))

api = Flask(__name__)
cors = CORS(api)

@api.route('/succed/<id>', methods=['post'])
def change_color():
    try:
        result = animals[id]
    except KeyError:
        result = 'Not animal with this id'
    result.__setattr__("led", True)
    return result

@api.route('/all', methods=['get'])
def get_all():
    return animals

if __name__ == '__main__':
    api.run()