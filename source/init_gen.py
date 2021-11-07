import random
from bs4 import BeautifulSoup as soup
from urllib.request import Request, urlopen
import re

def get_spell(string, info=None):
    # Tags for info
    tags = {
    "level" : "ddb-statblock-item ddb-statblock-item-level",
    "castingtime" : "ddb-statblock-item ddb-statblock-item-casting-time",
    "range" : "ddb-statblock-item ddb-statblock-item-range-area",
#    "area" : "aoe-size",
    "components" : "ddb-statblock-item ddb-statblock-item-components",
    "duration" : "ddb-statblock-item ddb-statblock-item-duration",
    "school" : "ddb-statblock-item ddb-statblock-item-school",
    "savedc" : "ddb-statblock-item ddb-statblock-item-attack-save",
    "damagetype" : "ddb-statblock-item ddb-statblock-item-damage-effect",
    "description" : "more-info-content",
#    "classes" : "tag class-tag"
    }

    #save resulting url
    my_url = "https://www.dndbeyond.com/spells/"+string

    # open up page and download data in HTML File
    req = Request(my_url, headers={'User-Agent': 'Mozilla/5.0'})
    page_html = urlopen(req).read()

    # parse HTML
    page_soup = soup(page_html, "html.parser")

    # find tag of interest
    if info and info != "description":
        destination_tag = tags[info]
        bs_contents = page_soup.findAll("div", {"class":destination_tag})
    else:
        bs_contents = page_soup.findAll("div", {"class":tags["description"]})

    contents = "".join(list((map(lambda x: str(x), bs_contents))))
    TAG_RE = re.compile(r'<[^>]+>')
    result = TAG_RE.sub('', str(contents))
    return result

def add_initiative(args, arr):
    " " " appends global order_of_play-array by player name and player init " " "
    player_name = args.split(" ")[0]
    player_init = args.split(" ")[1]
    arr.append((player_name, int(player_init)))

def start_game(arr):
    " " " infinite generator function that yields string calling the person to start out" " "
    arr.sort(key=lambda x: x[1], reverse=True)
    while True:
        for current in arr:
            yield "Player number {}: {}, it's your turn.".format(arr.index(current) + 1, current[0])

def diceroll(string):
    " " " takes string-input 'x d y + z' and generates a random, cumulative result for dnd-dice rolls " " "
    # mögliche verbesserungsidee: Generatorausgabe
    full_array = string.split(" ")
    no_ws_string = "".join(full_array)
    no_ws_array = no_ws_string.split(
        "d")  # splits string into everything left to the 'd' and everything right to the 'd'
    if not no_ws_array[0]:  # nothing left to the d means there is only one dice
        factor = 1
    else:
        factor = int(no_ws_array[0])  # number of dice

    dice_and_modifier = "".join(no_ws_array[1:]).split("+")  # split right side to the d into dice-type and modifier
    if len(dice_and_modifier) <= 1:
        summand = 0  # modifier to the dice
    else:
        summand = sum(map(int, dice_and_modifier[1:]))
    dice = int(dice_and_modifier[0])  # dice-type, maximum number you can roll on a single throw

    res_array = []  # will contain the individual throws, will be factor-long

    if factor == 0 or dice == 0:
        res_array.append("0")  # you will get a 0 if you throw 0 dices or your dice is a 0...

    while factor >= 1 and dice >= 1:  # append res_array by individual dice throws
        res_array.append(str(random.randint(1, dice)))
        factor -= 1

    res = sum(map(int, res_array))  # produce sum of all dice throws
    if len(res_array) <= 1:
        res_string = "your roll: " + " + ".join(res_array) + " + " + str(summand) + " = " + str(res + summand)
    else:
        res_string = "your roll: (" + " + ".join(res_array) + ") + " + str(summand) + " = " + str(res + summand)

    if len(
            res_string) >= 1800:  # shortens the string on long computations, (discord has a limit of 2000 charactes per message)
        return res + summand
    else:
        return res_string

# print(diceroll("3d8 + 4"))
# print(diceroll("d20"))
# get_spell("moonbeam")