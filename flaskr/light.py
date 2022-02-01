from flask import (Blueprint, request, jsonify)

from db import get_db

bp = Blueprint('light', __name__)


@bp.route('/light', methods=['GET'])
def get_light():
    all_lights = get_db().execute(
        'SELECT *'
        ' FROM light'
        ' ORDER BY timestamp DESC'
    ).fetchall()
    result = ""
    for row in all_lights:
        result = result + str(row['id']) + " " + str(row['color']) + "  intensity:" + str(row['intensity']) \
                 + "  schedule:" + str(row['schedule']) + "  aquarium_id:" + str(row['aquarium_id']) + "  " + \
                 str(row['timestamp']) + "\n"
    return result


@bp.route('/light', methods=['POST'])
def set_light():
    aquarium_id = request.form['aquarium_id']
    intensity = request.form['intensity']
    color = request.form['color']
    schedule = request.form['schedule']
    error = None

    if not aquarium_id:
        return jsonify({'status': 'Aquarium_id is required.'}), 403
    elif not intensity:
        return jsonify({'status': 'Intensity is required.'}), 403
    elif not color: 
        return jsonify({'status': 'Color is required.'}), 403
    elif not schedule: 
        return jsonify({'status': 'Schedule is required.'}), 403    

    db = get_db()
    db.execute(
        'INSERT INTO light (aquarium_id, intensity, color, schedule)'
        ' VALUES (?, ?, ?, ?)',
        (aquarium_id, intensity, color, schedule)
    )
    db.commit()

    check = get_db().execute(
        'SELECT id, timestamp, aquarium_id, intensity, color, schedule'
        ' FROM light'
        ' ORDER BY timestamp DESC'
    ).fetchone()
    return jsonify({
        'status': 'Light settings successfully recorded',
        'data': {
            'id': check['id'],
            'timestamp': check['timestamp'],
            'aquarium_id': check['aquarium_id'],
            'intensity': check['intensity'],
            'color': check['color'],
            'schedule': check['schedule']
        }
        }), 200


@bp.route('/light', methods=['PUT'])
def update_light():
    light_id = request.form['id']
    aquarium_id = request.form['aquarium_id']
    intensity = request.form['intensity']
    color = request.form['color']
    schedule = request.form['schedule']
    error = None

    if not light_id:
        return jsonify({'status': 'Light id is required.'}), 403
    elif not aquarium_id:
        return jsonify({'status': 'Aquarium id is required.'}), 403
    elif not intensity:
        return jsonify({'status': 'Intensity is required.'}), 403
    elif not color:
        return jsonify({'status': 'Color is required.'}), 403
    elif not schedule:
        return jsonify({'status': 'Schedule is required.'}), 403

    db = get_db()
    db.execute(
        'UPDATE light'
        ' SET aquarium_id=?, color=?, intensity=?, schedule=?, timestamp=CURRENT_TIMESTAMP'
        ' WHERE id=?',
        (aquarium_id, color, intensity, schedule, light_id)
    )
    db.commit()

    check = get_db().execute(
        'SELECT *'
        ' FROM light'
        ' WHERE id=?',
        (light_id,)
    ).fetchone()

    if not check:
        return jsonify({'status': 'Light does not exist.'}), 404

    return jsonify({
        'status': 'Light settings successfully updated',
        'data': {
            'id': check['id'],
            'timestamp': check['timestamp'],
            'aquarium_id': check['aquarium_id'],
            'intensity': check['intensity'],
            'color': check['color'],
            'schedule': check['schedule']
        }
    }), 200


@bp.route('/light/<string:_id>', methods=['DELETE'])
def delete_light(_id):
    if not _id:
        return jsonify({'status': 'Light id is required.'}), 403
    print(f"Light id is {_id}")

    db = get_db()
    db.execute(
        'DELETE FROM light'
        ' WHERE id=?',
        (_id,)
    )
    db.commit()
    return jsonify({'status': 'Light successfully deleted.'}), 200
