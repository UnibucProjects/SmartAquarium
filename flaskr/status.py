from db import get_db

def get_status():
    temperature_data = get_db().execute(
        'SELECT id, timestamp, value'
        ' FROM temperature'
        ' ORDER BY timestamp DESC'
    ).fetchone()
    
    if temperature_data is None:
        return {'status': 'The tempeture isn\'t set'}
    
    return {
        'data': {
            'temperature':{ 
                'data': temperature_data['value'],
                'timestamp': temperature_data['timestamp'] 
                           }
            
        }
    }