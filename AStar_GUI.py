import pygame
import sys
import math
import tkinter
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import os
import sys  # for exit and arg

import simple_AStar as simp

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
PURPLE = (255, 0, 255)
YELLOW = (255, 255, 0)
GRAY = (128, 128, 128)
# Size of screen
size = 800

# Create the columns dn rows to be half the size
cols = 100
rows = 100

# Create a 2 dimensional array. A two dimensional
# array is simply a list of lists.
grid = []
for row in range(rows):
    # Add an empty array that will hold each cell
    # in this row
    grid.append([])
    for column in range(cols):
        grid[row].append(0)  # Append a cell


# Sample start and end node
# start = grid[11][21] = 1
# end = grid[9][3] = 2

# Function runs when submit button is pressed
def onsubmit():
    global start
    global end
    # Get individual numbers from input
    st = startBox.get().split(',')
    ed = endBox.get().split(',')

    start = (int(st[0]), int(st[1]))
    print(start)
    end = (int(ed[0]), int(ed[1]))
    print(end)
    # Store them into the grid
    gridStart = grid[int(st[0])][int(st[1])] = 1
    gridEnd = grid[int(ed[0])][int(ed[1])] = 2
    root.quit()
    root.destroy()


# creating main tkinter window/toplevel
root = tkinter.Tk()
root.title('Set Node Positions')

message = ttk.Label(root, text='Enter Values from 0 to ' + str(cols - 1))
message.grid(row=0, columnspan=2)

# this will create a label widget
# for start and end position
startLabel = ttk.Label(root, text='Start Position (X,Y): ')
endLabel = ttk.Label(root, text='End Position (X,Y): ')

# grid method to arrange labels in respective
# rows and columns as specified
startLabel.grid(row=1, column=0, sticky=W, pady=2)
endLabel.grid(row=2, column=0, sticky=W, pady=2)

# entry widgets, used to take entry from user
startBox = Entry(root)
endBox = Entry(root)

# this will arrange entry widgets
startBox.grid(row=1, column=1, pady=2)
endBox.grid(row=2, column=1, pady=2)
# Create style
style = ttk.Style()
style.configure("Red.TCheckbutton", foreground="red")

# checkbutton widget
checkVar1 = IntVar()
playButton = ttk.Checkbutton(root, text='Show Steps', onvalue=1, offvalue=0, variable=checkVar1)
playButton.grid(row=3, columnspan=2)  # Set up text box iterations
playButton.configure(style="Red.TCheckbutton")
# button widget
submit = Button(root, text='Submit', command=onsubmit)
submit.grid(row=4, columnspan=2)

# playButton.pack()
# root.mainloop()  # Rest of the script won't execute until playButton pressed
root.update()
mainloop()

# Initialize pygame window
pygame.init()

screen = pygame.display.set_mode((size, size))
pygame.display.set_caption("A* Path-finding Algorithm")
# Set the screen background
screen.fill(BLACK)

# This sets the WIDTH and HEIGHT of each grid location
WIDTH = size / cols
HEIGHT = size / rows

# This sets the margin between each cell
MARGIN = 1


# Node for path finding algorithm
class Node():
    """A node class for A* Pathfinding"""

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position


# Initial grid for start pygame
def drawGrid():
    global rectangles
    global rect
    rectangles = []
    # Draw the grid
    for row in range(rows):
        for column in range(cols):
            color = WHITE
            # Start Value
            if grid[row][column] == 1:
                color = GREEN
            # End Value
            if grid[row][column] == 2:
                color = RED
            rect = pygame.Rect((MARGIN + WIDTH) * column + MARGIN,
                               (MARGIN + HEIGHT) * row + MARGIN,
                               WIDTH,
                               HEIGHT)
            pygame.draw.rect(screen,
                             color,
                             rect)
            rectangles.append((rect, color))


# Determines the maze values dynamically when clicked
# 1 is blocked
# 0 is open
def maze(listC):
    # Create maze to maneuver
    output = [[0 for y in range(cols)] for x in range(rows)]
    # print(output)
    # Transverse the output
    # output[gY][gX] = 1
    for i in listC:
        output[i[1]][i[0]] = 1
    return output


