import discord
import json
import requests
import os
from dotenv import load_dotenv
from discord.ext import commands
import lyricsgenius as lg
from googlesearch import search
from discordTogether import DiscordTogether

load_dotenv()
key1 = os.getenv('TOKEN_youtube')

class Youthoob (commands.Cog):
    def __init__(self, bot):
            self.bot=bot
            self.togetherControl = DiscordTogether(bot)
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
    
    @commands.command (help='Starts up Youtube together' , aliases=['YT'])
    async def yt(self,ctx):
         if not ctx.message.author.voice:
            await ctx.send("You have not connected to a voice channel \n Join a voice channel to continue")
            return 
         else:      
            link = await self.togetherControl.create_link(ctx.author.voice.channel.id, 'youtube')
            await ctx.send(f"Click the blue link!\n{link}")
def setup(bot):
    bot.add_cog(Youthoob(bot))    