import csv

from app import create_app
from db import get_db


def add_aquariums(aquariums_path):
    file = open(aquariums_path)
    content = csv.reader(file, delimiter=',')
    index = 0
    for line in content:
        if index > 0:
            name, default_mode, total_food_quantity = line
            database = get_db()
            database.execute(
                "INSERT INTO aquarium(name, default_mode, total_food_quantity) "
                "VALUES (?, ?, ?)",
                (name, default_mode, total_food_quantity)
            )
            database.commit()
        index += 1


def add_facilities(facilities_path):
    file = open(facilities_path)
    content = csv.reader(file, delimiter=',')
    index = 0
    for line in content:
        if index > 0:
            aquarium_name, electricity, movement_sensor, temperature_sensor, filter_sensor, weight_sensor = line

            database = get_db()

            aquarium = database.execute(
                "SELECT id "
                "FROM aquarium "
                "WHERE name=?",
                (aquarium_name,)
            ).fetchone()
            aquarium_id = aquarium["id"]

            database.execute(
                "INSERT INTO facility(aquarium_id, electricity, movement_sensor, temperature_sensor, filter_sensor, "
                "weight_sensor) "
                "VALUES (?, ?, ?, ?, ?, ?)",
                (aquarium_id, electricity, movement_sensor, temperature_sensor, filter_sensor, weight_sensor)
            )
            database.commit()
        index += 1


def add_food(food_path):
    file = open(food_path)
    content = csv.reader(file, delimiter=',')
    index = 0
    for line in content:
        if index > 0:
            food_type, quantity = line
            database = get_db()
            database.execute(
                "INSERT INTO food(type, quantity) "
                "VALUES (?, ?)",
                (food_type, quantity)
            )
            database.commit()
        index += 1


def add_feeding_schedules(feeding_schedules_path):
    file = open(feeding_schedules_path)
    content = csv.reader(file, delimiter=',')
    index = 0
    for line in content:
        if index > 0:
            aquarium_name, food_type, schedule, available_type_quantity = line

            database = get_db()

            aquarium = database.execute(
                "SELECT id "
                "FROM aquarium "
                "WHERE name=?",
                (aquarium_name,)
            ).fetchone()
            aquarium_id = aquarium["id"]

            food = database.execute(
                "SELECT id "
                "FROM food "
                "WHERE type=?",
                (food_type,)
            ).fetchone()
            food_id = food["id"]

            database.execute(
                "INSERT INTO feeding_schedule(aquarium_id, food_type_id, schedule, available_type_quantity) "
                "VALUES (?, ?, ?, ?)",
                (aquarium_id, food_id, schedule, available_type_quantity)
            )
            database.commit()
        index += 1


def add_fish_types(fish_types_path):
    file = open(fish_types_path)
    content = csv.reader(file, delimiter=',')
    index = 0
    for line in content:
        if index > 0:
            name, food_type, min_temperature, max_temperature, min_light_intensity, max_light_intensity = line

            database = get_db()

            food = database.execute(
                "SELECT id "
                "FROM food "
                "WHERE type=?",
                (food_type,)
            ).fetchone()
            food_id = food["id"]

            database.execute(
                "INSERT INTO fish_type(name, food_id, min_temperature, max_temperature, min_light_intensity, "
                "max_light_intensity) "
                "VALUES (?, ?, ?, ?, ?, ?)",
                (name, food_id, min_temperature, max_temperature, min_light_intensity, max_light_intensity)
            )
            database.commit()
        index += 1


def add_fish(fish_path):
    file = open(fish_path)
    content = csv.reader(file, delimiter=',')
    index = 0
    for line in content:
        if index > 0:
            fish_type_name, aquarium_name, name, health, birthday = line

            database = get_db()

            fish_type = database.execute(
                "SELECT id "
                "FROM fish_type "
                "WHERE name=?",
                (fish_type_name,)
            ).fetchone()
            fish_type_id = fish_type["id"]

            aquarium = database.execute(
                "SELECT id "
                "FROM aquarium "
                "WHERE name=?",
                (aquarium_name,)
            ).fetchone()
            aquarium_id = aquarium["id"]

            database.execute(
                "INSERT INTO fish(type_id, aquarium_id, name, health, birthday) "
                "VALUES (?, ?, ?, ?, ?)",
                (fish_type_id, aquarium_id, name, health, birthday)
            )
            database.commit()
        index += 1


def add_light(light_path):
    file = open(light_path)
    content = csv.reader(file, delimiter=',')
    index = 0
    for line in content:
        if index > 0:
            aquarium_name, intensity, color, schedule = line

            database = get_db()

            aquarium = database.execute(
                "SELECT id "
                "FROM aquarium "
                "WHERE name=?",
                (aquarium_name,)
            ).fetchone()
            aquarium_id = aquarium["id"]

            database.execute(
                "INSERT INTO light(aquarium_id, intensity, color, schedule) "
                "VALUES (?, ?, ?, ?)",
                (aquarium_id, intensity, color, schedule)
            )
            database.commit()
        index += 1


def add_water(water_path):
    file = open(water_path)
    content = csv.reader(file, delimiter=',')
    index = 0
    for line in content:
        if index > 0:
            aquarium_name, ph, oxygen, bacteria, temperature = line

            database = get_db()

            aquarium = database.execute(
                "SELECT id "
                "FROM aquarium "
                "WHERE name=?",
                (aquarium_name,)
            ).fetchone()
            aquarium_id = aquarium["id"]

            database.execute(
                "INSERT INTO water(aquarium_id, pH, oxygen, bacteria, temperature) "
                "VALUES(?, ?, ?, ?, ?)",
                (aquarium_id, ph, oxygen, bacteria, temperature)
            )
            database.commit()
        index += 1


if __name__ == "__main__":
    local_app = create_app()
    with local_app.app_context():
        add_aquariums("initial_data/aquarium.csv")
        add_facilities("./initial_data/facility.csv")
        add_food("./initial_data/food.csv")
        add_feeding_schedules("./initial_data/feeding_schedule.csv")
        add_fish_types("./initial_data/fish_type.csv")
        add_fish("./initial_data/fish.csv")
        add_light("./initial_data/light.csv")
        add_water("./initial_data/water.csv")
