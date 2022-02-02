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


def quality_check():
    min_ph = 4
    max_ph = 6
    min_oxygen = 50
    max_oxygen = 90

    default_ph = 5
    default_oxygen = 70


    aquariums = get_db().execute(
        'SELECT id'
        ' FROM aquarium'
    ).fetchall()

    message_queue = ""
    db = get_db()

    if aquariums is not None:
        for aq in aquariums:
            aq_id = aq['id']
            water_status = db.execute(
                'SELECT *'
                ' FROM water'
                f' WHERE aquarium_id={aq_id}'
                ' ORDER BY id DESC'
            ).fetchone()
            if water_status is not None:
                message_queue += f"--aquarium {aq['id']}:"
                issues = 0
                if water_status['pH'] > max_ph:
                    message_queue += " WARNING: pH levels too high."
                    message_queue += f" Resetting to {default_ph}."
                    db.execute(
                        'UPDATE water'
                        ' SET pH=?'
                        ' WHERE id=?',
                        (default_ph, water_status['id'])
                    )
                    db.commit()
                    issues += 1
                elif water_status['pH'] < min_ph:
                    message_queue += " WARNING: pH levels too low."
                    message_queue += f" Resetting to {default_ph}."
                    db.execute(
                        'UPDATE water'
                        ' SET pH=?'
                        ' WHERE id=?',
                        (default_ph, water_status['id'])
                    )
                    db.commit()
                    issues += 1

                if water_status['oxygen'] > max_oxygen:
                    message_queue += " WARNING: Oxygen levels too high."
                    message_queue += f" Resetting to {default_oxygen}."
                    db.execute(
                        'UPDATE water'
                        ' SET oxygen=?'
                        ' WHERE id=?',
                        (default_oxygen, water_status['id'])
                    )
                    db.commit()
                    issues += 1
                elif water_status['oxygen'] < min_oxygen:
                    message_queue += " WARNING: Oxygen levels too low."
                    message_queue += f" Resetting to {default_oxygen}."
                    db.execute(
                        'UPDATE water'
                        ' SET oxygen=?'
                        ' WHERE id=?',
                        (default_oxygen, water_status['id'])
                    )
                    db.commit()
                    issues += 1

                if water_status['bacteria'] > 0:
                    message_queue += " WARNING: Bacteria detected. Cleaning up"
                    db.execute(
                        'UPDATE water'
                        ' SET bacteria=0'
                        ' WHERE id=?',
                        (water_status['id'],)
                    )
                    db.commit()
                    issues += 1

                if issues == 0:
                    message_queue += ' No issues detected.'

    return {
        'water quality check': message_queue
    }
