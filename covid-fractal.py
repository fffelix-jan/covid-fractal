#!/usr/bin/env python3

# COVID-19 Fractal
# Coyright (c) 2020 by Felix An
# with live data from the COVID19Py module

import turtle
import random
from time import ctime
import sys

try:
    import COVID19Py # the module used to get the data for the coronavirus counter, also needs the requests module, install with "pip install COVID19py requests"
    cantImport = False
except:
    cantImport = True

try:
    covid19api = COVID19Py.COVID19()  # make a new instance of the API wrapper
    cantGetData = False
except:
    cantGetData = True

# set the recursion limit to the maximum allowed (the highest possible value of an int variable in C) so we won't exceed the limit
sys.setrecursionlimit(2147483647)

# make the turtle screen
turtleScreen = turtle.Screen()
turtleScreen.title("COVID-19 Fractal by Felix An")
turtleScreen.setup(1440, 1024)
turtleScreen.bgcolor(random.choice(["cyan", "skyblue", "dodgerblue", "cornflowerblue", "lightskyblue"]))    # random colours for more fun

# turn off the delay and disable updating the screen to make it faster
turtle.delay(0)
turtle.tracer(0, 0)

# loading screen text to see when the counts are being fetched over the Internet, the user might see this if they have crappy Internet
loadingText = turtle.Turtle(visible=False)
loadingText.speed(0)
loadingText.color("beige")
loadingText.write("Getting data...", font=("Arial", 60, "bold italic"), align='center')

# get the confirmed cases and the maximum generations of the virus growing, which is based on the real case count
try:
    covid19data = covid19api.getLatest()
    confirmedCases = covid19data['confirmed']
    deaths = covid19data['deaths']
    totalGenerations = confirmedCases // 1000000 # this limits the number of times it splits off - for every one million cases, there is one extra generation of children in the fractal
    cantGetData = False
except:
    totalGenerations = random.randint(3, 7) # if we can't get the actual numbers, choose a random number of generations
    cantGetData = True

# define the covidVirus class so each virus is spawned as an object and can decide what to do on its own
class covidVirus:
    # every time we create an instance of the covidVirus object all this stuff runs on itself
    def __init__(self, generation, xPos, yPos, startAngle):
        children = []   # list to store the "children" virus objects, which we will create later
        global totalGenerations # the generation limit

        # limits the number of generations
        # it will stop reproducing of it exceeds the limit
        if generation > totalGenerations:
            return
        
        self.generation = generation
        self.xPos = xPos
        self.yPos = yPos
        self.startAngle = startAngle
        self.virusTurtle = turtle.Turtle(visible=False)
        self.virusTurtle.speed(0)

        # this function does the actual drawing of the virus
        def drawVirus(size):
            self.virusTurtle.up()
            self.virusTurtle.goto(self.xPos, self.yPos)

            # draw the main beige-ish circle that represents the virus
            self.virusTurtle.seth(270)
            self.virusTurtle.fd(size)
            self.virusTurtle.seth(0)
            self.virusTurtle.fillcolor(random.choice(["antiquewhite", "beige", "bisque", "blanchedalmond", "burlywood", "cornsilk", "ivory", "linen"])) # random colours that look beige-ish
            self.virusTurtle.begin_fill()
            self.virusTurtle.circle(size)
            self.virusTurtle.end_fill()

            # the "crowns" I'm talking about are actually called peplomers (but I didn't know that they were called)
            # draw the crown in the middle
            self.virusTurtle.goto(self.xPos, self.yPos)
            self.virusTurtle.seth(0)
            self.virusTurtle.fillcolor("red")
            self.virusTurtle.begin_fill()
            self.virusTurtle.circle(size / random.randint(11, 14))
            self.virusTurtle.end_fill()
            self.virusTurtle.goto(self.xPos, self.yPos)

            # draw the inner ring of crowns
            for crownAngle in range(0, 360, 45):
                self.virusTurtle.seth(crownAngle)
                self.virusTurtle.fd(random.uniform((size / 2) - size / 19, (size / 2) + size / 19))
                self.virusTurtle.begin_fill()
                self.virusTurtle.circle(size / random.randint(9, 12))
                self.virusTurtle.end_fill()
                self.virusTurtle.goto(self.xPos, self.yPos)
            
            # draw the outer ring of crowns
            for crownAngle in range(0, 360, 30):
                self.virusTurtle.seth(crownAngle)
                self.virusTurtle.fd(random.uniform(size - size / 19, size + size / 19))
                self.virusTurtle.begin_fill()
                self.virusTurtle.circle(size / random.randint(5, 9))
                self.virusTurtle.end_fill()
                self.virusTurtle.goto(self.xPos, self.yPos)
            
            
            # spawn the children in three directions, forming a triangle
            for childrenAngle in range(startAngle, startAngle - 360, -120):
                self.virusTurtle.seth(childrenAngle)
                self.virusTurtle.forward(200 / generation)
                children.append(covidVirus(generation + 1, self.virusTurtle.xcor(), self.virusTurtle.ycor(), childrenAngle))
                self.virusTurtle.goto(self.xPos, self.yPos)
            
        
        # draw the virus based on the current generation
        # the later generation viruses are drawn smaller
        # use this reciprocal function to calculate the size
        drawVirus(60 / generation)


# show some text while drawing
loadingText.reset()
loadingText.ht()
loadingText.color("beige")
loadingText.write("Drawing the fractal...", font=("Arial", 60, "bold italic"), align='center')

# fire off the chain of events by making a new instance of the covidVirus class - we'll call it patientZero
patientZero = covidVirus(1, 0, 0, 90)

# remove the loading text
loadingText.reset()
loadingText.ht()

# make the counters at the bottom of the screen
statsDisplay = turtle.Turtle(visible=False)
statsDisplay.speed(0)
statsDisplay.up()
statsDisplay.goto(0, -440)
statsString = ""

# generate the text at the bottom, put error messages if necessary
if not cantImport and not cantGetData:
    statsString += "COVID-19 confirmed cases: " + str(confirmedCases) + "\nDeaths: " + str(deaths) + "\n"
elif cantGetData:
    statsString += "Can't get COVID-19 data from API.\n"
elif cantImport:
    statsString += "Can't import the COVID19Py module. It might not be installed.\n"
else:
    statsString += "Unknown error when getting COVID-19 data.\n"

statsString += "#stayhome and stay safe!"

# write the text
statsDisplay.color("beige")
statsDisplay.write(statsString, font=("Arial", 50, "bold"), align='center')

# write the current time
statsDisplay.goto(0, -480)
statsDisplay.write("Fractal generated " + ctime(), font=("Arial", 24, "bold"), align='center')


turtle.done()
 
