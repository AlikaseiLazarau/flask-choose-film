from flask import Flask, render_template, request, url_for, jsonify
import BusinessLogic

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/news')
def get_news():
    return 'News!'

@app.route('/room', methods=['GET'])
def get_room():
    args = request.args
    print(args.get("id"))
    return BusinessLogic.getRoom(args.get("id"), args.get("userId"))

@app.route('/create_room', methods=['GET'])
def create_room():
    args = request.args
    return BusinessLogic.createRoom(args.get("ownerId"))

@app.route('/room_result', methods=['GET'])
def room_result():
    args = request.args
    return BusinessLogic.getRoomResult(args.get("roomId"))

@app.route('/select_films', methods=['POST'])
def select_films():
    input_json = request.get_json(force=True)
    is_room_completed = BusinessLogic.selectFilmsInRoom(input_json)
    dictToReturn = {'isRoomCompleted': is_room_completed}
    return jsonify(dictToReturn)

if __name__ == '__main__':
    app.run(port=8000, debug=True)
