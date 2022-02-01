from db import get_db
from flask import (Blueprint, jsonify, request)


bp = Blueprint("aquarium", __name__)


@bp.route("/aquarium", methods=["GET"])
def get_aquarium():
    all_aquariums = get_db().execute(
        'SELECT id, timestamp, name, default_mode, total_food_quantity'
        ' FROM aquarium'
        ' ORDER BY timestamp DESC'
    ).fetchall()
    result = ""
    for row in all_aquariums:
        result = result + str(row['id']) + " " + str(row['name']) + " " + str(row['default_mode']) + " " + str(row['total_food_quantity']) \
                 + " " + str(row['timestamp']) + "\n"
    return result


@bp.route("/aquarium", methods=["POST"])
def set_aquarium():
    name = request.form["name"]
    default_mode = request.form["mode"]
    total_quantity = request.form["total_quant"]

    if not default_mode:
        return jsonify({'status': 'Default mode is required.'}), 403
    elif not total_quantity:
        return jsonify({'status': 'Total quantity is required.'}), 403
    elif not name:
        return jsonify({'status': 'Name is required.'}), 403

    print(name)
    print(default_mode)
    print(total_quantity)

    db = get_db()
    db.execute(
        'INSERT INTO aquarium(name, default_mode, total_food_quantity)'
        ' VALUES (?, ?, ?)',
        (name, default_mode, total_quantity)
    )
    db.commit()

    check = get_db().execute(
        'SELECT id, timestamp, name, default_mode, total_food_quantity'
        ' FROM aquarium'
        ' ORDER BY timestamp DESC'
    ).fetchone()
    return jsonify({
        'status': 'Aquarium successfully recorded',
        'data': {
            'id': check['id'],
            'name': check['name'],
            'timestamp': check['timestamp'],
            'default_mode': check['default_mode'],
            'total_food_quantity': check['total_food_quantity']
        }
    }), 200


@bp.route("/aquarium", methods=["PUT"])
def update_aquarium():
    name = request.form["name"]
    aquarium_id = request.form["id"]
    default_mode = request.form["mode"]
    total_food_quantity = request.form["total_quant"]

    if not aquarium_id:
        return jsonify({'status': 'Aquarium id is required.'}), 403
    elif not name:
        return jsonify({'status': 'Name is required.'}), 403
    elif not total_food_quantity:
        return jsonify({'status': 'Total food quantity is required.'}), 403
    elif not default_mode:
        return jsonify({'status': 'Default mode is required.'}), 403

    print(name)
    print(aquarium_id)
    print(total_food_quantity)
    print(default_mode)

    db = get_db()
    db.execute(
        'UPDATE aquarium'
        ' SET name=?, default_mode=?, total_food_quantity=?, timestamp=CURRENT_TIMESTAMP'
        ' WHERE id=?',
        (name, default_mode, total_food_quantity, aquarium_id)
    )
    db.commit()

    check = get_db().execute(
        'SELECT id, name, timestamp, default_mode, total_food_quantity'
        ' FROM aquarium'
        ' WHERE id=?',
        (aquarium_id,)
    ).fetchone()

    if not check:
        return jsonify({'status': 'Aquarium does not exist.'}), 404

    return jsonify({
        'status': 'Aquarium successfully updated',
        'data': {
            'id': check['id'],
            'name': check['name'],
            'timestamp': check['timestamp'],
            'default_mode': check['default_mode'],
            'total_food_quantity': check['total_food_quantity']
        }
    }), 200


@bp.route("/aquarium", methods=["DELETE"])
def delete_aquarium():
    aquarium_id = request.form["id"]

    if not aquarium_id:
        return jsonify({'status': 'Aquarium id is required.'}), 403

    print(aquarium_id)

    db = get_db()
    db.execute(
        'DELETE FROM aquarium'
        ' WHERE id=?',
        (aquarium_id,)
    )
    db.commit()

    return jsonify({
        'status': 'Aquarium successfully deleted',
    }), 200
