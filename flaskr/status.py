from db import get_db


def get_status():
    food_data = get_db().execute(
        'SELECT id, timestamp, type, quantity'
        ' FROM food'
        ' ORDER BY timestamp DESC'
    ).fetchone()
    
    if food_data is None:
        return {'status': 'The food isn\'t set'}
    
    return {
        'data': {
            'food': {
                'type': food_data['type'],
                'quantity': food_data['quantity'],
                'timestamp': food_data['timestamp']
                           }
            
        }
    }
