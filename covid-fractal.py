#!/usr/bin/env python3

# COVID-19 Fractal
# by Felix An
# with live data from the COVID19Py module

import turtle
import random
try:
    import COVID19Py # used to get the data for the coronavirus counter
    covid19api = COVID19Py.COVID19()  # make a new instance of the API wrapper
    COVID19PyImportSuccess = True
except:
    COVID19PyImportSuccess = False


# make the turtle screen
turtleScreen = turtle.Screen()
turtleScreen.title("COVID-19 Fractal by Felix An")
turtleScreen.bgcolor(random.choice(["cyan", "skyblue", "dodgerblue", "cornflowerblue", "lightskyblue"]))

# loading screen text to see when the counts are being fetched over the Internet, the user might see this if they have crappy Internet
loadingText = turtle.Turtle(visible=False)
loadingText.speed(0)
loadingText.color("beige")
loadingText.write("Getting data...", font=("Arial", 60, "bold italic"), align='center')

# get the confirmed cases and the maximum generations of the virus growing, which is based on the real case count
if COVID19PyImportSuccess:
    confirmedCases = covid19api.getLatest()['confirmed']
    totalGenerations = confirmedCases // 100000 # this limits the number of times it splits off
else:
    confirmedCases = None
    totalGenerations = random.randint(30, 60)

# create the covidVirus class so each virus can decide what to do on its own
class covidVirus:
    # every time we create an instance of the covidVirus object all this stuff runs
    def __init__(self, generation, xPos, yPos):
        children = []
        global totalGenerations

        # limits the number of generations
        # it will stop reproducing of it exceeds the limit
        if generation > totalGenerations:
            return
        self.generation = generation
        self.xPos = xPos
        self.yPos = yPos
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
            self.virusTurtle.fillcolor(random.choice(["antiquewhite", "beige", "bisque", "blanchedalmond", "burlywood", "cornsilk", "ivory", "linen"]))
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
                self.virusTurtle.circle(size / random.randint(11, 14))
                self.virusTurtle.end_fill()
                self.virusTurtle.goto(self.xPos, self.yPos)
            
            # draw the outer ring of crowns
            for crownAngle in range(0, 360, 30):
                self.virusTurtle.seth(crownAngle)
                self.virusTurtle.fd(random.uniform(size - size / 19, size + size / 19))
                self.virusTurtle.begin_fill()
                self.virusTurtle.circle(size / random.randint(6, 10))
                self.virusTurtle.end_fill()
                self.virusTurtle.goto(self.xPos, self.yPos)
            
            # spawn the children
            for childrenAngle in range(-90, 270, 120):
                self.virusTurtle.seth(childrenAngle)
                self.virusTurtle
        
        # draw the virus based on the current generation
        # the later generation viruses are drawn smaller
        drawVirus(100 / generation)

# this is a test - remove this
if COVID19PyImportSuccess:
    print(covid19api.getLatest())

# remove the loading text
loadingText.reset()
loadingText.ht()

# fire off the chain with patientZero
patientZero = covidVirus(1, 0, 0)

turtle.done()
 