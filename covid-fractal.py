#!/usr/bin/env python3

# COVID-19 Fractal
# by Felix An
# with live data from the COVID19Py module

from tkinter import messagebox  # for error boxes and the like
import turtle
try:
    import COVID19dddPy # used to get the data for the coronavirus counter
    covid19data = COVID19Py.COVID19()  # make a new instance of the COVID
    COVID19PyImportSuccess = True
except:
    COVID19PyImportSuccess = False
    errWin 
    messagebox.showwarning("Failed to import COVID19Py", "The COVID19Py module could not be imported. If not installed, you can install it by running the command 'pip install COVID19Py'. The fractal will run anyway, but it will be random, not based on live COVID-19 data.")
    
    from random import randint

# create the covidVirus class so each virus can decide what to do on its own
class covidVirus:
    global totalGenerations
    def __init__(self, generation, xPos, yPos):
        self.generation = generation
        self.xPos = xPos
        self.yPos = yPos
        self.virusTurtle = turtle.Turtle()

        def drawVirus(size):
            self.virusTurtle.up()
            self.virusTurtle.seth(270)
            self.virusTurtle.fd(size)
            #self.
            self.virusTurtle.circle(size)
        
        
        drawVirus(50)
        # self.virusTurtle.speed(0)

        #children = [covidVirus(self.generation + 1, self.xPos, self.yPos + )]

# make the turtle screen
turtleScreen = turtle.Screen()
turtleScreen.title("COVID-19 Fractal by Felix An")
turtleScreen.bgcolor("cyan")

# loading screen text to see when the counts are being fetched over the Internet, the user might see this if they have crappy Internet
loadingText = turtle.Turtle()
loadingText.ht()
loadingText.color("beige")
loadingText.write("Getting data...", font=("Arial", 50, "bold italic"), align='center')

# get the confirmed cases and the maximum generations of the virus growing, which is based on the real case count
if COVID19PyImportSuccess:
    confirmedCases = covid19data.getLatest()['confirmed']
    totalGenerations = confirmedCases // 100000
else:
    confirmedCases = None


# remove the loading text
loadingText.reset()


patientZero = covidVirus(0, 0, 0)
turtle.done()
