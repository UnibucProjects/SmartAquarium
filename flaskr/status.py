from db import get_db


def get_status():
    food_data = get_db().execute(
        'SELECT id, timestamp, type, quantity'
        ' FROM food'
        ' ORDER BY timestamp DESC'
    ).fetchone()

    aquarium_data = get_db().execute(
        'SELECT id, timestamp, default_mode, total_food_quantity'
        ' FROM aquarium'
        ' ORDER BY timestamp DESC'
    ).fetchone()

    light_data = get_db().execute(
        'SELECT id, timestamp, aquarium_id, intensity, color, schedule'
        ' FROM light'
        ' ORDER BY timestamp DESC'
    ).fetchone()

    status = ""
    if food_data is None:
        status += 'The food isn\'t set. '
    elif aquarium_data is None:
        status += 'The aquarium isn\'t set. '
    elif light_data is None:
        status += 'The light isn\'t set.'

    if status != "":
        return {'status': status}

    return {
        'data': {
            'food': {
                'type': food_data['type'],
                'quantity': food_data['quantity'],
                'timestamp': food_data['timestamp']
            },
            'aquarium': {
                'default_mode': aquarium_data['default_mode'],
                'total_food_quantity': aquarium_data['total_food_quantity'],
                'timestamp': aquarium_data['timestamp']
            },
            'light': {
                # 'id': light_data['id'],
                'timestamp': light_data['timestamp'],
                'aquarium_id': light_data['aquarium_id'],
                'intensity': light_data['intensity'],
                'color': light_data['color'],
                'schedule': light_data['schedule']
            }

        }
    }


def get_utility_status():
    message_queue_utility = "Attention!  "
    facilities = get_db().execute(
        'SELECT DISTINCT aquarium_id, electricity, movement_sensor, temperature_sensor, filter_sensor, weight_sensor'
        ' FROM facility'
    ).fetchall()
    if facilities is not None:
        for f in facilities:
            if f['electricity'] != '1':
                message_queue_utility += f"-Electricity in aquarium {f['aquarium_id']} seems to be broken. Please fix!-"
            elif f['movement_sensor'] != '1':
                message_queue_utility += f"-Moveement sensor in aquarium {f['aquarium_id']} seems to be broken. Please fix!-"
            elif f['temperature_sensor'] != '1':
                message_queue_utility += f"-Temperature sensor in aquarium {f['aquarium_id']} seems to be broken. Please fix!-"
            elif f['filter_sensor'] != '1':
                message_queue_utility += f"-Filter sensor in aquarium {f['aquarium_id']} seems to be broken. Please fix!-"
            elif f['weight_sensor'] != '1':
                message_queue_utility += f"-Weight sensor in aquarium {f['aquarium_id']} seems to be broken. Please fix!-"
    if message_queue_utility == "Attention!  ":
        message_queue_utility = "All utilities are working fine!"
    return {'utility_status': message_queue_utility}
