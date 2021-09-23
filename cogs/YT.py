import discord
import json
import requests
import os
from dotenv import load_dotenv
from discord.ext import commands
import lyricsgenius as lg
from googlesearch import search

load_dotenv()
key1 = os.getenv('TOKEN_youtube')

class Youthoob (commands.Cog):
    def __init__(self, bot):
            self.bot=bot

    @commands.command (help='Youtube video search. *ytsearch video title with number of results desired ')
    async def ytsearch(self,ctx, *, info):
            query = " ".join(info.split(" ")[0:-1]).replace(" ","+")
            num = int(info.split(" ")[-1])
            req = f"https://www.googleapis.com/youtube/v3/search?part=snippet&maxResults={num}&q={query}&key={key1}"
            response = requests.get(req)
            for item in response.json()["items"]:
                    if item["id"]["kind"] == "youtube#playlist":
                            await ctx.send("https://www.youtube.com/watch?v=temp&list="+item["id"]["playlistId"])
                    elif item["id"]["kind"] == "youtube#video":
                            await ctx.send("https://www.youtube.com/watch?v="+item["id"]["videoId"])


def setup(bot):
    bot.add_cog(Youthoob(bot))    