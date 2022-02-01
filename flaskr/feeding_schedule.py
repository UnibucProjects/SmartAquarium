from flask import (Blueprint, request, jsonify)
from db import get_db


bp = Blueprint("feeding_schedule", __name__)


@bp.route("/feeding_schedule", methods=["GET"])
def get_feeding_schedule():
    all_feeding_schedules = get_db().execute(
        'SELECT * '
        'FROM feeding_schedule '
        'ORDER BY timestamp DESC'
    ).fetchall()

    result = ""
    for fs in all_feeding_schedules:
        fields = [str(fs["id"]), f"aquarium={str(fs['aquarium_id'])}", f"food_type={str(fs['food_type_id'])}",
                  f"schedule={str(fs['schedule'])}", f"available_type_quantity={str(fs['available_type_quantity'])}",
                  str(fs["timestamp"])]
        result += " ".join(fields)

    return result


@bp.route("/feeding_schedule", methods=["POST"])
def set_feeding_schedule():
    aquarium_id = request.form["aquarium_id"]
    food_type_id = request.form["food_type_id"]
    schedule = request.form["schedule"]
    available_type_quantity = request.form["available_type_quantity"]

    if not aquarium_id:
        return jsonify({"status": "Aquarium is required."}), 403
    elif not food_type_id:
        return jsonify({"status": "Food type is required."}), 403
    elif not schedule:
        return jsonify({"status": "Status is required."}), 403
    elif not available_type_quantity:
        return jsonify({"status": "Available type quantity is required."}), 403

    print(aquarium_id)
    print(food_type_id)
    print(schedule)
    print(available_type_quantity)

    db = get_db()
    db.execute(
        'INSERT INTO feeding_schedule(aquarium_id, food_type_id, schedule, available_type_quantity) '
        'VALUES (?, ?, ?, ?)',
        (aquarium_id, food_type_id, schedule, available_type_quantity)
    )
    db.commit()

    check = get_db().execute(
        'SELECT * '
        'FROM feeding_schedule '
        'ORDER BY timestamp DESC'
    ).fetchone()

    return jsonify({
        "status": "Feeding schedule successfully recorded.",
        "data": {
            "id": check["id"],
            "aquarium_id": check["aquarium_id"],
            "food_type_id": check["food_type_id"],
            "schedule": check["schedule"],
            "available_type_quantity": check["available_type_quantity"],
            "timestamp": check["timestamp"]
        }
    }), 200


@bp.route("/feeding_schedule", methods=["PUT"])
def update_feeding_schedule():
    feeding_id = request.form["id"]
    aquarium_id = request.form["aquarium_id"]
    food_type_id = request.form["food_type_id"]
    schedule = request.form["schedule"]
    available_type_quantity = request.form["available_type_quantity"]

    if not feeding_id:
        return jsonify({"status": "Feeding schedule id is required."}), 403
    elif not aquarium_id:
        return jsonify({"status": "Aquarium is required."}), 403
    elif not food_type_id:
        return jsonify({"status": "Food type is required."}), 403
    elif not schedule:
        return jsonify({"status": "Status is required."}), 403
    elif not available_type_quantity:
        return jsonify({"status": "Available type quantity is required."}), 403

    print(feeding_id)
    print(aquarium_id)
    print(food_type_id)
    print(schedule)
    print(available_type_quantity)

    db = get_db()
    db.execute(
        'UPDATE feeding_schedule '
        'SET aquarium_id=?, food_type_id=?, schedule=?, available_type_quantity=?, timestamp=CURRENT_TIMESTAMP '
        'WHERE id=?',
        (aquarium_id, food_type_id, schedule, available_type_quantity, feeding_id)
    )
    db.commit()

    check = get_db().execute(
        'SELECT * '
        'FROM feeding_schedule '
        'WHERE id=?',
        (feeding_id,)
    ).fetchone()

    return jsonify({
        "status": "Feeding schedule successfully updated.",
        "data": {
            "id": check["id"],
            "aquarium_id": check["aquarium_id"],
            "food_type_id": check["food_type_id"],
            "schedule": check["schedule"],
            "available_type_quantity": check["available_type_quantity"],
            "timestamp": check["timestamp"]
        }
    }), 200


@bp.route("/feeding_schedule/<string:_id>", methods=["DELETE"])
def delete_feeding_schedule(_id):
    if not _id:
        return jsonify({"status": "Feeding schedule id is required."}), 403

    print(_id)

    db = get_db()
    db.execute(
        'DELETE FROM feeding_schedule '
        'WHERE id=?',
        (_id,)
    )
    db.commit()

    return jsonify({
        "status": "Feeding schedule successfully deleted."
    }), 200
