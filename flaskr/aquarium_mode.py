from flask_restful import Resource
from db import get_db
from enum import Enum

aquarium_types = ['crescatorie', 'petShop', 'personal']

types_preferences = {aquarium_types[0] :
    "UPDATE light "
    "SET color='white', intensity=85, schedule = 'frequently' "
    "WHERE id=?",
    aquarium_types[1] :
    "UPDATE light "
    "SET color='blue', intensity=60, schedule = 'normal' "
    "WHERE id=?",
    aquarium_types[2] :
    "UPDATE light "
    "SET color='yellow', intensity=50, schedule = 'moderate' "
    "WHERE id=?",
}

class AquariumMode(Resource):
    def get(self, id):
        aquariumMode = get_db().execute(
            'SELECT default_mode '
            'FROM aquarium '
            'WHERE id=?', (str(id),)
            ).fetchone()
        if aquariumMode is None:
            return {'Status': 'Invalid aquarium id'}
        else:
            return {'Aquarium mode': str(aquariumMode['default_mode'])};


    def put(self, id, type):
        db = get_db()
        aquarium_id = get_db().execute(
            'SELECT id '
            'FROM aquarium '
            'WHERE id=?', (str(id),)
            ).fetchone()

        if type not in aquarium_types:
            return {'Status' : 'Undentified type'}

        if aquarium_id is None:
            return {'Status' : 'No aquarium with this id'}

        query =  db.execute(
            'UPDATE aquarium '
            'SET default_mode=? '
            'WHERE id=?', (type, str(id))
            )

        db.commit()

        # light_id = db.execute(
        #     "SELECT id from "
        #     "(SELECT id, timestamp "
        #     "FROM light "
        #     "WHERE aquarium_id=?) "
        #     "ORDER BY timestamp DESC "
        #     ,(str(aquarium_id), )
        #     ).fetchone()

        light_id = db.execute(
            "SELECT id, timestamp "
            "FROM light "
            "WHERE aquarium_id=? "
            "ORDER BY timestamp DESC "
            ,(str(id), )
            ).fetchone()

        db.execute(types_preferences[type], (str(light_id['id']),))
        db.commit()

        return {'Status' : 'Aquaruim mode changed successfully'}
