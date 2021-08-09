import discord
import os
import json
from web3 import Web3
from web3.gas_strategies.time_based import slow_gas_price_strategy, medium_gas_price_strategy, fast_gas_price_strategy

w3 = Web3(Web3.HTTPProvider(os.getenv('ETH_API')))

client = discord.Client()

def get_gas_prices():
    w3.eth.set_gas_price_strategy(slow_gas_price_strategy)
    slow = w3.toWei(w3.eth.generate_gas_price(), 'gwei')

    w3.eth.set_gas_price_strategy(medium_gas_price_strategy)
    med = w3.toWei(w3.eth.generate_gas_price(),'gwei')

    w3.eth.set_gas_price_strategy(fast_gas_price_strategy)
    fast = w3.toWei(w3.eth.generate_gas_price(),'gwei')

    return (slow, med, fast)

@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
    return

  if message.content.startswith('!gas'):
    prices = get_gas_prices()
    embed = discord.Embed(title="Gas Prices")
    embed.add_field(name="Slow Gas", value=prices[0])
    embed.add_field(name="Medium Gas", value=prices[1])
    embed.add_field(name="Fast Gas", value=prices[2])
    await message.send(embed=embed)

client.run(os.getenv('TOKEN'))