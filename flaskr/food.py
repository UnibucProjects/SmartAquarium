from flask import (Blueprint, request, jsonify)

from db import get_db

bp = Blueprint('environment', __name__)


@bp.route('/food', methods=['POST'])
def set_food():
    food_type = request.form['food']
    quantity = request.form['quant']
    error = None

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
