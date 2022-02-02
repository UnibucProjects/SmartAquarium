from db import get_db
from datetime import datetime


def feed_the_fish():
    current_time = datetime.now()
    current_hour = current_time.strftime("%H:%M")

    message_queue_feeding = ""

    feeding_schedules = get_db().execute(
        'SELECT id, food_type_id, aquarium_id, schedule, available_type_quantity'
        ' FROM feeding_schedule'
    ).fetchall()

    if feeding_schedules is not None:
        for fs in feeding_schedules:
            hours = str(fs['schedule']).split(';')
            food_tid = fs['food_type_id']
            fs_id = fs['id']
            aquarium_id = fs['aquarium_id']
            if current_hour in hours:
                food_to_be_released = get_db().execute(
                    'SELECT type, quantity'
                    ' FROM FOOD'
                    f" WHERE id={food_tid}"
                ).fetchone()
                if fs['available_type_quantity'] >= food_to_be_released['quantity']:
                    message_queue_feeding += f"Feeding fish in aquarium {fs['aquarium_id']}" \
                                             f"with type {food_to_be_released['type']}"
                    db = get_db()
                    db.execute(
                        'UPDATE feeding_schedule'
                        f" SET available_type_quantity={fs['available_type_quantity'] - food_to_be_released['quantity']}"
                        f" WHERE id={fs_id}"
                    )
                    db.commit()

                    db = get_db()
                    db.execute(
                        'UPDATE aquarium'
                        f" SET total_food_quantity=total_food_quantity - { food_to_be_released['quantity']}"
                        f" WHERE id = {aquarium_id}"
                    )
                    db.commit()
                else:
                    message_queue_feeding += f"You have a new notification! In aquarium {fs['aquarium_id']}" \
                                             f"there is no {food_to_be_released['type']}"

    if message_queue_feeding == "":
        message_queue_feeding = "All fish are fed!"
    return {
        'feeding check': message_queue_feeding
    }





