import discord
import os
from dotenv import load_dotenv
import random
from discord.ext import commands
from googlesearch import search
import lyricsgenius as lg
import json
import requests
load_dotenv()
token = os.getenv('TOKEN')
key = os.getenv('TOKEN1')
key1 = os.getenv('TOKEN2')
bot = commands.Bot(command_prefix='*')
@bot.event
async def on_ready():
	for guild in bot.guilds:
    		if (guild.name == guild):
            		break

	print(f'{bot.user} is up online:\n')

#GREETINGS SECTION
#starts
@bot.command(pass_context=True, help='Greets back the user', aliases=['hey','yo','hi','konichiwa','yoo'])
async def hello(ctx):			
    quotes =  ['hey!!!','yo!!!','hi!!!','Konnichiwa!!!','Hola!!','Bonjour!!','Namaste!!','heyooo!!'] 
    response = random.choice(quotes)
    await ctx.send(f'{response} {ctx.author.mention}')
#ends 

#GOOGLE SEARCH 
#starts 
@bot.command(pass_help='Google Search')
async def gsearch( ctx, n :int):
        await ctx.send("Type the search query")
        def check(msg):
                return msg.author == ctx.author and msg.channel == ctx.channel
        msg = await bot.wait_for("message", check=check)
        return_value=search(str(msg.content), tld='co.in', num=n, stop=n, pause=1)
        for j in return_value:
                await ctx.send(j)
#ends

#LYRICS LOOK UP 
#starts
@bot.command(help='Searches up and gives the link for lyrics from genius.com')
async def lyrics_link( ctx):
        await ctx.send("Enter the name of the song you are searching the lyrics for")
        def check(msg):
                return msg.author == ctx.author and msg.channel == ctx.channel
        msg = await bot.wait_for("message", check=check)
        return_value=search(str(msg.content)+'lyrics genius', tld='co.in', num=1, stop=1, pause=0.5)
        for j in return_value:
                await ctx.send(j)
  
@bot.command(help='Lyrics lookup using GENIUS. command *lyrics song name artist name use quotes if more than one word')
async def lyrics(ctx, msg1, msg2):
        genius = lg.Genius(key)
        song = genius.search_song(title=msg1,artist=msg2)
        await ctx.send(song.lyrics)
        await ctx.send(f'{ctx.author.mention}')

#ends
@bot.command (help='Youtube video search. *ytsearch video title with number of results desired ')
async def ytsearch(ctx, *, info):
          query = " ".join(info.split(" ")[0:-1]).replace(" ","+")
          num = int(info.split(" ")[-1])
          req = f"https://www.googleapis.com/youtube/v3/search?part=snippet&maxResults={num}&q={query}&key={key1}"
          response = requests.get(req)
          for item in response.json()["items"]:
                 if item["id"]["kind"] == "youtube#playlist":
                         await ctx.send("https://www.youtube.com/watch?v=temp&list="+item["id"]["playlistId"])
                 elif item["id"]["kind"] == "youtube#video":
                         await ctx.send("https://www.youtube.com/watch?v="+item["id"]["videoId"])
                
    
        
bot.run(token)
