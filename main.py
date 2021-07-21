#Allen Mathew
#ICS31
#Mr. Greco
#January 17, 2020
#This is a clicker game where the player has to click as many games as they 
#can before the timer runs out. The player also has to watch out for the red death dot or they will die.

#------------------------------------------------------------------------
#Libraries
#------------------------------------------------------------------------
import pygame, sys, time
from pygame.locals import *
from pygame.constants import *
import random
import math
import re

pygame.font.init()

#------------------------------------------------------------------------
#Variables
#------------------------------------------------------------------------
programName = "C l i c k r"
screenDimensions = (800, 575)
fpsClock = pygame.time.Clock() #FPS means "Frames per second".
fpsLock = 60

username = ""

totalClicks = 0
hits = 0
hit2 = 0
totalHits = 0

totalAccuracy = 0

countdown = 3
seconds1 = 0

tries = 1

time = 30
seconds2 = 0

hitMarker = pygame.image.load("hitmarker.png")

hitMarker = pygame.transform.scale(hitMarker, (25, 25))

markerSize = hitMarker.get_rect().size

markerX = 0
markerY = 0

leftClick = False

font = pygame.font.SysFont("comicsans", 30)

deathX = 0
deathY = 0

speedDeath = 3

velX = 0
velY = 0

radius = 10

players = 0

play = 0
#------------------------------------------------------------------------
#Initialization
#------------------------------------------------------------------------
pygame.init()
screen = pygame.display.set_mode(screenDimensions)
pygame.display.set_caption(programName)

pygame.mixer.init()

#Playing music
pygame.mixer.music.load("music.mp3")
pygame.mixer.music.play(-1,0.0)

#Setting the cursor invisible
pygame.mouse.set_visible(0)

#Making sure that no objects are on the screen
circle = None
particles = []

#Classifying a Circle as an object
class Circle():
    #Initializing variables
    def __init__(self, x, y, r, color):
        self.x = x
        self.y = y
        self.r = r
        self.color = color
        self.alive = True
    
    #Defining a function to see if the point where the mouse clicked is in the circle
    def pointTouches(self, x, y):
        if(math.sqrt((x - self.x)**2 +(y - self.y)**2) <= self.r):
            return True
        
        #Returning False if it is a miss
        return False

    #Defining a function for drawing one circle at a time
    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), int(self.r))


#Classifying Particles as an object
class Particle():
    #Initializing variables
    def __init__(self, pos, vel):
        self.pos = pos
        self.vel = vel
        
        #Setting each particle's lifetime to 50 frames
        self.lifetime = 50
        
    #Defining a function for updating the particles. (Velocity and movement)
    def update(self):
        self.lifetime -= 1
        
        self.vel = [self.vel[0] * 0.998, self.vel[1] * 0.998]
        
        self.pos = [self.pos[0] + self.vel[0], self.pos[1] + self.vel[1]]
    
    #Defining a function to draw the particles
    def draw(self, scr):
        pygame.draw.circle(scr, (255, 128, 0), (int(self.pos[0]), int(self.pos[1])), 3)

