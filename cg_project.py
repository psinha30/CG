
import pygame
import sys
from math import *
import tkinter as tk
from tkinter import simpledialog

# Initialization of Pygame
pygame.init() #initialisation of pygame as to avoid any errors while importing

width = 400 #window size
height = 400 # window size
display = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

# Colors
background = (21, 67, 96)
border = (208, 211, 212)
red = (231, 76, 60)
white = (244, 246, 247)
violet = (136, 78, 160)
yellow = (244, 208, 63)
green = (88, 214, 141)

playerColor = [red, green, violet, yellow] # no if colours

font = pygame.font.SysFont("Times New Roman", 30)

ROOT = tk.Tk()

ROOT.withdraw()
# the input dialog
USER_INP = simpledialog.askstring(title="",
                                  prompt="Number of Players(Max 4):")
noPlayers = int(USER_INP)
blocks = 40
pygame.display.set_caption("Chain Reaction %d Player" % noPlayers)

score = []
for i in range(noPlayers):
    score.append(0)

players = []
out_players  = {}
for i in range(noPlayers):
    players.append(playerColor[i])
    out_players[i] = 1

d = blocks//2 - 2

cols = int(width//blocks)
rows = int(height//blocks)

grid = []

# Quit or Close the Game Window
def close():
    pygame.quit()
    sys.exit()

# Class for Each Spot in Grid
class Spot():
    def __init__(self):
        self.color = border
        self.neighbors = []
        self.noAtoms = 0

    def addNeighbors(self, i, j):
        """
        0 1 2 3 4 5 6 7 8 9
       0 * * * * * * * * * *
       1 * * * * * * * * * *
       2 * * * * * * * * * *
       3 * * * * * * * * * *
       5 * * * * * * * * * *
       6 * * * * * * * * * *
       7 * * * * * * * * * *
       8 * * * * * * * * * *
       9 * * * * * * * * * *
        
        """
        # assigning neighbours for left  and right neighbours in the grid
        if i > 0: # i is column and j is row
            self.neighbors.append(grid[i - 1][j]) # left neighbour
        if i < rows - 1: # i< 10 -1 = i< 9
            self.neighbors.append(grid[i + 1][j]) # right neighbour
        # assigning neighbours for above and below  neighbours in the grid
        if j < cols - 1:
            self.neighbors.append(grid[i][j + 1])
        if j > 0:
            self.neighbors.append(grid[i][j - 1])

# Initializing the Grid with "Empty or 0"
def initializeGrid():
    global grid, score, players
    score = []
    for i in range(noPlayers):
        score.append(0)

    players = []
    for i in range(noPlayers):
        players.append(playerColor[i])

    grid = [[]for _ in range(cols)]  # creating grid as [ [], [], [], [], [], [], [] ]
    for i in range(cols): # if block size ==10 then len cols = 10
        for j in range(rows): # len rows = 10
            newObj = Spot()
            grid[i].append(newObj)   # filling  grid witth three props  [ [], [], [], [], [], [], [] ]
    for i in range(cols):
        for j in range(rows):
            grid[i][j].addNeighbors(i, j)

# Draw the Grid in Pygame Window   
def drawGrid(currentIndex):
    r = 0
    c = 0
    for i in range(width//blocks):
        r += blocks
        c += blocks
        pygame.draw.line(display, players[currentIndex], (c, 0), (c, height))
        pygame.draw.line(display, players[currentIndex], (0, r), (width, r))

# Draw the Present Situation of Grid
def showPresentGrid(vibrate = 1):
    r = -blocks # -40
    c = -blocks # -40
    padding = 2
    for i in range(cols):
        r += blocks # i=0 r=0
        c = -blocks  # i=0 c=-40
        for j in range(rows):
            c += blocks
            if grid[i][j].noAtoms == 0:
                grid[i][j].color = border
            elif grid[i][j].noAtoms == 1:
                pygame.draw.ellipse(display, grid[i][j].color, (r + blocks/2 - d/2 + vibrate, c + blocks/2 - d/2, d, d))
            elif grid[i][j].noAtoms == 2:
                pygame.draw.ellipse(display, grid[i][j].color, (r + 5, c + blocks/2 - d/2 - vibrate, d, d))
                pygame.draw.ellipse(display, grid[i][j].color, (r + d/2 + blocks/2 - d/2 + vibrate, c + blocks/2 - d/2, d, d))
            elif grid[i][j].noAtoms == 3:
                angle = 90
                x = r + (d/2)*cos(radians(angle)) + blocks/2 - d/2
                y = c + (d/2)*sin(radians(angle)) + blocks/2 - d/2
                pygame.draw.ellipse(display, grid[i][j].color, (x - vibrate, y, d, d))
                x = r + (d/2)*cos(radians(angle + 90)) + blocks/2 - d/2
                y = c + (d/2)*sin(radians(angle + 90)) + 5
                pygame.draw.ellipse(display, grid[i][j].color, (x + vibrate, y, d, d))
                x = r + (d/2)*cos(radians(angle - 90)) + blocks/2 - d/2
                y = c + (d/2)*sin(radians(angle - 90)) + 5
                pygame.draw.ellipse(display, grid[i][j].color, (x - vibrate, y, d, d))

    pygame.display.update()

# Increase the Atom when Clicked
def addAtom(i, j, color):
    grid[i][j].noAtoms += 1
    grid[i][j].color = color
    if grid[i][j].noAtoms >= len(grid[i][j].neighbors):
        overFlow(grid[i][j], color)
    
# Split the Atom when it Increases the "LIMIT"
def overFlow(cell, color):
    showPresentGrid()
    cell.noAtoms = 0
    for m in range(len(cell.neighbors)):
        cell.neighbors[m].noAtoms += 1
        cell.neighbors[m].color = color
        if cell.neighbors[m].noAtoms >= len(cell.neighbors[m].neighbors):
            overFlow(cell.neighbors[m], color)

# Checking if Any Player has WON!

def isPlayerInGame():
    global score, out_players
    playerScore = []
    for i in range(noPlayers):
        playerScore.append(0)
    for i in range(cols):
        for j in range(rows):
            for k in range(noPlayers):
                if grid[i][j].color == players[k]:
                    playerScore[k] += grid[i][j].noAtoms
    score = playerScore[:]
    for i in range(len(score)):
      if score[i]==0:
        out_players[i] = 0
      else:
        out_players[i] = 1
    #print(score)

# GAME OVER
def gameOver(playerIndex):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                close()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    close()
                if event.key == pygame.K_r:
                    main()

        text = font.render("Player %d Won!" % (playerIndex + 1), True, white)
        text2 = font.render("Press \'r\' to Reset!", True, white)

        display.blit(text, (width/3, height/3))
        display.blit(text2, (width/3, height/2 ))

        pygame.display.update()
        clock.tick(60)


def checkWon():
    num = 0
    for i in range(noPlayers):
        if score[i] == 0:
            num += 1
    if num == noPlayers - 1:
        for i in range(noPlayers):
            if score[i]:
                return i

    return 9999

# Main Loop
def main():
    global out_players
    initializeGrid() # grid initialisation with score 0 and giving players the clours
    loop = True

    turns = 0
    
    currentPlayer = 0

    vibrate = .5

    while loop: # infinite loop until game ends
        for event in pygame.event.get(): # follows a queue of instructions  follows FIFO
            if event.type == pygame.QUIT: 
                close()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    close()
            if out_players[currentPlayer]==0:
                    currentPlayer += 1
                    turns += 1
            else:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    
                        x, y = pygame.mouse.get_pos()
                        i = x//blocks  # 0 to 10
                        j = y//blocks  # 0 to 10
                        if grid[i][j].color == players[currentPlayer] or grid[i][j].color == border :
                            print(out_players)
                            turns += 1
                            addAtom(i, j, players[currentPlayer])
                            currentPlayer += 1
                        if currentPlayer >= len(out_players):
                            currentPlayer = 0
                        if turns >= len(out_players):
                            isPlayerInGame()
                
        
        display.fill(background)
        # Vibrate the Atoms in their Cells
        vibrate *= -1
        drawGrid(currentPlayer)
        showPresentGrid(vibrate)
        
        pygame.display.update()

        res = checkWon()
        if res < 9999:
            gameOver(res)

        clock.tick(20)

if __name__=='__main__':
    main()# start of game 
"""
Constant      ASCII   Description
---------------------------------
K_BACKSPACE   \b      backspace
K_TAB         \t      tab
K_CLEAR               clear
K_RETURN      \r      return
K_PAUSE               pause
K_ESCAPE      ^[      escape
K_SPACE               space
K_EXCLAIM     !       exclaim
K_QUOTEDBL    "       quotedbl
K_HASH        #       hash
K_DOLLAR      $       dollar
K_AMPERSAND   &       ampersand
K_QUOTE               quote
K_LEFTPAREN   (       left parenthesis
K_RIGHTPAREN  )       right parenthesis
K_ASTERISK    *       asterisk
K_PLUS        +       plus sign
K_COMMA       ,       comma
K_MINUS       -       minus sign
K_PERIOD      .       period
K_SLASH       /       forward slash
K_0           0       0
K_1           1       1
K_2           2       2
K_3           3       3
K_4           4       4
K_5           5       5
K_6           6       6
K_7           7       7
K_8           8       8
K_9           9       9
K_COLON       :       colon
K_SEMICOLON   ;       semicolon
K_LESS        <       less-than sign
K_EQUALS      =       equals sign
K_GREATER     >       greater-than sign
K_QUESTION    ?       question mark
K_AT          @       at
K_LEFTBRACKET [       left bracket
K_BACKSLASH   \       backslash
K_RIGHTBRACKET ]      right bracket
K_CARET       ^       caret
K_UNDERSCORE  _       underscore
K_BACKQUOTE   `       grave
K_a           a       a
K_b           b       b
K_c           c       c
K_d           d       d
K_e           e       e
K_f           f       f
K_g           g       g
K_h           h       h
K_i           i       i
K_j           j       j
K_k           k       k
K_l           l       l
K_m           m       m
K_n           n       n
K_o           o       o
K_p           p       p
K_q           q       q
K_r           r       r
K_s           s       s
K_t           t       t
K_u           u       u
K_v           v       v
K_w           w       w
K_x           x       x
K_y           y       y
K_z           z       z
K_DELETE              delete
K_KP0                 keypad 0
K_KP1                 keypad 1
K_KP2                 keypad 2
K_KP3                 keypad 3
K_KP4                 keypad 4
K_KP5                 keypad 5
K_KP6                 keypad 6
K_KP7                 keypad 7
K_KP8                 keypad 8
K_KP9                 keypad 9
K_KP_PERIOD   .       keypad period
K_KP_DIVIDE   /       keypad divide
K_KP_MULTIPLY *       keypad multiply
K_KP_MINUS    -       keypad minus
K_KP_PLUS     +       keypad plus
K_KP_ENTER    \r      keypad enter
K_KP_EQUALS   =       keypad equals
K_UP                  up arrow
K_DOWN                down arrow
K_RIGHT               right arrow
K_LEFT                left arrow
K_INSERT              insert
K_HOME                home
K_END                 end
K_PAGEUP              page up
K_PAGEDOWN            page down
K_F1                  F1
K_F2                  F2
K_F3                  F3
K_F4                  F4
K_F5                  F5
K_F6                  F6
K_F7                  F7
K_F8                  F8
K_F9                  F9
K_F10                 F10
K_F11                 F11
K_F12                 F12
K_F13                 F13
K_F14                 F14
K_F15                 F15
K_NUMLOCK             numlock
K_CAPSLOCK            capslock
K_SCROLLOCK           scrollock
K_RSHIFT              right shift
K_LSHIFT              left shift
K_RCTRL               right control
K_LCTRL               left control
K_RALT                right alt
K_LALT                left alt
K_RMETA               right meta
K_LMETA               left meta
K_LSUPER              left Windows key
K_RSUPER              right Windows key
K_MODE                mode shift
K_HELP                help
K_PRINT               print screen
K_SYSREQ              sysrq
K_BREAK               break
K_MENU                menu
K_POWER               power
K_EURO                Euro


"""
