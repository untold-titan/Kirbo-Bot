import asyncio
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
        await ctx.send(f"{member} type `y` to confirm that you LOST against {ctx.author.name}")
        def check(m: discord.Message):
            return m.author.id == member.id and m.channel.id == ctx.channel.id and m.content == "y" or "Y" 
        try:
            msg = await self.bot.wait_for(event = 'message', check = check, timeout = 60.0)
        except asyncio.TimeoutError:
            await ctx.send(f"Automatically declined win.")
            return
        else:
                winner = Helper.getUserData(ctx.author.id)
                loser = Helper.getUserData(member.id)
                if winner != None and loser != None:
                    #in the case that both users already have played against each other
                    ids = winner["playedVS"].split(",")
                    wins = winner["wins"].split(",")
                    if(winner["playedVS"] != ""):
                        for i in range(len(ids)):
                            if(str(member.id) == ids[i]):
                                win = int(wins[i])
                                win += 1
                                wins[i] = str(win)
                                winner["wins"] = ""
                                for win in wins:
                                    winner["wins"] += win + ","
                                winner["wins"] = winner["wins"].rstrip(winner["wins"][-1])
                            elif(member.id != ids[i] and i == len(ids) - 1):
                                winner["playedVS"] += "," + str(member.id)
                                winner["wins"] += ",1"
                                winner["losses"] += ",0"
                    ids = loser["playedVS"].split(",")
                    losses = loser["losses"].split(",")
                    if(loser["playedVS"] != ""):
                        for i in range(len(ids)):
                            if(str(ctx.author.id) == ids[i]):
                                lose = int(losses[i])
                                lose += 1
                                losses[i] = str(lose)
                                loser["losses"] = ""
                                for lose in losses:
                                    loser["losses"] += lose + ","
                                loser["losses"] = loser["losses"].rstrip(loser["losses"][-1])
                            elif(member.id != ids[i] and i == len(ids) - 1):
                                loser["playedVS"] += "," + str(ctx.author.id)
                                loser["wins"] += ",0"
                                loser["losses"] += ",1"
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
                    res = requests.put(USER_URL + str(ctx.author.id),json=winner)
                    res = requests.put(USER_URL + str(member.id),json=loser)
                    await ctx.send("Updated Stats!")
                elif(winner == None):
                    await ctx.send("You need to create a Kirbo account! Use `,bal` or `,daily` to start!")
                elif(loser == None):
                    await ctx.send(f"`{member.name}` needs to create a Kirbo account! Use `,bal` or `,daily` to start!")
        return
    
    @commands.command(name="stats")
    async def stats(self,ctx):
        user = Helper.getUserData(ctx.author.id)
        players = user["playedVS"].split(",")
        wins = user["wins"].split(",")
        losses = user["losses"].split(",")
        embed = discord.Embed(title=f"{ctx.author.name}'s MTG stats",color=Helper.PINK)
        i = 0
        if players[0] == "":
            await ctx.send("You need to play against someone first!")
            return
        for playerID in players:
            player = await self.bot.fetch_user(playerID)
            embed.add_field(name=f"Games against {player.name}",value=f"Wins:{wins[i]}|Losses:{losses[i]}")
            i += 1
        await ctx.send(embed=embed)
            

            
                    
                    