from urllib import response
import requests
import random


tilesToCreate = 100
for x in range(tilesToCreate):
    print(x)
    plot = random.randrange(1,4)
    json={
        "plotNum":x + 1,
        "plotOwner":0,
        "plotType":plot
    }
    response = requests.post("https://cataclysmapi20211218110154.azurewebsites.net/api/maps",json=json)
    if(response.status_code != 201):
        print(response)
        print("Error occured")
        quit()