# Function that identifies the coordinates of
# the mouse click
def mousePress(click):
    # Identify X and Y indications of mouse click
    x = click[0]
    y = click[1]
    # Change the x/y screen coordinates to grid coordinates
    gridColumn = x // (WIDTH + MARGIN)
    gridRow = y // (HEIGHT + MARGIN)
    # print(gridColumn)
    # print(gridRow)
    # access = grid[gridRow][gridColumn]
    # print(access)
    # print(maze(gridX, gridY))
    return [int(gridColumn), int(gridRow)]


# Function displays the color on the grid given a index
def show(loopIndex, gridColor):
    row = loopIndex[0]
    column = loopIndex[1]
    idx = (row * rows) + column
    rect = pygame.Rect((MARGIN + WIDTH) * column + MARGIN,
                       (MARGIN + HEIGHT) * row + MARGIN,
                       WIDTH,
                       HEIGHT)
    # print(idx)
    rectangles[idx] = (rect, gridColor)
    pygame.draw.rect(screen, color, rect)
    pygame.display.update()


# Main Code to Run
running = True
count = 0
listClicks = []
while running:
    if count == 0:
        # Draw initial grid
        drawGrid()
    else:
        # maze =

        # path = s.aStar(maze(), start, end)
        # print(path)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            elif pygame.mouse.get_pressed()[0]:
                mouse_pos = pygame.mouse.get_pos()
                # Store values of one mouse click
                click = mousePress(mouse_pos)
                # print(click)
                # create a list of off all clicks
                listClicks.append(click)

                # Enumerate creates tuples of a number (the index)
                # and the rect-color tuple, so it looks like:
                # (0, (<rect(0, 0, 20, 20)>, (255, 255, 255)))
                # You can unpack them directly in the head of the loop.
                for index, (rect, color) in enumerate(rectangles):
                    if rect.collidepoint(mouse_pos):
                        # Create a tuple with the new color and assign it.
                        rectangles[index] = (rect, GRAY)
                        # print(index)
            elif event.type == pygame.KEYDOWN:
                # When you press escape key
                # quit the program
                if event.key == pygame.K_ESCAPE:
                    running = False
                    pygame.quit()
                    sys.exit()
                # When you press the space bar
                # The algorithm is solved
                elif event.key == pygame.K_SPACE:
                    path, steps = simp.aStar(maze(listClicks), start, end)
                    # print(steps)
                    # print(path)
                    # JUST SHOW THE STEPS AND PATH
                    if checkVar1.get():
                        for phase in steps:
                            # Check if step is in path
                            if phase in path:
                                # print("Found")
                                # IF START IS FOUND
                                if phase == start:
                                    show(phase, GREEN)
                                # IF END IS FOUND
                                elif phase == end:
                                    show(phase, RED)
                                # IF PATH IS FOUND
                                else:
                                    show(phase, PURPLE)
                            # Steps the algorithm had to take to get to the
                            # solution
                            else:
                                show(phase, YELLOW)
                        # Update all rectangles
                        for rect, color in rectangles:
                            pygame.draw.rect(screen, color, rect)
                            pygame.display.update()
                    # JUST SHOW THE PATH
                    else:
                        for node in path:
                            # If node does not equal start or end
                            if node != start and node != end:
                                show(node, PURPLE)
                        # Update all rectangles
                        for rect, color in rectangles:
                            pygame.draw.rect(screen, color, rect)
                            pygame.display.update()

                    # Ask Re-Run program
                    tkinter.Tk().wm_withdraw()
                    result = tkinter.messagebox.askokcancel('Done!', (
                            'The program finished running, and the shortest distance \n to the path is '
                            + str(len(path)-2) + ' blocks away, \n Do you want to run it again?'))
                    # IF you would like to Re-run the program
                    if result:
                        os.execl(sys.executable, sys.executable, *sys.argv)
                    #
                    else:
                        ag = True
                        while ag:
                            ev = pygame.event.get()
                            for event in ev:
                                if event.type == pygame.KEYDOWN:
                                    ag = False
                                    break
                    pygame.quit()

        # screen.fill(BLACK)
        # Now draw the rects. You can unpack the tuples
        # again directly in the head of the for loop.
        for rect, color in rectangles:
            pygame.draw.rect(screen, color, rect)
    # Go ahead and update the screen with what we've drawn.
    pygame.display.update()
    count += 1
