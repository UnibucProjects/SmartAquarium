from db import get_db


def fix_light_intensity():
    aquariums = get_db().execute(
        'SELECT id'
        ' FROM aquarium'
    ).fetchall()

    message_queue = ""
    db = get_db()

    if aquariums is not None:
        for aq in aquariums:

            fish_types = db.execute(
                'SELECT DISTINCT type_id'
                ' FROM fish'
                ' WHERE aquarium_id = ?'
                ' ORDER BY timestamp DESC',
                str(aq['id'])
            ).fetchall()

            if fish_types is not None:
                lowest = [10]
                highest = [10]

                for x in fish_types:
                    check_val = x['type_id']
                    lowest_possible = db.execute(
                        'SELECT min_light_intensity'
                        ' FROM fish_type'
                        f' WHERE id={check_val}'
                    ).fetchone()
                    lowest.append(lowest_possible['min_light_intensity'])

                    highest_possible = db.execute(
                        'SELECT max_light_intensity'
                        ' FROM fish_type'
                        f' WHERE id={check_val}'
                    ).fetchone()
                    highest.append(highest_possible['max_light_intensity'])

                    new_intensity = (max(lowest) + min(highest)) / 2

                    db.execute(
                        'UPDATE light'
                        ' SET intensity=?, timestamp=CURRENT_TIMESTAMP'
                        ' WHERE id=?',
                        (new_intensity, str(aq['id']))
                    )

                    db.commit()
                    message_queue += f"--aquarium {aq['id']} " \
                                     f"light intensity was examined and set to {new_intensity}.-- "
    return {
        'light intensity check': message_queue
    }