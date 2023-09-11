import { apiUrl, gamerRoleId } from "./data/vars"

export async function handleEvent(data) {
    let command = data["data"]["name"]
    if(command == "about"){
        console.log("about command sent")
        respondWithMessage(data["id"], data["token"], "Holy shit this command worked!")
        return;
    }
    if(command == "join_gamers"){
        respondWithMessage(data["id"], data["token"], "Request received. Granting access to gaming wing.")
        giveUserRole(gamerRoleId, data["guild_id"], data["member"]["user"]["id"])
        return;
    }

}

function giveUserRole(roleId, guildId, userId){
    fetch(apiUrl + "guilds/" + guildId + "/members/" + userId + "/roles/" + roleId,{
        method:"PUT",
        headers:{
            "Authorization":"Bot " + Bun.env.TOKEN 
        }
    }).then(res => {
        if(!res.ok)
            console.error("Failed to add role to user!")
        return res.ok
    })
}

function respondWithMessage(id,token,reply){
    fetch(apiUrl + "interactions/" + id + "/" + token + "/callback",{
        method:"POST",
        headers:{
            "Content-Type":"application/json"
        },
        body:JSON.stringify({
            "type":4,
            "data":{
                "content":reply
            }
        })
    }).then((res) => {
        if(!res.ok)
            console.error("Failed to reply to interaction!")
        return res.ok
    }).catch(() => {
        throw new Error("HTTP request FAILED")
    })
}