import discord
import json
import requests
import os
from dotenv import load_dotenv
from discord.ext import commands
import lyricsgenius as lg
from googlesearch import search

load_dotenv()
key = os.getenv('TOKEN_genius')

class Lyrics (commands.Cog):
    def __init__(self, bot):
        self.bot=bot

    #LYRICS LOOK UP 
    #starts
    @commands.command(help='Searches up and gives the link for lyrics from genius.com')
    async def lyrics_link(self,ctx):
            await ctx.send("Enter the name of the song you are searching the lyrics for")
            def check(msg):
                    return msg.author == ctx.author and msg.channel == ctx.channel
            msg = await self.bot.wait_for("message", check=check)
            return_value=search(str(msg.content)+'lyrics genius', tld='co.in', num=1, stop=1, pause=0.5)
            for j in return_value:
                    await ctx.send(j)
    
    @commands.command(help='Lyrics lookup using GENIUS. command *lyrics song name artist name use quotes if more than one word')
    async def lyrics(self,ctx, msg1, msg2):
            genius = lg.Genius(key)
            song = genius.search_song(title=msg1,artist=msg2)
            await ctx.send(song.lyrics)
            await ctx.send(f'{ctx.author.mention}')

    #ends

def setup(bot):
    bot.add_cog(Lyrics(bot))    