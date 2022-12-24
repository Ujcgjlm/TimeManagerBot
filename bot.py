from statistic import Statistic
from telebot.async_telebot import AsyncTeleBot
import asyncio
import tools
from collections import defaultdict
from threading import Timer


bot = AsyncTeleBot(tools.TOKEN, parse_mode=None)

# dict [userId][statName] = statObj
userData = defaultdict(dict)

async def UpdateHoursStat(userId, statName, minutes, backId):
    global userData
    userData[userId][statName].IncreaseStat(minutes)

    await bot.send_message(backId, text=statName + ' timer ended!')


@bot.message_handler(commands=['start'])
async def StartStatTimer(message):
    args = message.text.split()[1:]
    Timer(
        int(args[1]) * 60,
        UpdateHoursStat,
        [
            message.from_user.id,
            args[0],
            int(args[1]),
            message.chat.id
        ]
    ).start()
    await bot.send_message(message.chat.id, text='Timer started!')


@bot.message_handler(commands=['stat'])
async def GetStatistic(message):
    global userData
    statistic = '\n'.join(map(
        lambda tuple: str(tuple[0]) + " " + str(tuple[1]),
        userData[message.from_user.id].items()
    ))
    await bot.send_message(
        message.chat.id,
        text='You actual statistic:\n' + statistic
    )


@bot.message_handler(commands=['new'])
async def CreateNewStatistic(message):
    global userData
    args = message.text.split()[1:]

    if len(args) == 0:
        await bot.send_message(message.chat.id, text='I can\'t create empty stat')
        return

    userData[message.from_user.id][args[0]] = Statistic(hours=0)
    await bot.send_message(message.chat.id, text='Succesfully added!')


@bot.message_handler(commands=['del'])
async def CreateNewStatistic(message):
    global userData
    args = message.text.split()[1:]

    if len(args) == 0:
        await bot.send_message(message.chat.id, text='I can\'t delete empty stat')
        return

    if args[0] not in userData[message.from_user.id].keys():
        await bot.send_message(message.chat.id, text='I don\'t know this stat')
        return

    del userData[message.from_user.id][args[0]]
    await bot.send_message(message.chat.id, text='Succesfully deleted!')


@bot.message_handler(commands=['help'])
async def Help(message):
    await bot.send_message(message.chat.id, text=(
        "/help --- this message\n"
        "/new *name* --- create new *name* stat\n"
        "/del *name* --- delete new *name* stat\n"
        "/stat *name* --- get *name* stat\n"
        "/start *name* *minutes* --- start *name* stat timer for *minutes*"
    ))


if __name__ == "__main__":
    while True:
        asyncio.run(bot.polling())
