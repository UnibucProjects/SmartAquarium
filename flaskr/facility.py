from db import get_db
from flask import (Blueprint, jsonify, request)

bp = Blueprint("facility", __name__)


@bp.route("/facility", methods=["GET"])
def get_facility():
    all_facilities = get_db().execute(
        'SELECT *'
        ' FROM facility'
        ' ORDER BY timestamp DESC'
    ).fetchall()
    result = ""
    for row in all_facilities:
        result = result + str(row['id']) + \
                 " electricity:" + str(row['electricity']) \
                 + " movement_sensor:" + str(row['movement_sensor']) \
                 + " temperature_sensor" + str(row['temperature_sensor']) \
                 + " filter_sensor:" + str(row['filter_sensor']) \
                 + " weight_sensor:" + str(row['weight_sensor']) \
                 + " aquarium_id:" + str(row['aquarium_id']) \
                 + " " + str(row['timestamp']) \
                 + "\n"
    return result


@bp.route('/facility', methods=["POST"])
def set_facility():
    electricity = request.form['electricity']
    movement_sensor = request.form['movement_sensor']
    temperature_sensor = request.form['temperature_sensor']
    filter_sensor = request.form['filter_sensor']
    weight_sensor = request.form['weight_sensor']
    aquarium_id = request.form['aquarium_id']

    if not electricity:
        return jsonify({'status': 'Electricity status is required.'}), 403
    elif not movement_sensor:
        return jsonify({'status': 'Movement sensor status is required.'}), 403
    elif not temperature_sensor:
        return jsonify({'status: Temperature sensor status is required.'}), 403
    elif not filter_sensor:
        return jsonify({'status: Filter sensor status is required.'}), 403
    elif not weight_sensor:
        return jsonify({'status: Weight sensor status is required.'}), 403
    elif not aquarium_id:
        return jsonify({'status: Aquarium_id is required.'}), 403

    print(f"electricity status is {electricity}")
    print(f"movement_sensor status is {movement_sensor}")
    print(f"temperature_sensor status is {temperature_sensor}")
    print(f"filter_sensor status is {filter_sensor}")
    print(f"weight_sensor status is {weight_sensor}")
    print(f"aquarium_id is {aquarium_id}")

    db = get_db()
    db.execute('INSERT INTO facility (aquarium_id, electricity, movement_sensor, temperature_sensor, filter_sensor, '
               'weight_sensor) '
               ' VALUES (?, ?, ?, ?, ?, ?)',
               (aquarium_id, electricity, movement_sensor, temperature_sensor, filter_sensor, weight_sensor)
               )
    db.commit()

    check = get_db().execute(
        'SELECT id, aquarium_id, electricity, movement_sensor, temperature_sensor, filter_sensor, weight_sensor, '
        'timestamp '
        ' FROM facility'
        ' ORDER BY timestamp DESC'
    ).fetchone()

    return jsonify({
        'status': 'New facility list successfully recorded',
        'data': {
            'id': check['id'],
            'timestamp': check['timestamp'],
            'aquarium_id': check['aquarium_id'],
            'electricity': check['electricity'],
            'movement_sensor': check['movement_sensor'],
            'temperature_sensor': check['temperature_sensor'],
            'filter_sensor': check['filter_sensor'],
            'weight_sensor': check['weight_sensor']
        }
    }), 200


@bp.route('/facility', methods=['PUT'])
def update_facility():

    electricity = request.form['electricity']
    movement_sensor = request.form['movement_sensor']
    temperature_sensor = request.form['temperature_sensor']
    filter_sensor = request.form['filter_sensor']
    weight_sensor = request.form['weight_sensor']
    aquarium_id = request.form['aquarium_id']
    facility_id = request.form['id']

    if not facility_id:
        return jsonify({'status': 'Facility id is required.'}), 403
    elif not electricity:
        return jsonify({'status': 'Electricity status is required.'}), 403
    elif not movement_sensor:
        return jsonify({'status': 'Movement sensor status is required.'}), 403
    elif not temperature_sensor:
        return jsonify({'status: Temperature sensor status is required.'}), 403
    elif not filter_sensor:
        return jsonify({'status: Filter sensor status is required.'}), 403
    elif not weight_sensor:
        return jsonify({'status: Weight sensor status is required.'}), 403
    elif not aquarium_id:
        return jsonify({'status: Aquarium_id is required.'}), 403

    print(f"electricity status is {electricity}")
    print(f"movement_sensor status is {movement_sensor}")
    print(f"temperature_sensor status is {temperature_sensor}")
    print(f"filter_sensor status is {filter_sensor}")
    print(f"weight_sensor status is {weight_sensor}")
    print(f"aquarium_id is {aquarium_id}")

    db = get_db()
    db.execute('UPDATE facility'
               ' SET electricity=?, movement_sensor=?, temperature_sensor=?, filter_sensor=?, '
               'aquarium_id=?, weight_sensor=?, timestamp = CURRENT_TIMESTAMP '
               ' WHERE id=?',
               (electricity, movement_sensor, temperature_sensor, filter_sensor, weight_sensor, aquarium_id, facility_id)
               )
    db.commit()

    check = get_db().execute(
        'SELECT *'
        ' FROM facility'
        ' WHERE id=?',
        (facility_id,)
    ).fetchone()

    if not check:
        return jsonify({'status': 'Facility list does not exist.'}), 404

    return jsonify({
        'status': 'Facility list successfully updated',
        'data': {
            'id': check['id'],
            'timestamp': check['timestamp'],
            'aquarium_id': check['aquarium_id'],
            'electricity': check['electricity'],
            'movement_sensor': check['movement_sensor'],
            'temperature_sensor': check['temperature_sensor'],
            'filter_sensor': check['filter_sensor'],
            'weight_sensor': check['weight_sensor']
        }
    }), 200


@bp.route('/facility/<string:_id>', methods=['DELETE'])
def delete_facility(_id):
    if not _id:
        return jsonify({'status': 'Facility id is required.'}), 403

    print(_id)

    db = get_db()
    db.execute(
        'DELETE FROM facility'
        ' WHERE id=?',
        (_id,)
    )
    db.commit()

    return jsonify({'status': 'Facility list successfully deleted'}), 200

