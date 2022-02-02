from flask import Flask
from threading import Thread
from flask_mqtt import Mqtt
from flask_socketio import SocketIO
from flask_restful import Api, Resource

from water_data_sender import parse_data, send_data
from change_light import LightColor
from aquarium_mode import AquariumMode
import db
import auth
import food
import aquarium
import feeding_schedule
import water_preferences
import light_preferences
import status
import fish_type
import facility
import fish
import water
import light
import feed

import eventlet
import json
import time
import os

eventlet.monkey_patch()

app = None
api = None
mqtt = None
socketio = None
thread = None
thread_water_prefs = None
thread_feed_check = None
topic = 'python/mqtt'


def create_app(test_config=None):

    # create and configure the app
    global app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    @app.route('/')
    def hello():
        global thread, thread_water_prefs, thread_feed_check, thread_light_prefs
        if thread is None:
            thread = Thread(target=background_thread)
            thread.daemon = True
            thread.start()

            thread_water_prefs = Thread(target=thread_water_preferences)
            thread_water_prefs.daemon = True
            thread_water_prefs.start()

            thread_water_data = Thread(target=tread_send_water_data)
            thread_water_data.daemon = True
            thread_water_data.start()

            thread_feed_check = Thread(target=thread_feed_fish)
            thread_feed_check.daemon = True
            thread_feed_check.start()

            thread_light_prefs = Thread(target=thread_light_preferences)
            thread_light_prefs.daemon = True
            thread_light_prefs.start()

        return 'Hello, World!'

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    db.init_app(app)
    app.register_blueprint(auth.bp)
    app.register_blueprint(food.bp)
    app.register_blueprint(fish_type.bp)
    app.register_blueprint(aquarium.bp)
    app.register_blueprint(feeding_schedule.bp)
    app.register_blueprint(facility.bp)
    app.register_blueprint(fish.bp)
    app.register_blueprint(water.bp)
    app.register_blueprint(light.bp)
    return app


def background_thread():
    count = 0
    while True:
        time.sleep(7)
        # Using app context is required because the get_status() functions
        # requires access to the db.
        with app.app_context():
            # message = 'dummy message'
            message = json.dumps(status.get_status(), default=str)
        # Publish
        mqtt.publish(topic, message)


def thread_feed_fish():
    while True:
        with app.app_context():
            message = '\n\nFeeding schedule check!\n'
            message += json.dumps(feed.feed_the_fish(), default=str)
            message += '\n'
        # Publish
        mqtt.publish(topic, message)
        time.sleep(4)


def thread_water_preferences():
    while True:
        time.sleep(3)
        with app.app_context():
            message = '\nTemperature auto-check!\n'
            message += json.dumps(water_preferences.fix_temperature(), default=str)
            message += '\n\nWater quality summary\n'
            message += json.dumps(water_preferences.quality_check(), default=str)
            message += '\n'
        # Publish
        mqtt.publish(topic, message)


def thread_light_preferences():
    while True:
        time.sleep(5)
        with app.app_context():
            message = '\nLight intensity auto-check!\n'
            message += json.dumps(light_preferences.fix_light_intensity(), default=str)
            message += '\n'
        # Publish
        mqtt.publish(topic, message)


def tread_send_water_data():
    water_data = parse_data('WaterData.csv')
    sleepTime = 11
    aquarium_id = 1
    url = 'http://[::1]:5000/water'
    send_data(water_data, aquarium_id, sleepTime, url)


def create_rest_api(app):

    api = Api(app)
    api.add_resource(AquariumMode, '/aquariumMode/<int:id>')
    api.add_resource(LightColor, '/lightColor/<int:aquarium_id>')
    return api


def create_mqtt_app():
    global app
    # Setup connection to mqtt broker
    app.config['MQTT_BROKER_URL'] = 'localhost'
    app.config['MQTT_BROKER_PORT'] = 1883  # default port for non-tls connection
    app.config['MQTT_USERNAME'] = ''  # set the username here if you need authentication for the broker
    app.config['MQTT_PASSWORD'] = ''  # set the password here if the broker demands authentication
    app.config['MQTT_KEEPALIVE'] = 5  # set the time interval for sending a ping to the broker to 5 seconds
    app.config['MQTT_TLS_ENABLED'] = False  # set TLS to disabled for testing purposes

    global mqtt
    mqtt = Mqtt(app)
    global socketio
    socketio = SocketIO(app, async_mode="eventlet")


def run_socketio_app():
    global app
    create_app()
    create_rest_api(app)
    create_mqtt_app()
    socketio.run(app, host='localhost', port=5000, use_reloader=False, debug=True)


if __name__ == '__main__':
    run_socketio_app()
