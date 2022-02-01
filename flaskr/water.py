from flask import (Blueprint, request, jsonify)

from db import get_db

bp = Blueprint('water', __name__)


@bp.route('/water', methods=['GET'])
def get_water():
    all_water_instances = get_db().execute(
        'SELECT *'
        ' FROM water'
        ' ORDER BY timestamp DESC'
    ).fetchall()
    result = ""
    for row in all_water_instances:
        result = result + str(row['id']) + ' aquarium_id: ' + str(row['aquarium_id']) + ' pH: ' + str('pH') + ' oxygen: ' \
                 + str(row['oxygen']) + ' bacteria: ' + str(row['bacteria']) + ' temperature: ' + str(row['temperature']) + ' timestamp: ' \
                 + str(row['timestamp']) + '\n'
    return result


@bp.route('/water', methods=['POST'])
def set_water():
    aquarium_id = request.form['aquarium_id']
    pH = request.form['pH']
    oxygen = request.form['oxygen']
    bacteria = request.form['bacteria']
    temperature = request.form['temperature']

    if not aquarium_id:
        return jsonify({'status': 'Aquarium id is required'}), 403
    elif not pH:
        return jsonify({'status': 'pH value is required'}), 403
    elif not oxygen:
        return jsonify({'status': 'Oxygen value is required'}), 403
    elif not bacteria:
        return jsonify({'status': 'Bacteria value is required'}), 403
    elif not temperature:
        return jsonify({'status': 'Temperature value is required'}), 403

    db = get_db()
    db.execute(
        'INSERT INTO water(aquarium_id, pH, oxygen, bacteria, temperature)'
        ' VALUES(?, ?, ?, ?, ?)',
        (aquarium_id, pH, oxygen, bacteria, temperature)
    )
    db.commit()

    check = get_db().execute(
        'SELECT id, aquarium_id, pH, oxygen, bacteria, temperature, timestamp'
        ' FROM water'
        ' ORDER BY timestamp DESC',
    ).fetchone()
    return jsonify({
        'status': 'Water successfully recorded',
        'data': {
            'id': check['id'],
            'aquarium_id': check['aquarium_id'],
            'pH': check['pH'],
            'oxygen': check['oxygen'],
            'bacteria': check['bacteria'],
            'temperature': check['temperature'],
            'timestamp': check['timestamp']
        }
    }), 200


@bp.route('/water', methods=['PUT'])
def update_water():
    water_id = request.form['id']
    aquarium_id = request.form['aquarium_id']
    pH = request.form['pH']
    oxygen = request.form['oxygen']
    bacteria = request.form['bacteria']
    temperature = request.form['temperature']

    if not water_id:
        return jsonify({'status': 'Water id is required'}), 403
    elif not aquarium_id:
        return jsonify({'status': 'Aquarium id is required'}), 403
    elif not pH:
        return jsonify({'status': 'pH value is required'}), 403
    elif not oxygen:
        return jsonify({'status': 'Oxygen value is required'}), 403
    elif not bacteria:
        return jsonify({'status': 'Bacteria value is required'}), 403
    elif not temperature:
        return jsonify({'status': 'Temperature value is required'}), 403

    db = get_db()

    db.execute(
        'UPDATE water'
        ' SET aquarium_id=?, pH=?, oxygen=?, bacteria=?, temperature=?'
        ' WHERE id=?',
        (aquarium_id, pH, oxygen, bacteria, temperature, water_id)
    )
    db.commit()

    check = get_db().execute(
        'SELECT *'
        ' FROM water'
        ' WHERE id=?',
        (water_id,)
    ).fetchone()

    if not check:
        return jsonify({'status': 'Water does not exist.'}), 404

    return jsonify({
        'status': 'Water successfully updated',
        'data': {
            'id': check['id'],
            'aquarium_id': check['aquarium_id'],
            'pH': check['pH'],
            'oxygen': check['oxygen'],
            'bacteria': check['bacteria'],
            'temperature': check['temperature']
        }
    }), 200


@bp.route('/water/<string:_id>', methods=['DELETE'])
def delete_water(_id):
    if not _id:
        return jsonify({'status': 'Water id is required'}), 403

    db = get_db()
    db.execute(
        'DELETE FROM water'
        ' WHERE id=?',
        (_id,)
    )
    db.commit()

    return jsonify({
        'status': 'Water successfully deleted',
    }), 200
