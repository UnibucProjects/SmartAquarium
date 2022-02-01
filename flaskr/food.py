from flask import (Blueprint, request, jsonify)

from db import get_db

bp = Blueprint('food', __name__)

@bp.route('/food', methods=['GET'])
def get_food():
    all_foods = get_db().execute(
        'SELECT id, timestamp, type, quantity'
        ' FROM food'
        ' ORDER BY timestamp DESC'
    ).fetchall()
    result = ""
    for row in all_foods:
        result = result + str(row['id']) + " " + str(row['type']) + " " + str(row['quantity'])\
                 + " " + str(row['timestamp']) + "\n"
    return result

@bp.route('/food', methods=['POST'])
def set_food():
    food_type = request.form['food']
    quantity = request.form['quant']

    if not food_type:
        return jsonify({'status': 'Food type is required.'}), 403
    elif not quantity:
        return jsonify({'status': 'Food quantity is required.'}), 403

    print(food_type)
    print(quantity)
    db = get_db()
    db.execute(
        'INSERT INTO food (type, quantity)'
        ' VALUES (?, ?)',
        (food_type, quantity)
    )
    db.commit()

    check = get_db().execute(
        'SELECT id, timestamp, type, quantity'
        ' FROM food'
        ' ORDER BY timestamp DESC'
    ).fetchone()
    return jsonify({
        'status': 'Food type successfully recorded',
        'data': {
            'id': check['id'],
            'timestamp': check['timestamp'],
            'type': check['type'],
            'quantity': check['quantity']
         }
         }), 200


@bp.route('/food', methods=['PUT'])
def update_food():
    food_id = request.form['id']
    food_type = request.form['food']
    quantity = request.form['quant']

    if not food_id:
        return jsonify({'status': 'Food id is required.'}), 403
    elif not quantity:
        return jsonify({'status': 'Food quantity is required.'}), 403
    elif not food_type:
        return jsonify({'status': 'Food type is required.'}), 403

    print(food_id)
    print(quantity)
    print(food_type)

    db = get_db()
    db.execute(
        'UPDATE food'
        ' SET type=?, quantity=?, timestamp=CURRENT_TIMESTAMP'
        ' WHERE id=?',
        (food_type, quantity, food_id)
    )
    db.commit()

    check = get_db().execute(
        'SELECT id, timestamp, type, quantity'
        ' FROM food'
        ' WHERE id=?',
        (food_id,)
    ).fetchone()

    if not check:
        return jsonify({'status': 'Food does not exist.'}), 404

    return jsonify({
        'status': 'Food type successfully updated',
        'data': {
            'id': check['id'],
            'timestamp': check['timestamp'],
            'type': check['type'],
            'quantity': check['quantity']
        }
    }), 200


@bp.route('/food/<string:_id>', methods=['DELETE'])
def delete_food(_id):
    if not _id:
        return jsonify({'status': 'Food id is required.'}), 403

    print(_id)

    db = get_db()
    db.execute(
        'DELETE FROM food'
        ' WHERE id=?',
        (_id,)
    )
    db.commit()

    return jsonify({
        'status': 'Food type successfully deleted',
    }), 200
