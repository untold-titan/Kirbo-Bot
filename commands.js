import { apiUrl } from "./data/vars"

// Registers commands in the discord API.
const commandFile = Bun.file("data/commands.json")

const commandData = await JSON.parse(await commandFile.text())

commandData["commands"].forEach(async command => {
    console.log(command)
    let url = apiUrl + "applications/" + Bun.env.APP_ID + "/guilds/" + Bun.env.GUILD_ID + "/commands"
    console.log(url)
    let res = await fetch(url,{
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Authorization": "Bot " + Bun.env.TOKEN
        },
        body:JSON.stringify(command)
    })
    console.log(res.status)
})