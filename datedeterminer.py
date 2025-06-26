import time
from math import floor
import discord

###these are needed to make the bot work ###
# i ~believe~ these listen to messages to see if thee bot has been called on
intents = discord.Intents.default()
intents.message_content = True

### date finding function ###
# as we dont want the bot to be constantly doing work, we only call this function when
# the bot finds the keyword mentioned.
#
# the toggle variable determines whether we print out the format in dd/mm/yyyy
# or as a small snippet of ~whimsey~
def getDate(toggle):
    ###this function is dedicated to getting the right date name###
    #
    # what it's doing can be broken down into 3 main poritons 
    #
    # 1) setting the days to be between 0 and 6. this is done as week day names repeat
    #    every 7 days. doing this avoids unnessecary repetition
    #
    # 2) we set the output to 0. as this interacts with an array, we are using output to 
    #    reference an index.
    #
    # 3) once those are complete, we cycle through the range of 1-7, picking the
    #    appropriate, largest number that the input day is divisible by in whole
    #
    # once all those are complete, we set the output appropriately and return it

    def getDayName(dayin):
        y = floor(dayin/7)
        dayin = dayin - (7 * y)
        out = 0
        if dayin > 0:
            for x in range(1,7):
                if dayin % x == 0:
                    out = x
            return out
        else:
            return out


    ###this function is dedicated to getting the right month name###
    #
    # this operates almost identically to the prior function, only for working with 13 
    # options instead of 7

    def getMonthName(monthin):
        y = floor(monthin/13)
        monthin = monthin - (13 * y)
        out = 0
        if monthin > 0:
            for x in range(1,13):
                if monthin % x == 0:
                    out = x
            return out
        else:
            return out

    ### this is variable decleration ###
    # have a known date of Highsun 5, 1641 (05/04/1641 dd/mm/yy) that corresponds to 
    # 25/06/2025, first day of highsun therefore would be 20/06/2025
    # using that as a reference point for future calculations (as unix timestamp)
    # 
    # 364 days a year, 86400 seconds/day, 31449600 seconds/year IC.
    knownDate = 1750478400
    realDate = int(time.time())
    firstYearEnd = 24191999
    yearLength = 31449600
    yearCurrent = 1641
    finishD = ""
    finishW = ""
    finishM = ""

    ### arrays ###
    # as we will (in theory) use these over and over, the day/month names and month 
    # number are stored as arrays.
    dayNames = [
        "Sunday",
        "Wakeday",
        "Restday",
        "Cartday",
        "Blessday",
        "Washday",
        "Ashday",   
        ]
    
    # due to using the 4th month of the year as the 0 point, it is needed to track
    # the month number as an array as well.
    #
    # Could this have been donee better? yes. do i care? no. will i changee it? 
    # fuck no
    # it would require finding the first month's real date, and using that. 
    # also reworking a bunch of stuff and im, frankly, not paid
    monthNames = [
        "Highsun",
        "Bloomburrow",
        "Lowsun",
        "Falltide",
        "Goldleaf",
        "Harrowing",
        "Skybright",
        "Frostfall",
        "Darkmoon",
        "Reflection",
        "Snowmelt", ##this is the first month in the year
        "Firstide",
        "Greenrain",
        ]

    monthNumber = [
        "4",
        "5",
        "6",
        "7",
        "8",
        "9",
        "10",
        "11",
        "12",
        "13",
        "1",
        "2",
        "3",
        ]

    ###gross icky math###
    # i hate math honest
    
    # first we get the current unix timestap and just make sure it's an integer
    currentDate = int(realDate - knownDate)

    # this calculates if we should add a year onto the current known year, effectively
    # tracking what the current year is. duee to using the 4th month of the year as the
    # 0 point, we have to first initially find if that year has ended. then we can track
    # years semi-normally. we just subtract the seconds from the first year, but add 1
    # to compensate for it being past 1642.
    if  yearLength > currentDate > firstYearEnd:
       yearCurrent = yearCurrent + 1
    elif currentDate > (firstYearEnd + yearLength):
        yearCurrent = yearCurrent + floor((currentDate-firstYearEnd)/yearLength) + 1

    # these get the day and month as the closest, lowest integer. we want the lowest as
    # just rounding to the nearest whole would, effectively, causee a month change 14
    # days too early, as it would round up to the next integer. we don't want that.
    day = floor(currentDate/86400)
    month = floor(currentDate/2419200)

    # these both reset the day if we're over the 28 days in a month, as well as tracking
    # the current week. since the days get reset after every 28, we dont need to worry
    # about the weeks going over 4 at any point, it will simply loop back to week 1 once
    # the day reset has occured.
    if day >= 28: 
        day = day - (28 * floor(day/28))
    if day >= 7:
        week = floor(day/7)
    else: 
        week = 0

    # calling the functions above to get the day and month names.
    dayName = getDayName(day)
    monthName = getMonthName(month)

    # because the day is calculated to a range from 0-27, to avoid a "0th" day, we simply
    # add one to the day counter for the rest of the process.
    day = day + 1

    # these all handle the day/month/year endings. yknow, 1st, 2nd, 3rd, 4th...
    # since after 4 they are all the same, "th", we just really need to worry about
    # 1, 2, 3. otherwise, just stick with "th".
    #
    # is there a better way to do this? yes.
    # can i be bothered? no. im too lazy.
    # does it also look horrible? also yes.
    if (day == 1):
        finishD = "st"
    elif (day == 2):
        finishD = "nd"
    elif (day == 3):
        finishD = "rd"
    else:
        finishD = "th"
        
    if (week == 0):
        finishW = "st"
    elif (week == 1):
        finishW = "nd"
    elif (week == 2):
        finishW = "rd"
    else:
        finishW = "th"
    
    if (month == 10):
        finishM = "st"
    elif (month == 11):
        finishM = "nd"
    elif (month == 12):
        finishM = "rd"
    else:
        finishM = "th"

    # finally, we return the output. depending on the toggle, there's two outputs as
    # described in the description of the overall function
    if toggle == False:
        return ("It is the " + str(monthNumber[monthName]) + finishM + " month of the " +
            "common year " + str(yearCurrent) + " A.C. It is " + str(dayNames[dayName]) + 
            ".\nIt is the " + str(day) + finishD + ", in the " + str(week + 1) + 
            finishW + " week of " + str(monthNames[monthName]) + ".")
    elif toggle == True:
        return ("Current date: " + str(day) + "/" + str(monthNumber[monthName]) + "/" 
        + str(yearCurrent))

### discord integration ###
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$date -dmy'):
        await message.channel.send(getDate(True))
    elif message.content.startswith('$date'):
        await message.channel.send(getDate(False))

client.run('token would go here, but it is hidden for safety :D')