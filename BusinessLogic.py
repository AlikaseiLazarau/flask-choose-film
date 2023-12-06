from firebase_admin import credentials, firestore, initialize_app
import json
import NetworkRequests
import random

from Models import FilmSelection

# Initialize Firestore DB
cred = credentials.Certificate('key.json')
default_app = initialize_app(cred)
db = firestore.client()
rooms_ref = db.collection('rooms')


# firebase = firebase.FirebaseApplication('https://choose-film-default-rtdb.europe-west1.firebasedatabase.app', None)

# def createRoom() -> str:
#     room_data = {}
#     result = rooms_ref.stream()
#     for doc in result:
#         room_data[doc.id] = doc.to_dict()
#
#     # Convert the dictionary to JSON
#     json_result = json.dumps(room_data, indent=4)
#
#     return json_result

def createRoom(ownerId: str) -> str:
    # room_data = {}
    # result = rooms_ref.stream()
    # for doc in result:
    #     room_data[doc.id] = doc.to_dict()
    #
    # # Convert the dictionary to JSON
    # json_result = json.dumps(room_data, indent=4)
    randomFilmsList = NetworkRequests.getRandomFilmsArray()

    random_int = random.randint(10**7, 10**8 - 1)
    random_int_str = str(random_int).zfill(8)

    rooms_ref.document(random_int_str).set({"films": randomFilmsList, "ownerId": ownerId})

    return random_int_str

def getRoom(id: str, userId: str) -> str:
    result = rooms_ref.document(id)
    result.set({"userId": userId}, merge=True)
    snapshot = result.get()
    if snapshot.exists:
        doc_dict = snapshot.to_dict()
        return json.dumps(doc_dict, indent=4)
    else:
        return "Document not found"
def selectFilmsInRoom(model) -> bool:
    print(model)

    model = FilmSelection(
        user_id=model.get('userId'),
        room_id=model.get('roomId'),
        selected_films_ids=model.get('selectedFilmsIds', [])
    )

    room_ref = rooms_ref.document(str(model.roomId))
    room = room_ref.get().to_dict()

    if room:
        if room.get('ownerId') == str(model.userId):
            room_ref.set({"ownerFilmsIds": model.selectedFilmsIds}, merge=True)

        if room.get('userId') == str(model.userId):
            room_ref.set({"userFilmsIds": model.selectedFilmsIds}, merge=True)

        room_ref = rooms_ref.document(str(model.roomId))
        room = room_ref.get().to_dict()

        if room.get('ownerFilmsIds') and room.get('userFilmsIds'):
            notifyUsersThatRoomComplete(room.get('ownerId'), room.get('userId'), model.roomId)
            return True

        return False
    else:
        return "Document not found"

def notifyUsersThatRoomComplete(ownerId, userId, roomId):
    print(ownerId)
    print(userId)
    print(roomId)
