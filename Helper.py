import requests
import ast

USER_URL="https://cataclysmapi20211218110154.azurewebsites.net/api/users"

FACTION_URL="https://cataclysmapi20211218110154.azurewebsites.net/api/factions"

MAPS_URL="https://cataclysmapi20211218110154.azurewebsites.net/api/maps/"

def getAllUsers():
    response = requests.get(USER_URL)
    if response.status_code != 200:
        return None
    else:
        jsonResponse = ast.literal_eval(str(response.json()))
        return jsonResponse

def getUserData(id):
    url = USER_URL + "/" + str(id)
    response = requests.get(url)
    if response.status_code != 200:
        return None
    else:
        jsonResponse = ast.literal_eval(str(response.json()))
        return jsonResponse

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
        "factionLandClaim":faction["factionLandClaim"],
        "factionLogo":faction["factionLogo"],
        "attack":faction["attack"],
        "defense":faction["defense"],
        "utility":faction["utility"],
        "balance":faction["balance"]
        }
    response = requests.put(FACTION_URL+"/"+str(faction["id"]),json=json)
    return response