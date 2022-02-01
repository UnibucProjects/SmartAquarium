from db import get_db


def fix_temperature():
    aquariums = get_db().execute(
        'SELECT id'
        ' FROM aquarium'
    ).fetchall()

    message_queue_for_aquariums = ""

    if aquariums is not None:
        for aq in aquariums:

            fish_types = get_db().execute(
                'SELECT DISTINCT type_id'
                ' FROM fish'
                ' WHERE aquarium_id = ?'
                ' ORDER BY timestamp DESC',
                str(aq['id'])
            ).fetchall()

            if fish_types is not None:
                fishes = []
                # if no intersection is found, temp is fixed to 15
                lowest = [15]
                highest = [15]
                for x in fish_types:
                    fishes.append(str(x['type_id']))
                    check_val = x['type_id']
                    lowest_possible = get_db().execute(
                        'SELECT min_temperature'
                        ' FROM fish_type'
                        f' WHERE id={check_val}',
                    ).fetchone()
                    lowest.append(lowest_possible['min_temperature'])

                    highest_possible = get_db().execute(
                        'SELECT max_temperature'
                        ' FROM fish_type'
                        f' WHERE id={check_val}'
                    ).fetchone()
                    highest.append(highest_possible['max_temperature'])

                new_temperature = (max(lowest) + min(highest))/2

                db = get_db()
                db.execute(
                    'UPDATE water'
                    ' SET temperature=?, timestamp=CURRENT_TIMESTAMP'
                    ' WHERE id=?',
                    (new_temperature, str(aq['id']))
                )
                db.commit()
                message_queue_for_aquariums += f"--aquarium {aq['id']} " \
                                               f"temperature was examined and set to {new_temperature}.-- "

    return {
        'temperature check': message_queue_for_aquariums
    }
