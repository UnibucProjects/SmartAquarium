from flask import (Blueprint, request, jsonify)

from db import get_db

bp = Blueprint('light', __name__)


@bp.route('/light', methods=['POST'])
def set_food():
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