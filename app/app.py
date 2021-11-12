from subprocess import Popen

from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
from flask_socketio import SocketIO, emit

import constants
from match_utils import MatchUtils

app = Flask(__name__)
app.secret_key = '&(*(**((*@@@#$333(*(*221'
socket_io = SocketIO(app, cors_allowed_origins="*")

app.config.update(SESSION_COOKIE_SAMESITE="None", SESSION_COOKIE_SECURE=True)

cors = CORS(app)

match_utils = MatchUtils()

global match_details
match_details = constants.MATCH_DETAILS_TEMPLATE


@app.route('/start_match', methods=['GET', 'POST'])
@cross_origin(allow_headers=['*'])
def start_match():
    try:
        global match_details
        match_details = match_utils.instantiate_match_details()
        Popen('python .\components\get_live_frames.py')
        # Start live_video_process
        response = jsonify({"response": "Success"}), 200
    except Exception as exception:
        print("Exception", exception)
        response = jsonify({"response": "Error"}), 500
    return response
    # pass


@app.route('/stop_match', methods=['GET', 'POST'])
@cross_origin(allow_headers=['*'])
def stop_match():
    global match_details, live_video_process
    try:
        # terminate live_video_process
        socket_io.emit('kill_self',  {'data': 'Sleep'})
        match_details = constants.MATCH_DETAILS_TEMPLATE
        return jsonify({"response": "Success"}), 200
    except Exception as exception:
        print("Exception", exception)
        return jsonify({"response": "Error"}), 500


@app.route('/register_events', methods=['GET', 'POST'])
@cross_origin(allow_headers=['*'])
def register_events():
    global match_details
    match_details
    events = request.get_json()['events']
    print("events", events)
    try:
        match_details = match_utils.update_match_details(
            match_details, events)
        return jsonify({"response": "Success"}), 200

    except Exception as exception:
        print(exception)
        return jsonify({"response": "Error"}), 500


@app.route('/get_match_details', methods=['GET', 'POST'])
@cross_origin(allow_headers=['*'])
def get_match_details():
    global match_details
    # for testing:
    # testing_details = constants.corematch_example
    # return jsonify({"response": testing_details})
    # print("returning",match_details)
    return jsonify({"response": match_details})


@socket_io.on('connect')
def test_connect():
    global match_details
    print("1 machine connected")
    emit('after connect',  {'data': 'Woke up'})


@socket_io.on('after connect')
@cross_origin(allow_headers=['*'])
def after_connect():
    print("After machine- connected")


@socket_io.on('new_event')
def new_event(data):
    global match_details
    print("new_event", data)
    match_details = match_utils.update_match_details(
        match_details, data["event"])
    print("Sending new match_details")
    emit('receive_details',  {
         'match_details': match_details}, broadcast=True, include_self=False)


@app.route('/edit_team_details', methods=['GET', 'POST'])
@cross_origin(allow_headers=['*'])
def edit_team_details():
    # edit_team_details (eg.team name, logo etc.)in  CURRENT MATCH OBJECT with received details
    return "Not Implemented", 666
    pass


if __name__ == "__main__":
    # socketio.run(app, port=4445, host = socket.gethostbyname(socket.gethostname()),debug='true')
    socket_io.run(app, port=4445, host="127.0.0.1", debug='true')
    # app.run(host='0.0.0.0', port=4445, debug='true')
