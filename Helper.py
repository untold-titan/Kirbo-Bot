import requests
import ast
from discord import Color
import Datatypes

# Firebase Authentication/Initialization. Requires the kirbo-service-account-key.json file to be SOMEWHERE on the server/device you're running it on.

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Use a service account
cred = credentials.Certificate('kirbo-service-account-key.json')
firebase_admin.initialize_app(cred)

db = firestore.client()


USER_URL="https://cataclysmapi20211218110154.azurewebsites.net/api/users/"

FACTION_URL="https://cataclysmapi20211218110154.azurewebsites.net/api/factions/"

MAPS_URL="https://cataclysmapi20211218110154.azurewebsites.net/api/maps/"

PINK = Color.from_rgb(255,185,209)

# Gets all users from the Firebase database, returns List<Datatypes.User>
def getAllUsers():
    users = []
    docs = db.collection(u'users')
    for doc in docs:
        users.append(Datatypes.User.from_dict(doc.to_dict()))
    return users
        
# Gets a particual user from their Discord ID, returns Datatypes.User
def getUserData(id):
    doc_ref = db.collection(u'users').document(f'{id}')
    doc = doc_ref.get()
    if doc.exists:
        user = Datatypes.User.from_dict(doc.to_dict())
        return user
    else:
        return None

# Takes in a Datatype.User and sends it to the Firebase Database, or creates the user if it doesn't exist
# Returns True if the user exists, and was updated, and returns False if the user was created.
def updateUser(user):
    doc = db.collection(u'users').document(f"{user.id}").get()
    if doc.exists:
        db.collection(u'users').document(f"{user.id}").update(user.to_dict())
        return True
    else:
        db.collection(u'users').document(f"{user.id}").set(user.to_dict())
        return False

def getAllFactions():
    response = requests.get(FACTION_URL)
    if response.status_code != 200:
        return None
    else:
        jsonResponse = ast.literal_eval(str(response.json()))
        return jsonResponse


def getAllMapTiles():
    response = requests.get(MAPS_URL)
    if response.status_code != 200:
        return None
    else:
        jsonResponse = ast.literal_eval(str(response.json()))
        return jsonResponse

def getMapTile(id):
    response = requests.get(MAPS_URL + str(id))
    if response.status_code != 200:
        return None
    else: 
        jsonResponse = ast.literal_eval(str(response.json()))
        return jsonResponse

def claimMapTile(id,newOwner):
    response = requests.get(MAPS_URL + str(id))
    if response.status_code != 200:
        return None
    else: 
        jsonRespnse = ast.literal_eval(str(response.json()))
        jsonRespnse["plotOwner"] = newOwner

        response = requests.put(MAPS_URL + str(id),json=jsonRespnse)
        print(response.content)
        if response.status_code != 204:
            return None
        else:
            return True


def getUserFaction(id):
    response = getAllFactions()
    for x in response:
        factionData = ast.literal_eval(str(x))
        if ',' in factionData["factionMembers"]:
            members = str(factionData["factionMembers"]).split(",")
            for y in members:
                if y == str(id):
                    return factionData
        else:
            if factionData["factionMembers"] == str(id):
                return factionData

def updateFaction(faction):
    json = {
        "id":faction["id"],
        "factionName":faction["factionName"],
        "factionIncome":faction["factionIncome"],
        "factionMembers":faction["factionMembers"],
        "factionLogo":faction["factionLogo"],
        "attack":faction["attack"],
        "defense":faction["defense"],
        "utility":faction["utility"],
        "balance":faction["balance"]
        }
    response = requests.put(FACTION_URL+str(faction["id"]),json=json)
    return response