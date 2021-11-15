import discord
import os
from dotenv import load_dotenv
import random
from discord.ext import commands,tasks
from random import choice
from discord import client


load_dotenv()
token = os.getenv('TOKEN_discord')

bot = commands.Bot(command_prefix='*')



status = ['Trying out something new','Chilling listening to music']
@tasks.loop(seconds=100)
async def change_status():
	await bot.change_presence(activity=discord.Game(choice(status)))
	
@bot.command(name='ping',help='This command returns the latency', aliases=['Ping'])
async def ping(ctx):
	Lat=round(bot.latency * 1000)
	await ctx.send(f'{Lat}ms')
@bot.event
async def on_ready():
	change_status.start()
	for guild in bot.guilds:
    		if (guild.name == guild):
            		break

	print(f'{bot.user} is up online:\n')
	for file in os.listdir('./cogs'):
    		if file.endswith('.py'):
        			bot.load_extension(f'cogs.{file[:-3]}')

#GREETINGS SECTION
#starts
@bot.command(pass_context=True, help='Greets back the user', aliases=['hey','yo','hi','konichiwa','yoo'])
async def hello(ctx):			
    quotes =  ['hey!!!','yo!!!','hi!!!','Konnichiwa!!!','Hola!!','Bonjour!!','Namaste!!','heyooo!!'] 
    response = random.choice(quotes)
    await ctx.send(f'{response} {ctx.author.mention}')
#ends 

bot.run(token)