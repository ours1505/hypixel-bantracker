#!/bin/env python3
##Author:NyaProxy
#!/bin/env python

import discord
import requests
import asyncio
from discord.ext import commands
import datetime

TOKEN = 'Put Your Discord Bot Token Here'
CHANNEL_ID = 0000000000000000
#Put your ChannelID here!
intents = discord.Intents.default()
intents.typing = False
intents.presences = False
bot = commands.Bot(command_prefix='!', intents=intents)


async def send_to_discord(message):
    channel = bot.get_channel(CHANNEL_ID)
    await channel.send(message)

async def ban_tracker_logic():
    await send_to_discord('Bot restarting....')
    url = 'https://api.hypixel.net/punishmentstats'
    headers = {
        "API-Key": "input your developer dashboard APIKEY Here!"
    }
    resp = requests.post(url, headers=headers)
    watchdog = resp.json()['watchdog_total']
    staff = resp.json()['staff_total']

    while True:
        try:
            resp = requests.post(url, headers=headers)
            if resp.text:
                watchdog_now = resp.json()['watchdog_total']
                staff_now = resp.json()['staff_total']
                outp = ''
                
                if watchdog_now != watchdog:
                    watchdog_num = watchdog_now - watchdog
                    if watchdog_num == 1:
                        outp = f'🐕Watchdog has Banned {watchdog_num} hacker!'
                    if watchdog_num > 1 and watchdog_num < 10:
                        outp = f'🐕Watchdog has Banned {watchdog_num} hackers!'
                    if watchdog_num >= 10:
                        outp = f'🐕Watchdog has Banned {watchdog_num} hackers! Insance!🤡'
                    watchdog = watchdog_now
                    
                if staff_now != staff:
                    if outp:
                        outp = outp + "\n"
                        staff_num = staff_now - staff
                    if staff_num == 1:
                            outp = outp + f'👮Staff has Banned {staff_num} hacker!'
                    if staff_num > 1 and staff_num < 10:
                        outp = outp + f'👮Staff has Banned {staff_num} hackers!'
                    if staff_num >= 10:
                        outp = outp + f'👮Staff has Banned {staff_num} hackers! Insance!🤡'
                    staff = staff_now

            if outp:

                current_time = datetime.datetime.now()
                timestamp = int(current_time.timestamp())  # 将时间转换为 Unix 时间戳
    
                print(outp)
                await send_to_discord(f"{outp} <t:{timestamp}:R>")  # Await the coroutine
        
        except:
            pass
        await asyncio.sleep(1)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    # Start the ban_tracer_logic function in a separate task
    bot.loop.create_task(ban_tracker_logic())

bot.run(TOKEN)
