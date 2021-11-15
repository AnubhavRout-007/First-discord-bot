import discord
import json
import requests
import os
from dotenv import load_dotenv
from discord.ext import commands

from googlesearch import search

load_dotenv()


class Search (commands.Cog):
    def __init__(self, bot):
        self.bot=bot

    #LYRICS LOOK UP 
    #starts
    @commands.command(help='Enter your Search query and number of results for getting the required number of results' ,aliases=['gsearch'])
    async def GSearch(self,ctx):
            await ctx.send("Enter your Search Query")
            def check(msg):
                    return msg.author == ctx.author and msg.channel == ctx.channel
            msg = await self.bot.wait_for("message", check=check)
            await ctx.send("Enter desired no of results")
            msg1 = await self.bot.wait_for("message", check=check)

            return_value=search(str(msg.content),tld='co.in', num=int(msg1.content),stop=int(msg1.content), pause=0.25)
            
            for j in return_value:
                    await ctx.send(j)
                    
           
     #ends

def setup(bot):
    bot.add_cog(Search(bot))    