import time
import datetime
from math import floor
import discord
from discord.ext import commands
import calendar
import random

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='$', intents=intents)

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
#
# fdate and dateInput are for future dates. technically the capability is there to also
# calculate dates in the past

def getDate(formt, fdate, dateInput, dumbdumbmode):
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
    
    yearLength = 31449600
    secondsLength = 86400
    yearCurrent = 1341
    dayTemp = 0
    finishD = ""
    finishW = ""
    finishM = ""
    
    # this day corresponds to a day 300 years in avalore's past (1/1/1341)
    knownDate = datetime.datetime(1726, 4, 5)
    
    # a simple check and calculation that does two things:
    # 
    # 1) are we calculating a future date? and if so, 
    #
    # 2) we get the unix timestamp and use that as the date for our calculations
    # rather than the current time. due to this running at UTC -5, we subtract 2 hours
    # for a proper line up with UTC -7.

    if (fdate == True):
        dateM = datetime.datetime.strptime(dateInput, "%d/%m/%Y")
        dayTemp = dateM - knownDate
        realDate = int(((dayTemp.days) * secondsLength))
    else:
        dayTemp = datetime.datetime.now() - knownDate
        dateM = datetime.datetime.now()
        realDate = int((dayTemp.days) * secondsLength)


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
        "Snowmelt",
        "Firstide",
        "Greenrain",
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
        ]

    ###gross icky math###
    # i hate math honest
    
    # first we get the current unix timestap and just make sure it's an integer
    
    x = datetime.datetime.now()
    if (0 <=  int(x.hour) < 2   ) & fdate == False:
        currentDate = realDate - secondsLength
    else:
        currentDate = realDate

    # these get the day and month as the closest, lowest integer. we want the lowest as
    # just rounding to the nearest whole would, effectively, causee a month change 14
    # days too early, as it would round up to the next integer. we don't want that.
    # we also set the current year by adding how many years have passed since the 
    # reference year
    day = floor(currentDate/86400)
    month = floor(currentDate/2419200)
    yearCurrent += floor(currentDate/yearLength)
    
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
    day += 1

    # these all handle the day/month/year endings. yknow, 1st, 2nd, 3rd, 4th...
    # since after 4 they are all the same, "th", we just really need to worry about
    # 1, 2, 3. otherwise, just stick with "th".
    #
    # is there a better way to do this? yes.
    # can i be bothered? no. im too lazy.
    # does it also look horrible? also yes.
    #
    # dumbdumbmode is just a joke mode that randomizes the endings of days
    # so instead of the 2nd, or 1st, you get the twond or the fourd
    # or the twelvst. you get the jist.
    # it just randomly pulls from a list. thats it, without it ever being
    # correct. dumbasss.
    if(dumbdumbmode == False):
        ending = "st", "nd", "rd", "th"
        if (day == 1 or day == 21):
            finishD = ending[0]
        elif (day == 2 or day == 22):
            finishD = ending[1]
        elif (day == 3 or day == 23):
            finishD = ending[2]
        else:
            finishD = ending[3]
            
        if (week == 0):
            finishW = ending[0]
        elif (week == 1):
            finishW = ending[1]
        elif (week == 2):
            finishW = ending[2]
        else:
            finishW = ending[3]
        
        if (monthName == 0):
            finishM = ending[0]
        elif (monthName == 1):
            finishM = ending[1]
        elif (monthName == 2):
            finishM = ending[2]
        else:
            finishM = ending[3]
    else:
        firstED = "nd", "rd", "th"
        secondED = "st", "rd", "th"
        thirdED = "st", "nd", "th"
        otherED = "st", "nd", "rd"
        if (day == 1 or day == 21):
            finishD = random.choice(firstED)
        elif (day == 2 or day == 22):
            finishD = random.choice(secondED)
        elif (day == 3 or day == 23):
            finishD = random.choice(thirdED)
        else:
            finishD = random.choice(otherED)
            
        if (week == 0):
            finishW = random.choice(firstED)
        elif (week == 1):
            finishW = random.choice(secondED)
        elif (week == 2):
            finishW = random.choice(thirdED)
        else:
            finishW = random.choice(otherED)
        
        if (monthName == 0):
            finishM = random.choice(firstED)
        elif (monthName == 1):
            finishM = random.choice(secondED)
        elif (monthName == 2):
            finishM = random.choice(thirdED)
        else:
            finishM = random.choice(otherED)

    # finally, we return the output. depending on the toggle, there's two outputs as
    # described in the description of the overall function
    if (fdate == False):
        if formt == False:
            return ("It is the " + str(monthName+1) + finishM 
            + " month of the common year " + str(yearCurrent) + " A.C. It is " 
            + str(dayNames[dayName]) + ".\nIt is the " + str(day) + finishD 
            + ", in the " + str(week + 1) + finishW + " week of " 
            + str(monthNames[monthName]) + ".")
        elif formt == True:
            return ("Current date: " + str(day) + "/" + str(monthName+1).rjust(2,"0") 
            + "/" + str(yearCurrent))
    
    else:
        if formt == False:
            return ("Given " + str(dateInput) + ", that would be " 
                + str(dayNames[dayName]) + " the " + str(day) + finishD + " of "
                + str(monthNames[monthName]) + "\nIt would be the " +  str(week + 1) 
                + finishW + " week of the " + str(monthName+1) + finishM 
                + " month, A.C " + str(yearCurrent))
        elif formt == True:
            return ("Given date: " + str(dateInput) + "\nWill become: "
            + str(day) + "/" + str(monthName+1).rjust(2, "0") + "/" 
            + str(yearCurrent))

