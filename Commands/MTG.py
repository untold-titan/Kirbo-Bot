import discord
from requests import request
import requests
import Helper
import json
from discord import Color
from discord.ext import commands
from discord.ext.commands.converter import MemberConverter

USER_URL="https://cataclysmapi20211218110154.azurewebsites.net/api/users/"

class MTGCog(commands.Cog):
    def __init__(self,bot):
        self.bot = bot


    # DO NOT TOUCH THIS HOLY FUCK THIS IS PRECARIUOUS AS FUCK
    @commands.command(name="won")
    async def won(self,ctx,member:MemberConverter):
        winner = Helper.getUserData(ctx.author.id)
        loser = Helper.getUserData(member.id)
        if winner != None and loser != None:
            #For when the winner has no values set
            if winner["playedVS"] == "":
                winner["playedVS"] = str(member.id)
                winner["wins"] = "1"
                winner["losses"] = "0"
                res = requests.put(USER_URL + str(ctx.author.id),json=winner)
            #For when the loser has no values set
            if loser["playedVS"] == "":
                loser["playedVS"] = str(ctx.author.id)
                loser["wins"] = "0"
                loser["losses"] = "1"
                res = requests.put(USER_URL + str(member.id),json=loser)
            #in the case that both users already have played against each other
            else:
                ids = winner["playedVS"].split(",")
                wins = winner["wins"].split(",")
                for i in range(len(ids)):
                    if(str(member.id) == ids[i]):
                        win = int(wins[i])
                        win += 1
                        wins[i] = str(win)
                        winner["wins"] = ""
                        for win in wins:
                            winner["wins"] += win + ","
                        winner["wins"] = winner["wins"].rstrip(winner["wins"][-1])
                    if(member.id != ids[i] and i == len(ids)):
                        winner["playedVS"] += "," + member.id
                        winner["wins"] += ",1"
                        winner["losses"] += ",0"
                ids = loser["playedVS"].split(",")
                losses = loser["losses"].split(",")
                for i in range(len(ids)):
                    if(str(ctx.author.id) == ids[i]):
                        lose = int(losses[i])
                        lose += 1
                        losses[i] = str(lose)
                        loser["losses"] = ""
                        for lose in losses:
                            loser["losses"] += lose + ","
                        loser["losses"] = loser["losses"].rstrip(loser["losses"][-1])
                    if(member.id != ids[i] and i == len(ids)):
                        loser["playedVS"] += "," + ctx.author.id
                        loser["wins"] += ",0"
                        loser["losses"] += ",1"
            res = requests.put(USER_URL + str(ctx.author.id),json=winner)
            res = requests.put(USER_URL + str(member.id),json=loser)
        elif(winner == None):
            await ctx.send("You need to create a Kirbo account! Use `,bal` or `,daily` to start!")
        elif(loser == None):
            await ctx.send(f"`{member.name}` needs to create a Kirbo account! Use `,bal` or `,daily` to start!")
            
            

            
                    
                    