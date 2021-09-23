import discord
import os
from dotenv import load_dotenv
import random
from discord.ext import commands, tasks
from random import choice
from discord.voice_client import VoiceClient
import lavalink
from discord import Embed



load_dotenv()


class Music (commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.music = lavalink.Client(self.bot.user.id)
        self.bot.music.add_node('localhost', 6969, 'BITCH', 'eu', 'node_music')
        self.bot.add_listener(self.bot.music.voice_update_handler, 'on_socket_response')
        self.bot.music.add_event_hook(self.track_hook)

    @commands.command(name='Join', help='This command makes the bot join the voice channel', aliases=['join'])
    async def join(self, ctx):
        if not ctx.message.author.voice:
            await ctx.send("You have not connected to a voice channel \n Join a voice channel to continue")
            return

        else:
            channel = ctx.message.author.voice.channel
            await channel.connect()

    @commands.command(name='play', help='This commands make the bot to play the song of your choice', aliases=['Play'])
    async def play(self, ctx, *, query):
        try:
            player = self.bot.music.player_manager.get(ctx.guild.id)
            query = f'ytsearch:{query}'
            results = await player.node.get_tracks(query)
            tracks = results['tracks'][0:5]
            i = 0
            query_result = ''
            for track in tracks:
                i = i + 1
                query_result = query_result + f"{i} {track['info']['title']} - {track['info']['url']}"

            embed = Embed()
            embed.description = query_result

            await ctx.channel.send(embed=embed)

            def check(m):
                return m.author.id == ctx.author.id

            response = await self.bot.wait_for('message', check=check)
            track = tracks[int(response.content)-1]


            player.add(requester=ctx.author.id, track=track)
            if not player.is_playing:
                await player.play()

            



        except Exception as error:
             print(error)



    async def track_hook(self, event):
        if isinstance(event, lavalink.events.QueueEndEvent):
            guild_id = int(event.player.guild_id)
            await self.connect_to(guild_id, None)  

    async def connect_to(self, guild_id: int, channel_id: str):
        ws = self.bot._connection._get_websocket(guild_id)
        await ws.voice_state(str(guild_id), channel_id)



    
    
     
    @commands.command(name='Leave', help='This command makes the bot leave the voice channel', aliases=['leave'])
    async def stop(self, ctx):
        VoiceClient = ctx.voice_client
        await VoiceClient.disconnect()


def setup(bot):
    bot.add_cog(Music(bot))
