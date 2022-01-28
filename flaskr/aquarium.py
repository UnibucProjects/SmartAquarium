from db import get_db
from flask import (Blueprint, jsonify, request)


bp = Blueprint("aquarium", __name__)


@bp.route("/aquarium", methods=["POST"])
def set_aquarium():
    default_mode = request.form["mode"]
    total_quantity = request.form["total_quant"]
    error = None

    if not default_mode:
        return jsonify({'status': 'Default mode is required.'}), 403
    elif not total_quantity:
        return jsonify({'status': 'Total quantity is required.'}), 403

    print(default_mode)
    print(total_quantity)
    db = get_db()
    db.execute(
        'INSERT INTO aquarium(default_mode, total_food_quantity)'
        ' VALUES (?, ?)',
        (default_mode, total_quantity)
    )
    db.commit()

    check = get_db().execute(
        'SELECT id, timestamp, default_mode, total_food_quantity'
        ' FROM aquarium'
        ' ORDER BY timestamp DESC'
    ).fetchone()
    return jsonify({
        'status': 'Default mode and total quantity successfully recorded',
        'data': {
            'id': check['id'],
            'timestamp': check['timestamp'],
            'default_mode': check['default_mode'],
            'total_food_quantity': check['total_food_quantity']
        }
    }), 200
