from flask import (Blueprint, request, jsonify)

from db import get_db

bp = Blueprint('fish_type', __name__)

@bp.route('/fish_type', methods=['GET'])
def get_fish_type():
    all_fish_types = get_db().execute(
        'SELECT *'
        ' FROM fish_type'
        ' ORDER BY timestamp DESC'
    ).fetchall()
    result = ""
    for row in all_fish_types:
        result = result + str(row['id']) + " " + str(row['name']) + "  temp:" + str(row['min_temperature']) \
                 + "-" + str(row['max_temperature']) + "  light:" + str(row['min_light_intensity']) + "-"\
                 + str(row['max_light_intensity']) + " food_id:" + str(row['food_id']) + " " + str(row['timestamp'])\
                 + "\n"
    return result

@bp.route('/fish_type', methods=['POST'])
def set_fish_type():
    type_name = request.form['name']
    min_temperature = request.form['min_temperature']
    max_temperature = request.form['max_temperature']
    min_light_intensity = request.form['min_light_intensity']
    max_light_intensity = request.form['max_light_intensity']
    food_type_id = request.form['food_id']

    if not type_name:
        return jsonify({'status': 'Fish type name is required.'}), 403
    elif not min_temperature:
        return jsonify({'status': 'Fish type min temperature is required.'}), 403
    elif not max_temperature:
        return jsonify({'status': 'Fish type max temperature is required.'}), 403
    elif not min_light_intensity:
        return jsonify({'status': 'Fish type min light intensity is required.'}), 403
    elif not max_light_intensity:
        return jsonify({'status': 'Fish type max light intensity is required.'}), 403
    elif not food_type_id:
        return jsonify({'status': 'Fish type food id is required.'}), 403

    print(type_name)
    print(min_temperature)
    print(max_temperature)
    print(min_light_intensity)
    print(max_light_intensity)
    print(food_type_id)
    db = get_db()
    db.execute(
        'INSERT INTO fish_type (name, food_id, min_temperature, max_temperature, min_light_intensity, max_light_intensity)'
        ' VALUES (?, ?, ?, ?, ?, ?)',
        (type_name, food_type_id, min_temperature, max_temperature, min_light_intensity, max_light_intensity)
    )
    db.commit()

    check = get_db().execute(
        'SELECT id, name, food_id, min_temperature, max_temperature, min_light_intensity, max_light_intensity, timestamp'
        ' FROM fish_type'
        ' ORDER BY timestamp DESC'
    ).fetchone()
    return jsonify({
        'status': 'Fish type successfully recorded',
        'data': {
            'id': check['id'],
            'timestamp': check['timestamp'],
            'name': check['name'],
            'food_id': check['food_id'],
            'min_temp': check['min_temperature'],
            'max_temp': check['max_temperature'],
            'min_light': check['min_light_intensity'],
            'max_light': check['max_light_intensity']
        }
    }), 200


@bp.route('/fish_type', methods=['PUT'])
def update_fish_type():
    fish_type_id = request.form['id']
    type_name = request.form['name']
    min_temperature = request.form['min_temperature']
    max_temperature = request.form['max_temperature']
    min_light_intensity = request.form['min_light_intensity']
    max_light_intensity = request.form['max_light_intensity']
    food_type_id = request.form['food_id']

    if not fish_type_id:
        return jsonify({'status': 'Fish type id is required.'}), 403
    elif not type_name:
        return jsonify({'status': 'Fish type name is required.'}), 403
    elif not min_temperature:
        return jsonify({'status': 'Fish type min temperature is required.'}), 403
    elif not max_temperature:
        return jsonify({'status': 'Fish type max temperature is required.'}), 403
    elif not min_light_intensity:
        return jsonify({'status': 'Fish type min light intensity is required.'}), 403
    elif not max_light_intensity:
        return jsonify({'status': 'Fish type max light intensity is required.'}), 403
    elif not food_type_id:
        return jsonify({'status': 'Fish type food id is required.'}), 403

    print(fish_type_id)
    print(type_name)
    print(min_temperature)
    print(max_temperature)
    print(min_light_intensity)
    print(max_light_intensity)
    print(food_type_id)

    db = get_db()
    db.execute(
        'UPDATE fish_type'
        ' SET name=?, min_temperature=?, max_temperature=?, min_light_intensity=?, max_light_intensity=?, food_id=?, timestamp=CURRENT_TIMESTAMP'
        ' WHERE id=?',
        (type_name, min_temperature, max_temperature, min_light_intensity, max_light_intensity, food_type_id, fish_type_id)
    )
    db.commit()

    check = get_db().execute(
        'SELECT *'
        ' FROM fish_type'
        ' WHERE id=?',
        (fish_type_id,)
    ).fetchone()

    if not check:
        return jsonify({'status': 'Fish type does not exist.'}), 404

    return jsonify({
        'status': 'Fish type successfully updated',
        'data': {
            'id': check['id'],
            'timestamp': check['timestamp'],
            'name': check['name'],
            'food_id': check['food_id'],
            'min_temp': check['min_temperature'],
            'max_temp': check['max_temperature'],
            'min_light': check['min_light_intensity'],
            'max_light': check['max_light_intensity']
        }
    }), 200


@bp.route('/fish_type', methods=['DELETE'])
def delete_fish_type():
    fish_type_id = request.form['id']

    if not fish_type_id:
        return jsonify({'status': 'Fish type id is required.'}), 403

    print(fish_type_id)

    db = get_db()
    db.execute(
        'DELETE FROM fish_type'
        ' WHERE id=?',
        (fish_type_id,)
    )
    db.commit()

    return jsonify({
        'status': 'Fish type successfully deleted',
    }), 200