### discord integration ###
client = discord.Client(intents=intents)

# this is a readout to console to confirm what we're logged in as

@bot.event
async def on_ready():
    print("Logged in as: \n"
    + bot.user.name + "\n"
    + str(bot.user.id))

### Commands ####
# the following are all command declarations

# this is the default command. it gets the current day and spits out what it would be IC
# there are two possible flags: -f and -dumb
# -f formats the output to a dd/mm/yyy format, no fluff
# -dumb enables dumbdumbmode. see above for dumbdumbmode.
# it also checks to see if we're taking in an IRL date

@bot.command()
async def date(ctx, *form):
    if len(form) == 0:
        await ctx.send (getDate(False, False, 0, False))
    elif form[0] == "-dumb":
        await ctx.send(getDate(False, False, 0, True))
    elif form[0] == "-f":
        await ctx.send(getDate(True, False, 0, False))
    elif form [0] != "-f":
        dateNew = form[0].split("/")
        try:
            dateC = datetime.datetime(year=int(dateNew[2]),month=int(dateNew[1]),day=int(dateNew[0]))
            if len(form) == 1:
                await ctx.send (getDate(False, True, form[0], False))
            elif form[1] == "-f":
                await ctx.send (getDate(True, True, form[0], False))
            elif form[1] == "-dumb":
                await ctx.send (getDate(False, True, form[0], True))
        except ValueError:
            await ctx.send("Incorrect date format/Incorrect value entered\n" +
            "Correct Format: dd/mm/yyyy")
        
# this is the future command. provided a correct, and valid, day, it spits out what day
# it will become IC

'''@bot.command()
async def future(ctx, date, *form):
    dateNew = date.split("/")
    try:
        dateC = datetime.datetime(year=int(dateNew[2]),month=int(dateNew[1]),day=int(dateNew[0]))
        if len(form) == 0:
            await ctx.send (getDate(False, True, date))
        else:
            await ctx.send (getDate(True, True, date))
    except ValueError:
        await ctx.send("Incorrect date format/Incorrect value entered\n" +
        "Correct Format: dd/mm/yyyy")'''
        
# this is a custom help command   

@bot.command()
async def helpme(ctx):
    await ctx.send("Usage: $date [dd/mm/yyyy] [-f]\n" +
        "Optional modifiers\n" +
        "```[dd/mm/yyyy}: enter real date to calculate equivalent Avaloran Date"
        +"\n[-f] toggle formatting to a concise dd/mm/yyyy output format```")

# token
bot.run('')