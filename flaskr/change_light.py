from flask import request
from flask_restful import Resource
from db import get_db


def is_aquarium_id_valid(id):
    db = get_db()
    aquariumMode = get_db().execute(
        'SELECT id '
        'FROM aquarium '
        'WHERE id=?', (id,)
        ).fetchone()
    if aquariumMode is None:
        return False;
    else:
        return True;


class LightColor(Resource):
    def get(self, aquarium_id):
        db = get_db()
        if is_aquarium_id_valid(aquarium_id) == False:
            return {'Status': 'Invalid aquarium id!'}, 403

        light_data = db.execute(
            "SELECT color "
            "FROM light "
            "WHERE aquarium_id=? "
            "ORDER BY timestamp DESC "
            ,(str(aquarium_id), )
            ).fetchone()

        return {'Light color': light_data['color']}, 200


    def put(self, aquarium_id):
        db = get_db()
        color = request.args.getlist('color')[0]

        if is_aquarium_id_valid(aquarium_id) is False:
            return {'Status': 'Invalid aquarium id!'}, 403

        print ('Aquarium id exist? :' + str(aquarium_id))

        light_data = db.execute(
            "SELECT color, id "
            "FROM light "
            "WHERE aquarium_id=? "
            "ORDER BY timestamp DESC "
            ,(aquarium_id, )
            ).fetchone()

        db.execute(
            "UPDATE light "
            "SET color=? "
            "WHERE id=?", (color, light_data['id']))

        db.commit()

        return {'Status': 'Color was set successfully '}, 200
