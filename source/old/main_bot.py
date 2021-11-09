import discord
import init_gen

client = discord.Client()
order_of_play = [] # we need this later
generator = init_gen.start_game(order_of_play)

@client.event
async def on_ready():
    " " " this reassures me that my bot is okay " " "
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    " " " main " " "
    try:
        if message.author == client.user:
            " " " ensures that bot does not react to itself " " "
            return

        if message.content.startswith('spell '):
            " " " cuts off keyword and calls get_spell with resulting string " " "
            content_string = message.content[6:].lower()
            content_array = content_string.split(", ")
            content_array[0] = content_array[0].replace(" ", "-")
            if len(content_array) <= 1: # call init_gen.get_spell with spell name, without another argument
                await message.channel.send(init_gen.get_spell(content_array[0]))
            else: # message contains more than one argument, call get_spell() with extra argument
                await message.channel.send(init_gen.get_spell(content_array[0], content_array[1]))

        if message.content.startswith('roll '):
            " " " cuts off keyword and calls init_gen.diceroll with resulting string " " "
            msg_rest = message.content.lower().split(" ")
            if any([x.isnumeric() for x in message.content[5:].lower()]): # checks for x d y + z syntax containing nums
                content_string = message.content[5:].lower()
                await message.channel.send(init_gen.diceroll(content_string))
            elif len(msg_rest) > 1 and msg_rest[1] != "fireball": # checks for spells in my spell list for snowdrop
                damage_die = {"moonbeam":"2d10",
                                "shillelagh":"1d8+3",
                                "healingword":"1d4+3",
                                "heatmetal":"2d8",
                                "init":"1d20+3"}
                await message.channel.send(init_gen.diceroll(damage_die[msg_rest[1]]))
            elif len(msg_rest) > 1 and msg_rest[1] == "fireball":
                " " " computes the amount of d6 needed for a higher than level 3 fireball" " "
                DEFAULT_LVL = 3
                difference = 0
                content_array = list(filter(lambda letter: letter.isnumeric(),
                                            list(message.content)))  # filter numbers out of the message
                new_level = sum(map(lambda x: int(x), content_array))  # sum all numbers and declare them new_level
                if new_level >= 3:
                    difference = abs(DEFAULT_LVL - new_level)
                new_factor = str(8 + difference)
                await message.channel.send(init_gen.diceroll(new_factor + "d6"))

        if message.content.startswith('start combat') or message.content.startswith('next'):
            " " " after collecting init values this call will return the next in line to attack " " "
            await message.channel.send(generator.__next__())

        if message.content.startswith('init '):
            " " " syntax: init name value; with init you add a players name and their initiative to a global dict " " "
            args = message.content[5:]
            init_gen.add_initiative(args, order_of_play)
    except Exception as exc:
        " " " catches exception and ensures that program will continue after a mippety mistake " " "
        print(exc) # prints exception on your console
        await message.channel.send("Oops, Error") # chat will receive this message
        return None

client.run("Njk4MTY0NDIwNTEzMzY2MDU2.XpB2cw.AU1OGyYZusZa-4ZqKY6gui9rpDc")