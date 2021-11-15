import discord
import os
from dotenv import load_dotenv
import random
from discord.ext import commands, tasks
from random import choice
#from discord.voice_client import VoiceClient
import lavalink
from discord import Embed
import math


load_dotenv()


class Music (commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.music = lavalink.Client(self.bot.user.id)
        self.bot.music.add_node('localhost', 9696, 'BITCH', 'eu', 'node_music')
        self.bot.add_listener(
            self.bot.music.voice_update_handler, 'on_socket_response')
        self.bot.music.add_event_hook(self.track_hook)

    @commands.command(name='Join', help='This command makes the bot join the voice channel', aliases=['join'])
    async def join(self, ctx):
        if not ctx.message.author.voice:
            await ctx.send("You have not connected to a voice channel \n Join a voice channel to continue")
            return

        else:
            # channel = ctx.message.author.voice.channel
            # await channel.connect()
            voice_channel = ctx.message.author.voice.channel
            player = self.bot.music.player_manager.create(
                ctx.guild.id, endpoint=str(ctx.guild.region))
            if not player.is_connected:
                player.store('channel', ctx.channel.id)
                await self.connect_to(ctx.guild.id, str(voice_channel.id))

    @commands.command(name='play', help='This commands make the bot to play the song of your choice', aliases=['Play'])
    async def play(self, ctx, *, query):
        await ctx.invoke(self.bot.get_command('Join'))
        def check(m):
            return m.author.id == ctx.author.id

        
        option = query.split()[-1]
        query = query[:-1]

        player = self.bot.music.player_manager.get(ctx.guild.id)
        query = f'ytsearch:{query}'
        results = await player.node.get_tracks(query)

        if option=='l':
            tracks = results['tracks'][0]
       
        else:
            tracks = results['tracks'][0:5]
        
        i = 0
        query_result = ''
        for track in tracks:
            i = i + 1
            query_result = query_result + \
                f"{i} {track['info']['title']} - {track['info']['uri']}\n\n\n"

        embed = Embed(color=discord.Color.from_rgb(255, 0, 0))
        embed.description = query_result

        await ctx.channel.send(embed=embed)

        response = await self.bot.wait_for('message', check=check)
        track = tracks[int(response.content)-1]

        player.add(requester=ctx.author.id, track=track)
        if not player.is_playing:
            await player.play()

        # except Exception as error:
        #      print(error)

    async def track_hook(self, event):
        if isinstance(event, lavalink.events.QueueEndEvent):
            guild_id = int(event.player.guild_id)
            await self.connect_to(guild_id, None)

    async def connect_to(self, guild_id: int, channel_id: str):
        ws = self.bot._connection._get_websocket(guild_id)
        await ws.voice_state(str(guild_id), channel_id)

    @commands.command(help="This command helps the current queue of the songs playing", aliases=["Queue"])
    async def queue(self, ctx, page: int = 1):
        player = self.bot.music.player_manager.get(ctx.guild.id)
        queue = player.queue
        items_per_page = 15
        pages = math.ceil(len(queue)/items_per_page)
        start = (page-1)*items_per_page
        end = start + items_per_page
        description = f"Currently Playing: **[{player.current.title}]** **({player.current.uri})**\n\n"
        if len(queue):
            for index, track in enumerate(queue[start:end], start=1):
                requester = ctx.guild.get_member(track.requester)
                description += f"{index}. **{track.title}** ({track.uri})\n"
        elif player.current == None:
            description = "Queue is Empty, /n Add some songs"
            

        embed = discord.Embed(title="Current Playlist",color=discord.Color.dark_teal(),description=description)

        embed.set_footer(text=f'{page}/{pages}\n')  
        await ctx.send(embed=embed)  

    @commands.command(name='pause', help='This command makes the player pause', aliases=['Pause'])
    async def pause(self, ctx):
        player = self.bot.music.player_manager.get_player(ctx)

        if player.is_paused:
            embed= discord.Embed(title="Player is already Paused\n\nPlay to continue",color=discord.Color.dark_red())
        
        await player.set_pause(True)  
        embed = discord.Embed(title="Paused",color=discord.Color.blue())  
    
    # @commands.command(name='resume', help='This command makes the player pause', aliases=['Resume'])
    # async def resume(self, ctx):
    #     player = self.get_player(ctx)

    #   if player.is_paused:
    #        embed= discord.Embed(title="Player is already Paused\n\nPlay to continue",color=discord.Color.dark_red())
        
    #    await player.set_pause(True)  
    #    embed = discord.Embed(title="Paused",color=discord.Color.blue())  
    
    @commands.command(name='Leave', help='This command makes the bot leave the voice channel', aliases=['leave'])
    async def leave(self, ctx):
      
        player = self.bot.music.player_manager.get(ctx.guild.id)

        if not player.is_connected:
            return await ctx.send('Not connected.')

        if not ctx.author.voice or (player.is_connected and ctx.author.voice.channel.id != int(player.channel_id)):
            return await ctx.send('You\'re not in my voicechannel!')

        player.queue.clear()
     
        await player.stop()
       
        await ctx.guild.change_voice_state(channel=None)
        await ctx.send(' Disconnected.')

    # async def stop(self, ctx):
    #     VoiceClient = ctx.voice_client
    #     await VoiceClient.disconnect()


def setup(bot):
    bot.add_cog(Music(bot))
