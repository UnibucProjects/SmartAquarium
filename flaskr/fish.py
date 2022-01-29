from flask import (Blueprint, request, jsonify)

from db import get_db

bp = Blueprint('fish', __name__)


@bp.route('/fish', methods=['GET'])
def get_fish():
    all_fish = get_db().execute(
        'SELECT *'
        ' FROM fish'
        ' ORDER BY timestamp DESC'
    ).fetchall()
    result = ""
    for row in all_fish:
        result = result + str(row['id']) + " " + str(row['name']) + " health:" + str(row['health']) \
        + " birthday: " + str(row['birthday']) + " type_id: " + str(row['type_id']) + " aquarium_id" \
        + str(row['aquarium_id']) + " timestamp: " + str(row['timestamp']) + "\n"
    return result


@bp.route('/fish', methods=['POST'])
def set_fish():
    name = request.form['name']
    health = request.form['health']
    birthday = request.form['birthday']
    type_id = request.form['type_id']
    aquarium_id = request.form['aquarium_id']

    if not name:
        return jsonify({'status': 'Fish name is required.'}), 403
    elif not health:
        return jsonify({'status': 'Fish health info is required.'}), 403
    elif not birthday:
        return jsonify({'status': 'Fish birthday is required'}), 403
    elif not type_id:
        return jsonify({'status': 'Fish type is required.'}), 403
    elif not aquarium_id:
        return jsonify({'status': 'Fish aquarium is required.'}), 403

    print(f"name is {name}")
    print(f"health is {health}")
    print(f"birthday is {birthday}")
    print(f"fish type id is {type_id}")
    print(f"aquarium id is {aquarium_id}")

    db = get_db()
    db.execute(
        'INSERT INTO fish (type_id, aquarium_id, name, health, birthday)'
        ' VALUES (?, ?, ?, ?, ?)',
        (type_id, aquarium_id, name, health, birthday)
    )
    db.commit()

    check = get_db().execute(
        'SELECT id, type_id, aquarium_id, name, health, birthday, timestamp'
        ' FROM fish'
        ' ORDER BY timestamp DESC'
    ).fetchone()
    return jsonify({
        'status': 'Fish successfully recorded.',
        'data': {
            'id': check['id'],
            'timestamp': check['timestamp'],
            'type_id': check['type_id'],
            'aquarium_id': check['aquarium_id'],
            'name': check['name'],
            'health': check['health'],
            'birthday': check['birthday']
        }
    }), 200


@bp.route('/fish', methods=['PUT'])
def update_fish():
    fish_id = request.form['id']
    type_id = request.form['type_id']
    aquarium_id = request.form['aquarium_id']
    name = request.form['name']
    health = request.form['health']
    birthday = request.form['birthday']

    if not fish_id:
        return jsonify({'status': 'Fish id is required.'}), 403
    elif not type_id:
        return jsonify({'status': 'Fish type id is required.'}), 403
    elif not aquarium_id:
        return jsonify({'status': 'Aquarium id is required.'}), 403
    elif not name:
        return jsonify({'status': 'Fish name is required,'}), 403
    elif not health:
        return jsonify({'status': 'Fish health is required.'}), 403
    elif not birthday:
        return jsonify({'status': 'Fish birthday is required.'}), 403

    print(f"Fish id is {fish_id}")
    print(f"Fish type id is {type_id}")
    print(f"Aquarium id is {aquarium_id}")
    print(f"Fish name is {name}")
    print(f"Fish health is {health}")
    print(f"Birthday is {birthday}")

    db = get_db()
    db.execute(
        'UPDATE fish'
        ' SET type_id=?, aquarium_id=?, name=?, health=?, birthday=?, timestamp=CURRENT_TIMESTAMP'
        ' WHERE id=?',
        (type_id, aquarium_id, name, health, birthday, fish_id)
    )
    db.commit()

    check = get_db().execute(
        'SELECT *'
        ' FROM fish'
        ' WHERE id=?',
        fish_id
    ).fetchone()
    return jsonify({
        'status': 'Fish successfully updated',
        'data': {
            'id': check['id'],
            'timestamp': check['timestamp'],
            'type_id': check['type_id'],
            'aquarium_id': check['aquarium_id'],
            'name': check['name'],
            'health': check['health'],
            'birthday': check['birthday']
        }
    }), 200


@bp.route('/fish', methods=['DELETE'])
def delete_fish():
    fish_id = request.form['id']

    if not fish_id:
        return jsonify({'status': 'Fish id is required.'}), 403
    print(f"Fish id is {fish_id}")

    db = get_db()
    db.execute(
        'DELETE FROM fish'
        ' WHERE id=?',
        fish_id
    )
    db.commit()
    return jsonify({'status': 'Fish successfully deleted.'}), 200
