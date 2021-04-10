import discord
import os
from dotenv import load_dotenv
import random
from discord.ext import commands
from googlesearch import search


load_dotenv()
token = os.getenv('TOKEN')
bot = commands.Bot(command_prefix='.l')
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
@bot.command(help='Google Search')
async def gsearch( ctx, n :int):
        await ctx.send("Type the search query")
        def check(msg):
                return msg.author == ctx.author and msg.channel == ctx.channel
        msg = await bot.wait_for("message", check=check)
        return_value=search(str(msg.content), tld='co.in', num=n, stop=n, pause=1)
        for j in return_value:
                await ctx.send(j)



bot.run(token)
