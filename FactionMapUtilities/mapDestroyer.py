from urllib import response
import requests

tilesToCreate = 100
for x in range(tilesToCreate):
    print(x)
    response = requests.delete("https://cataclysmapi20211218110154.azurewebsites.net/api/maps/"+str(x + 1))
    if(response.status_code != 204):
        print(response)
        print("Error occured")
        quit()