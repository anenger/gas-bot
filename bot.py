import discord
import os
import json
import requests
import time
import asyncio

client = discord.Client()

def get_gas_prices():
  r = requests.get(f"https://data-api.defipulse.com/api/v1/egs/api/ethgasAPI.json?api-key={os.getenv('API_KEY')}")
  try:
    r.raise_for_status()
    gas_prices = r.json()
    gas_dict = {
      "low": int(gas_prices['safeLow']) / 10,
      "medium": int(gas_prices['fast']) / 10,
      "high": int(gas_prices['fastest']) / 10,
      "average": int(gas_prices['average']) / 10
    }
    return gas_dict
  except Exception as e:
    return "Error fetching gas prices"

async def update_presence():
    prices = get_gas_prices()
    await client.change_presence(activity=discord.Game(f"🐌 {prices['low']} | 🚶 {prices['medium']} | 🔥 {prices['high']}"))
    await asyncio.sleep(15)

@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))
  client.loop.create_task(update_presence())

@client.event
async def on_message(message):
  if message.author == client.user:
    return

  if message.content.startswith('!gas'):
    prices = get_gas_prices()
    embed = discord.Embed(title="Gas Prices")
    embed.add_field(name=":snail: Slow :snail:", value=prices['low'], inline=False)
    embed.add_field(name=":person_walking: Medium :person_walking:", value=prices['medium'], inline=False)
    embed.add_field(name=":fire: Fast :fire:", value=prices['high'], inline=False)
    embed.add_field(name=":blue_circle: Average :blue_circle:", value=prices['average'], inline=False)
    await message.channel.send(embed=embed)

if __name__ == "__main__":
  client.run(os.getenv('TOKEN'))