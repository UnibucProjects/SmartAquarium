from flask import request
from flask_restful import Resource
from db import get_db

aquarium_types = ['crescatorie', 'petShop', 'personal']

types_preferences = {aquarium_types[0] :
    "UPDATE light "
    "SET color='white' "
    "WHERE id=?",
    aquarium_types[1] :
    "UPDATE light "
    "SET color='blue'"
    "WHERE id=?",
    aquarium_types[2] :
    "UPDATE light "
    "SET color='yellow'"
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
            return {'Status': 'Invalid aquarium id'}, 403
        else:
            return {'Aquarium mode': str(aquariumMode['default_mode'])}, 200


    def put(self, id):
        type = request.args.getlist('type')[0]

        db = get_db()
        aquarium_id = get_db().execute(
            'SELECT id '
            'FROM aquarium '
            'WHERE id=?', (str(id),)
            ).fetchone()

        if type not in aquarium_types:
            return {'Status' : 'Undentified type'}, 403
        if aquarium_id is None:
            return {'Status' : 'No aquarium with this id'}, 403

        db.execute(
            'UPDATE aquarium '
            'SET default_mode=? '
            'WHERE id=?', (type, str(id))
            )

        db.commit()

        light_id = db.execute(
            "SELECT id, timestamp "
            "FROM light "
            "WHERE aquarium_id=? "
            "ORDER BY timestamp DESC "
            ,(str(id), )
            ).fetchone()

        db.execute(types_preferences[type], (light_id['id'],))
        db.commit()

        return {'Status': 'Aquarium mode changed successfully'}, 200
