#from discord.ext import commands
from dotenv import load_dotenv
import os
#import requests
import discord
import sqlite3
#import mysql.connector
#from mysql.connector import Error

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")

con = sqlite3.connect('suggestions.db')
cur = con.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS requests(songs text PRIMARY KEY collate nocase )""")

bot = discord.Bot()

@bot.event
async def on_ready():
    print("I'm ready!")
    channel = bot.get_channel(CHANNEL_ID)
    #await channel.send("Hello world!")

@bot.slash_command()
async def hello(ctx):
    await ctx.send("Hello!")

@bot.command(name="show_dances", description="This shows all the dance requests. <3")
async def show_dances(ctx):
    embed = discord.Embed(
        title=f"Dance Suggestions",
        color=discord.Color.blurple(),

    )

    cur.execute('''SELECT * FROM requests''')
    all = cur.fetchall()
    update_1 = all
    for row in range(len(update_1)):
        embed.add_field(name='request ' + str(row+1), value=update_1[row][0], inline=False)
    await ctx.send_response(embed=embed)

@bot.slash_command(name="add_dance", description="This adds a dance to the list. <3", pass_context = True)
async def add_dance(ctx, dance: str):
    cur.execute('''INSERT OR IGNORE INTO requests VALUES (:songs)''',{"songs" : dance})
    con.commit()
    cur.execute('''SELECT * FROM requests''')
    row_count = cur.rowcount
    print("number of affected rows: {}".format(row_count))
    if row_count == 0:
        await ctx.send_response(dance + " has been added to the list.")
    else:
        await ctx.send_response(dance + " has already been added to the list.")

@bot.slash_command(name="remove_dance", description="Removes dance. Only type the request number above the dance to be removed. <3",pass_context = True) #Danny coded this
async def remove_dance(ctx, dance: str):
    copyList = []

    cur.execute("SELECT * FROM requests")
    all = cur.fetchall()
    for i in all:
        copyList.append(i)
        print(i)

    wow = copyList[int(dance)-1]
    copyList.pop(int(dance)-1)
    update = '''DELETE FROM requests WHERE songs = ? '''
    cur.execute(update, (wow[0],))
    con.commit()

    await ctx.send_response("request " + dance + " has been removed from the list.")
bot.run(BOT_TOKEN)