def redDeath():
    #Globalling all required variables
    global markerX
    global markerY
    global mousePosition
    global markerSize
    global lengthX
    global lengthY
    global deathX
    global deathY
    global radians
    global directionX
    global directionY
    global speedDeath
    
    #Setting variables for the position of the cursor
    markerX = mousePosition[0] - (markerSize[0]//2)
    markerY = mousePosition[1] - (markerSize[1]//2)
    
    #Finding the distance from the death circle to the hitmarker
    lengthX = mousePosition[0] - deathX
    lengthY = mousePosition[1] - deathY
    
    #Avoid "division by zero" runtime error.
    if lengthX == 0:
        lengthX = 0.001

    #Find angle between the mouse and circle using inverse tan.
    radians = math.atan(lengthY/lengthX)
    
    #Remove half-circle from angle.
    radians -= math.pi / 2

    #Determine direction using sin and cos.
    directionX = math.sin(radians)
    directionY = math.cos(radians)

    #Apply direction to the correct quadrant.
    if lengthX > 0:
        directionX *= -1
    else:
        directionY *= -1

    #Apply direction to circle on its x-axis and y-axis.
    deathX += directionX * speedDeath
    deathY += directionY * speedDeath
    
    
    #-------------------------------------
    #Particle Effects for the circle
    #-------------------------------------
    
    #Setting the velocity of the particles the opposite direction of the red death dot
    vel = [-directionX, -directionY]
    
    #Determining the speed of the dot
    currentSpeed = math.sqrt(vel[0] ** 2 + vel[1] ** 2)
    
    #making the length of the hypotnuse 1
    vel = [vel[0] / currentSpeed, vel[1] / currentSpeed]
    
    #Setting the maximum angle of the particle spread to 50
    particleSpread = 50
    
    #Making a random angle of which the particle will appear
    rotTheta = random.randint(0, 2 * particleSpread) - particleSpread
    
    x = vel[0]
    y = vel[1]
    
    #Rotation matrix
    #Rotates the direction of the particles so that it could appear in random places
    vel[0] = x * math.cos(math.radians(rotTheta)) - y * math.sin(math.radians(rotTheta))
    vel[1] = x * math.sin(math.radians(rotTheta)) + y * math.cos(math.radians(rotTheta))
    
    #Creating the particle
    particles.append(Particle([deathX, deathY], vel))
    

def gameOver():
    #Globalling all required variables
    global tries
    global time
    global seconds2
    global fpsLock
    global deathX
    global mousePosition
    global deathY
    global username
    global hits
    global clickAccuracy
    global radius
    global players
    global hit2
    global deathReason
    global particles
    global totalClicks
    global speedDeath
    global seconds2
    global totalHits
    global totalAccuracy
    global play
    
    #Checking if the time is up or if the circle collided with the hitmarker
    if time - (seconds2 // fpsLock) == 0 or math.sqrt(((deathX - mousePosition[0])**2) + ((deathY - mousePosition[1])**2)) < (radius * 2):
        
        #If there are 2 players, the circle gets a 5 points because it is hard to kill player 1
        if players == 2:
                hit2 += 5
        
        #Once the player dies, the games goes into a while true loop that asks them if they want to play again
        while True:                                
            for event in pygame.event.get():
                
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    
                if event.type == pygame.KEYDOWN:
                    
                    if event.key == pygame.K_n:
                        
                        #If there is only 1 player, the game stores the player's scores
                        if players == 1 and tries == 1:
                            f = open("scores.txt", "a")
                            f.write("\n" + str(username) + " - " + str(hits) + " points with an accuracy of " + str(clickAccuracy) + " %")
                            f.close()
                            
                        elif players == 1 and tries > 1:
                            f = open("scores.txt", "a")
                            f.write("\n" + str(username) + " - " + str(totalHits + hits) + " total points with an average accuracy of " + str((clickAccuracy + totalAccuracy) // tries) + " %")
                            f.close()
                        
                        sys.exit()
                    
                    #If the player presses Y, the game resets to play again
                    if event.key == pygame.K_y:
                        if players == 1:
                            
                            #Resetting all the variables for single player mode
                            time = 30
                            totalHits += hits
                            totalAccuracy += clickAccuracy
                            seconds2 = 0
                            totalClicks = 0
                            hits = 0
                            tries += 1
                            play += 1
                            deathX = 0
                            deathY = 0
                            speedDeath = 3
                            seconds2 = 0
                            particles = []

                        elif players == 2:
                            
                            #Resetting all the variables for multiplayer mode
                            play += 1
                            deathX = 0
                            deathY = 0
                            speedDeath = 3
                            seconds2 = 0
                    
            screen.fill(pygame.Color(255,255,255))
            
            #Finding out why the player died and displaying the appropriate message
            if time - (seconds2 // fpsLock) == 0:
                deathReason = font.render("TIMES UP!", 1, (0,0,0))
            
            elif math.sqrt(((deathX - mousePosition[0])**2) + ((deathY - mousePosition[1])**2)) < (radius * 2) and players == 1:
                deathReason = font.render("You died from the red man.", 1, (0,0,0))
            
            if players == 1:
                gameOver = font.render("Your final score is: " + str(hits) + " with " + str(clickAccuracy) + "% accuracy", 1, (0,0,0))
                playAgain = font.render("Do you want to play again? Press Y for yes and N for no", 1, (0,0,0))
            elif players == 2:
                gameOver = font.render("Player 2 killed Player 1", 1, (0,0,0))
                playAgain = font.render("Do you want to play again? Press Y for yes and N for no", 1, (0,0,0))
            
            #Blitting and updating the screen
            if players == 1:
                screen.blit(deathReason, (100, 200))
            screen.blit(gameOver, (100, 300))
            screen.blit(playAgain, (100, 350))
            
            pygame.display.update()
            fpsClock.tick(fpsLock)
            
            #If they choose to play again, they break out of this loop and back into the main game loop
            if play > 0:
                play = 0
                break

def hitOrMiss():
    global click
    global leftClick
    global circle
    global markerX
    global markerY
    global markerSize
    global totalClicks
    global hits
    global screen

    click = False
    
    #If the user clicks, the game makes the variable click become True
    if pygame.mouse.get_pressed()[0]:
        if not leftClick:
            leftClick = True
            click = True
    else:
        leftClick = False
    
    #If there are circles on the screen, the game checks where the user clicked and sees if it hit the circle or not
    if circle != None:
        if circle.pointTouches(markerX + (markerSize[0]//2), markerY + (markerSize[1]//2)) and click:
            circle = None
            totalClicks += 1
            hits += 1
        elif click:
            totalClicks += 1
    
    #This draws the circle onto the screen
    if circle != None:
        circle.draw(screen)


#Pygame main loop
while True:
    #---------------------------------------------------------------------
    #Events
    #---------------------------------------------------------------------
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            
            #If the player says that there is only 1 player, the game stores that and brings the player into the singleplayer game
            if event.key == pygame.K_1:
                players = 1
                
                while True:
                    #---------------------------------------------------------------------
                    #Events
                    #---------------------------------------------------------------------
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                            
                        elif event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_RETURN:
                                while True:
                                    #---------------------------------------------------------------------
                                    #Events
                                    #---------------------------------------------------------------------
                                    
                                    #Setting the new line variable to 0 so that it could properly display the past scores
                                    newLine = 0
                                    
                                    for event in pygame.event.get():
                                            if event.type == pygame.QUIT:
                                                pygame.quit()
                                                sys.exit()
                                                
                                            elif event.type == pygame.KEYDOWN:
                                                
                                                #Coding every letter and number on the keyboard to get added in the username
                                                if (event.unicode.isalpha() or event.unicode.isdigit() or (len(username) > 0 and event.key == pygame.K_SPACE)) and len(username) <= 9:
                                                    username += event.unicode
                                                
                                                #Coding the backspace so that the user can delete the last character from their username
                                                elif event.key == pygame.K_BACKSPACE:
                                                    username = username[:-1] 
                                                
                                                #Once the player presses the enter key, the game counts down from 3 to tell the player that the game is starting
                                                elif event.key == pygame.K_RETURN:
                                                    for i in range(180):
                                                        screen.fill(pygame.Color(0,0,0))
                                                    
                                                        timer = font.render("Ready? " + str((countdown - (seconds1 // fpsLock))), 1, (255,255,255))
                                                        
                                                        screen.blit(timer, (350, 300))
                                                        
                                                        pygame.display.update()
                                                        fpsClock.tick(fpsLock)
                                                        
                                                        seconds1 += 1
                                                    
                                                    #Main game loop for single player
                                                    while True:
                                                        
                                                        #---------------------------------------------------------------------
                                                        #Events
                                                        #---------------------------------------------------------------------
                                                        for event in pygame.event.get():
                                                            
                                                            #The player can click the close window key or the escape key to quit the game
                                                            if event.type == pygame.QUIT:
                                                                pygame.quit()
                                                                sys.exit()
                                                                
                                                            elif event.type == pygame.KEYDOWN:
                                                                if event.key == pygame.K_ESCAPE:
                                                                    sys.exit()
                                                        #---------------------------------------------------------------------
                                                        #Runtime
                                                        #---------------------------------------------------------------------
                                                        screen.fill(pygame.Color(0,0,0))
                                                        
                                                        #Recalling the circle class so that it will pop up at random points, sizes, and colors
                                                        #This only happens if there are no circles currently on the screen
                                                        if circle == None:
                                                            circle = Circle(random.randint(20,800), random.randint(20, 575), random.randint(20,100), (random.randint(100,255), random.randint(100,255), random.randint(100,255)))
                                                        
                                                        #Creating a variable to get the position of the mouse
                                                        mousePosition = pygame.mouse.get_pos()
                                                        
                                                        for i in range(len(particles) -1, -1, -1):
                                                            particle = particles[i]
                                                            
                                                            particle.update()
                                                            
                                                            if particle.lifetime <= 0:
                                                                del(particles[i])
                                                        
                                                        #Recalling the red death circle so that it could follow the mouse
                                                        redDeath()
                                                        
                                                        #Recalling this function to check if the player hit the circle or not
                                                        hitOrMiss()
                                                        
                                                        #Setting the click accuracy to 0
                                                        clickAccuracy = 0
                                                        
                                                        #If the user clicked more than once, the program calculates the accuracy using the total clicks and total hits
                                                        if totalClicks != 0:
                                                            clickAccuracy = round(((hits/totalClicks)  * 100), 2)
                                                        
                                                        #Creating text to display the player's score, accuracy, and time left
                                                        textAccuracy = font.render("Accuracy: " + str(clickAccuracy) + " %", 1, (255,255,255))
                                                        score = font.render("Score: " + str(hits), 1, (255,255,255))
                                                        timer = font.render("Time: " + str((time - (seconds2 // fpsLock))), 1, (255,255,255))
                                                        
                                                        #Recalling the game over function to see if the player has died
                                                        gameOver()
                                                        
                                                        #Making the red dot go faster and faster
                                                        speedDeath += seconds2 * 0.000005
                                                        
                                                        #Blitting the text onto the screen
                                                        screen.blit(textAccuracy, (620, 10))
                                                        screen.blit(timer, (10, 10))
                                                        screen.blit(score, (350, 10))
                                                        screen.blit(hitMarker,(markerX,markerY))
                                                        
                                                        #Displaying the particles onto the screen
                                                        for particle in particles:
                                                            particle.draw(screen)
                                                        
                                                        #drawing the red death circle
                                                        pygame.draw.circle(screen, (255,0,0),(int(deathX),int(deathY)), 10)
                                                        #---------------------------------------------------------------------
                                                        #Screen Update
                                                        #---------------------------------------------------------------------
                                                        pygame.display.update()
                                                        fpsClock.tick(fpsLock)
                                                        
                                                        #Counting how much time has past
                                                        seconds2 += 1
                                    
                                    
                                    #---------------------------------------------------------------------
                                    #Runtime
                                    #---------------------------------------------------------------------
                                    screen.fill(pygame.Color(255,255,255))
                                    
                                    #Opening the text file that has all the past scores saved
                                    g = open("scores.txt", "r")
                                    s = g.read()
                                    
                                    #Splitting the long string into a list
                                    lines = s.split("\n")
                                    
                                    #Creating empty lists so I could list and sort the high scores
                                    scoresList = []
                                    usedIndeces = []
                                    sortedScores = []
                                    
                                    #Making a list with lists that contain the full sentence and their score
                                    for line in range(len(lines)):
                                        
                                        #Skipping the "Past Scores" part of the txt file
                                        if line == 0:
                                            continue
                                        
                                        text = lines[line]
                                        
                                        #Finding the score
                                        numScore = int(re.search("(\\-\\s)(\\d+)", text).group(2))
                                        
                                        #Appending the list into a list
                                        scoresList.append([text, numScore])
                                    
                                    #Looping for as much elements there are in the list
                                    for i in range(len(scoresList)):
                                        num = -1
                                        s = None
                                        index = 0
                                        
                                        #In order to sort the scores from greatest to lowest, I go through every index and see if the score is greater than the previous scores
                                        for j in range(len(scoresList)):

                                            if scoresList[j][1] > num:
                                                used = False
                                                
                                                #Checking if the index is already used
                                                for k in range(len(usedIndeces)):
                                                    if usedIndeces[k] == j:
                                                        used = True
                                                
                                                #Sorting the scores into the list
                                                if not used:
                                                    num = scoresList[j][1]
                                                    s = scoresList[j]
                                                    index = j
                                        
                                        #Appending the used indeces and the sorted scores into their own list
                                        sortedScores.append(s[0])
                                        usedIndeces.append(index)     
                                    
                                    #For every item in a list, the program displays the list of past scores onto the screen
                                    for i in sortedScores:
                                        
                                        leaderboard = font.render(i, 1, (0,0,0))
                                        
                                        screen.blit(leaderboard, (10, 35 + (newLine * 25)))
                                    
                                        newLine += 1
                                    
                                    g.close()
                                    
                                    usernameInstructions = font.render("Type in your username, only letters and numbers are allowed (max 10):", 1, (0,0,0))
                                    highScores = font.render(lines[0], 1, (0,0,0))
                                    user = font.render(username, 1, (0,0,0))
                                    
                                    screen.blit(highScores, (10, 10))
                                    screen.blit(usernameInstructions, (50, 450))
                                    screen.blit(user, (400 - (len(username) * 5.5), 500))
                                    #---------------------------------------------------------------------
                                    #Screen Update
                                    #---------------------------------------------------------------------
                                    pygame.display.update()
                                    fpsClock.tick(fpsLock)
                                
                            
                            elif event.key == pygame.K_t:
                                
                                while True:
                                    exit = 0
                                    
                                    #---------------------------------------------------------------------
                                    #Events
                                    #---------------------------------------------------------------------
                                    for event in pygame.event.get():
                                        
                                        #The player can click the close window key or the escape key to quit the game
                                        if event.type == pygame.QUIT:
                                            pygame.quit()
                                            sys.exit()
                                            
                                        elif event.type == pygame.KEYDOWN:
                                            if event.key == pygame.K_ESCAPE:
                                                sys.exit()
                                            
                                            #If the user presses the N key, it will allow them to break out of this loop and into the instructions screen loop
                                            elif event.key == pygame.K_n:
                                                exit += 1
                                    #---------------------------------------------------------------------
                                    #Runtime
                                    #---------------------------------------------------------------------
                                    screen.fill(pygame.Color(0,0,0))
                                    
                                    #Recalling the circle class so that it will pop up at random points, sizes, and colors
                                    #This only happens if there are no circles currently on the screen
                                    if circle == None:
                                        circle = Circle(random.randint(20,800), random.randint(20, 575), random.randint(20,100), (random.randint(100,255), random.randint(100,255), random.randint(100,255)))
                                    
                                    #Creating a variable to get the position of the mouse
                                    mousePosition = pygame.mouse.get_pos()
                                    
                                    #Setting variables for the position of the cursor
                                    markerX = mousePosition[0] - (markerSize[0]//2)
                                    markerY = mousePosition[1] - (markerSize[1]//2)
                                    
                                    #Recalling this function to check if the player hit the circle or not
                                    hitOrMiss()
                                    
                                    #Creating text to display the player's score, accuracy, and time left
                                    click = font.render("You literally just click the circles dude, it's that easy", 1, (255,255,255))
                                    watchOut = font.render("Just watch out for the red dot in the real game!", 1, (255,255,255))
                                    exitAsk = font.render("Press 'N' on your keyboard to exit the tutorial", 1, (255,255,255))
                                    
                                    #Blitting the text onto the screen
                                    screen.blit(click, (100, 10))
                                    screen.blit(watchOut, (150, 40))
                                    screen.blit(exitAsk, (150, 530))
                                    screen.blit(hitMarker,(markerX,markerY))
                                    
                                    #---------------------------------------------------------------------
                                    #Screen Update
                                    #---------------------------------------------------------------------
                                    pygame.display.update()
                                    fpsClock.tick(fpsLock)
                                    
                                    if exit > 0:
                                        break
                                    
                    #---------------------------------------------------------------------
                    #Runtime
                    #---------------------------------------------------------------------
                    screen.fill(pygame.Color(255,255,255))
                    
                    #Creating the how to play instructions
                    howTP = font.render("How to Play:", 1, (0,0,0))
                    instruct = font.render("Click as many circles as you can in 30 seconds.", 1, (0,0,0))
                    warning = font.render("Watch out for the red dot, it will kill you!", 1, (0,0,0))
                    start = font.render("Press the enter key to continue or the T key to play the tutorial", 1, (0,0,0))
                    
                    #Blitting the text onto the screen
                    screen.blit(howTP, (350, 150))
                    screen.blit(instruct, (180, 250))
                    screen.blit(warning, (210, 300))
                    screen.blit(start, (100, 450))
                    #---------------------------------------------------------------------
                    #Screen Update
                    #---------------------------------------------------------------------
                    pygame.display.update()
                    fpsClock.tick(fpsLock)
            
            
            #If the user says there are 2 people playing, the game brings them into the multiplayer game loop
            elif event.key == pygame.K_2:
                
                #Setting the number of players to 2
                players = 2
                
                while True:
                    #---------------------------------------------------------------------
                    #Events
                    #---------------------------------------------------------------------
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                            
                        elif event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_RETURN:
                                
                                #Displaying the countdown timer
                                for i in range(180):
                                    screen.fill(pygame.Color(0,0,0))
                                
                                    timer = font.render("Ready? " + str((countdown - (seconds1 // fpsLock))), 1, (255,255,255))
                                    
                                    screen.blit(timer, (350, 300))
                                    
                                    pygame.display.update()
                                    fpsClock.tick(fpsLock)
                                    
                                    seconds1 += 1
                                    
                                while True:
                                    
                                    #Setting the red dot radius to 20 so that player 2 has a chance of killing player 1
                                    radius = 20
                                    
                                    #---------------------------------------------------------------------
                                    #Events
                                    #---------------------------------------------------------------------
                                    for event in pygame.event.get():
                                        if event.type == pygame.QUIT:
                                            pygame.quit()
                                            sys.exit()
                                            
                                        elif event.type == pygame.KEYDOWN:
                                            if event.key == pygame.K_ESCAPE:
                                                sys.exit()
                                            
                                            #Programming player 2 controls so i could input velocity
                                            elif event.key == pygame.K_a:
                                                velX -= 3 * speedDeath
                                            elif event.key == pygame.K_d:
                                                velX += 3 * speedDeath
                                            elif event.key == pygame.K_s:
                                                velY += 3 * speedDeath
                                            elif event.key == pygame.K_w:
                                                velY -= 3 * speedDeath
                                        
                                        elif event.type == pygame.KEYUP:
                                            
                                            #Once player 2 stop pressing down on a control, the dot stops moving
                                            if event.key == pygame.K_a:
                                                velX = 0
                                            elif event.key == pygame.K_d:
                                                velX = 0
                                            elif event.key == pygame.K_s:
                                                velY = 0
                                            elif event.key == pygame.K_w:
                                                velY = 0
                                    #---------------------------------------------------------------------
                                    #Runtime
                                    #---------------------------------------------------------------------
                                    screen.fill(pygame.Color(0,0,0))
                                    
                                    #Drawing the circle for player 1 if there currently aren't any
                                    if circle == None:
                                        circle = Circle(random.randint(20,800), random.randint(20, 575), random.randint(20,100), (random.randint(100,255), random.randint(100,255), random.randint(100,255)))
                                    
                                    
                                    #Getting the position of the mouse and making it into the position of the hitmarker
                                    mousePosition = pygame.mouse.get_pos()
                                    
                                    markerX = mousePosition[0] - (markerSize[0]//2)
                                    markerY = mousePosition[1] - (markerSize[1]//2)
                                    
                                    #Changing the position of player 2 depending on which key they pressed
                                    deathX += velX
                                    deathY += velY
                                    
                                    #Creating boundaries so that player 2 can't go off screen
                                    if deathX > 800:
                                        deathX = 800
                                        
                                    elif deathX < 0:
                                        deathX = 0
                                    
                                    elif deathY > 575:
                                        deathY = 575
                                        
                                    elif deathY < 0:
                                        deathY = 0
                                    
                                    #Recalling this function to check if the player hit the circle or not
                                    hitOrMiss()
                                    
                                    #Making the text to show the players' scores
                                    score1 = font.render("Player 1 Score: " + str(hits), 1, (255,255,255))
                                    score2 = font.render("Player 2 Score: " + str(hit2), 1, (255,255,255))
                                    
                                    #Checking if player 2 collided with player 1
                                    gameOver()
                                    
                                    #Blitting everything onto the screen
                                    screen.blit(score2, (350, 10))
                                    screen.blit(score1, (50, 10))
                                    screen.blit(hitMarker,(markerX,markerY))
                                    pygame.draw.circle(screen, (255,0,0),(int(deathX),int(deathY)), 25)
                                    #---------------------------------------------------------------------
                                    #Screen Update
                                    #---------------------------------------------------------------------
                                    pygame.display.update()
                                    fpsClock.tick(fpsLock)
                                    
                                    seconds2 += 1
                            
                    #---------------------------------------------------------------------
                    #Runtime
                    #---------------------------------------------------------------------
                    screen.fill(pygame.Color(255,255,255))
                    
                    #Creating text of the instructions for 2 player mode
                    how = font.render("How to Play:", 1, (0,0,0))
                    s = font.render("Player 1 (mouse): Click the circles and avoid the red dot.", 1, (0,0,0))
                    a = font.render("Player 2 (keyboard): Use WASD to kill Player 1!", 1, (0,0,0))
                    enter = font.render("Press the enter key to continue", 1, (0,0,0))
                    
                    #Blitting the text onto the screen
                    screen.blit(how, (350, 150))
                    screen.blit(s, (120, 250))
                    screen.blit(a, (200, 300))
                    screen.blit(enter, (250, 500))
                    #---------------------------------------------------------------------
                    #Screen Update
                    #---------------------------------------------------------------------
                    pygame.display.update()
                    fpsClock.tick(fpsLock)
    
    #---------------------------------------------------------------------
    #Runtime
    #---------------------------------------------------------------------
    screen.fill(pygame.Color(255,255,255))
    
    #Creating the text to ask how many players are playing
    option = font.render("How many players are there?:", 1, (0,0,0))
    limit = font.render("Maximum amount of players is 2", 1, (0,0,0))
    enter = font.render("Press the number of players on your keyboard", 1, (0,0,0))
    
    #Blitting the text onto the screen
    screen.blit(option, (270, 200))
    screen.blit(limit, (250, 250))
    screen.blit(enter, (190, 300))
    #---------------------------------------------------------------------
    #Screen Update
    #---------------------------------------------------------------------
    pygame.display.update()
    fpsClock.tick(fpsLock)