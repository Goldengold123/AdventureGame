import discord
import random

from discord.ext import commands
from dotenv import load_dotenv
from credentials import TOKEN

load_dotenv()

bot = commands.Bot('p!')


# Verifying the bot has connected to Discord

@bot.event
async def on_ready():
    print(f'{bot.user.name} is connected to Discord.')


# Stuff


intro = """
:sparkles: Welcome to this RPG  Game! :sparkles: 
=========================
Objective: Get to the roof after defeating the monster :smiling_imp:!
------------------------------------------------------------------
Commands (invalid commands will be ignored!):
- go [direction]
- get [item]
- use [utility]
- view map
- kill [creature]
"""


def makeStatus(myEnergy, myRooms, myCurrentRoom, myInventory):
    myStatus = '=====================' + '\n' + '**__STATUS:__**' + '\n' + ('Energy: ' + str(myEnergy)) + '\n' + (
            'You are in the ' + myCurrentRoom) + '\n' + ('Inventory: ' + str(myInventory)) + '\n'
    # prints items
    if 'item' in myRooms[myCurrentRoom]:
        myStatus += ('You see a ' + myRooms[myCurrentRoom]['item'])
        myStatus += '\n'
    # prints creatures
    if 'creature' in myRooms[myCurrentRoom]:
        myStatus += ('You see a ' + myRooms[myCurrentRoom]['creature'])
        myStatus += '\n'
    # prints map
    if 'map' in myRooms[myCurrentRoom]:
        myStatus += ('You see a ' + myRooms[myCurrentRoom]['map'])
        myStatus += '\n'
    # prints food
    if 'food' in myRooms[myCurrentRoom]:
        myStatus += ('You see a ' + myRooms[myCurrentRoom]['food'])
        myStatus += '\n'
    # prints utility
    if 'utility' in myRooms[myCurrentRoom]:
        myStatus += ('You see a ' + myRooms[myCurrentRoom]['utility'])
        myStatus += '\n'
    myStatus += '====================='
    myStatus += '\n'
    myStatus += 'Please enter your next move:'
    return myStatus


rooms = {
    'Downstairs Hall': {
        'south': 'Living Room',
        'east': 'Dining Room',
        'up': 'Elevator',
        'map': 'map'
    },
    'Dining Room': {
        'west': 'Downstairs Hall',
        'south': 'Garden',
        'east': 'Kitchen',
    },
    'Kitchen': {
        'west': 'Dining Room',
        'south': 'Garden',
        'utility': 'cake'
    },
    'Living Room': {
        'north': 'Downstairs Hall',
        'north': 'Downstairs Hall',
        'east': 'Garden',
        'creature': 'monster'
    },
    'Garden': {
        'west': 'Living Room',
        'north': 'Dining Room' or 'Kitchen',
        'item': 'key',
    },
    'Elevator': {
        'up': 'Upstairs Hall',
        'down': 'Downstairs Hall'
    },
    'Upstairs Hall': {
        'down': 'Elevator',
        'south': 'Red Bedroom' or 'Green Bedroom' or 'Blue Bedroom',
    },
    'Red Bedroom': {
        'north': 'Upstairs Hall',
        'east': 'Green Bedroom',
        'utility': 'candy'
    },
    'Green Bedroom': {
        'north': 'Upstairs Hall',
        'west': 'Red Bedroom',
        'east': 'Blue Bedroom',
        'utility': 'bed'
    },
    'Blue Bedroom': {
        'north': 'Upstairs Hall',
        'west': 'Green Bedroom',
        'up': 'Roof',
        'item': 'sword'
    },
    'Roof': {
        'down': 'Blue Bedroom'
    }
}


def check(message):
    return True


# Adventure Game
@bot.command(name='game', help='adventure game')
async def game(ctx):
    await ctx.send(intro)
    alive = True
    energy = random.randint(10, 15)
    currentRoom = 'Downstairs Hall'
    inventory = []
    while alive:
        await ctx.send(makeStatus(energy, rooms, currentRoom, inventory))
        moveMessage = await bot.wait_for('message', check=check)
        move = moveMessage.content.lower().split(' ')
        energy -= 1
        # go
        if move[0] == 'go':
            if move[1] in rooms[currentRoom]:
                if move[1] == 'Roof':
                    if not('key' in inventory and 'monster head' in inventory):
                        await ctx.send('You need to have defeat the monster and have a key in order to win. Go down the stairs to continue your journey...')
                currentRoom = rooms[currentRoom][move[1]]
            else:
                await ctx.send('There is no path that direction!')
        # get
        if move[0] == 'get':
            if ('item' in rooms[currentRoom]) and (move[1] in rooms[currentRoom]['item']):
                inventory.append(move[1])
                await ctx.send(move[1] + ' put into inventory!')
                del rooms[currentRoom]['item']
            else:
                await ctx.send(move[1] + ' is not here!')
        # view
        if move[0] == 'view':
            if 'map' in rooms[currentRoom] and move[1] in rooms[currentRoom]['map']:
                printMap = 'Viewing ' + move[1]
                printMap += '''
┌┤Elevator├-┬────────┬────────┐    ┌┤Elevator├┬──────┬─────┐
│  Downstairs │Dining Room │                          │    │                      │                    │               │               N
│        Hall        ╪                         ╪      Kitchen      │    │                      Upstairs Hall                 │      W ─┼─ E
├──╫────┼───╫────┴───╫────┤     ├──╫────┼───╫──┼──╫──┤               S
│      Living      │                                                      │     │       Red         │      Blue     │    Green  │   ┌─────┐
│      Room      ╪      Garden                                  │     │  Bedroom    │  Bedroom│ Bedroom│   │    Roof    │
└───────┴─────────────────┘     └───────┴──────┴┤Stairs├┘   └┤Stairs├┘
                                Ground Level                                                         Upper Level                                Roof Level'''
                await ctx.send(printMap)
            else:
                await ctx.send(move[1] + ' is not here!')
        # use
        if move[0] == 'use':
            if 'utility' in rooms[currentRoom] and move[1] in rooms[currentRoom]['utility']:
                energy += random.randint(2, 5)
                await ctx.send(move[1] + ' used.')
                del rooms[currentRoom]['utility']
            else:
                await ctx.send(move[1] + ' is not here!')
        # kill
        if move[0] == 'kill':
            if 'creature' in rooms[currentRoom] and move[1] in rooms[currentRoom]['creature']:
                if 'sword' in inventory:
                    print(move[1] + ' killed!')
                    inventory.remove('sword')
                    inventory.append([move[1]] + ' head')
                    del rooms[currentRoom]['creature']
                else:
                    await ctx.send('You need a weapon to kill a creature. The creature has killed you...GAME OVER!')
                    alive = False
            else:
                await ctx.send(move[1] + ' is not here!')
        # check for win
        if currentRoom == 'Roof':
            if 'key' in inventory and 'monster head' in inventory:
                await ctx.send('You gathered all the required items and defeated the monster, CONGRADUATIONS YOU WIN!')
                alive = False
            else:
                await ctx.send('You have not gathered all the required items/defeated the monster. Go down the stairs to continue your journey...')
        if energy < 1:
            await ctx.send('You ran out of energy...GAME OVER! say p!game in the chat to play again.')
            alive = False


bot.run(TOKEN)
