import tkinter as tk
import random
from time import sleep

def tkDestroyWindow(root):
    root.destroy()

def tkCreateAndPlaceButton(root, text, width, font_size, pos=[0, 0], tkDestroyWindow=None, color='black', bg=None):
    button = tk.Button(root, text=text, width=width, font=('Arial', font_size), fg=color, bg=bg, command=lambda: tkDestroyWindow(root))
    button.place(x=pos[0], y=pos[1])
    return button

def tkPlaceScore(root):
    scoreLabel = tk.Label(root, text='Score: x', width=16, font=('Arial', 14), fg='yellow', bg='black')
    scoreLabel.place(x=700, y=12)

def tkPlaceLives(root, livesText):
    scoreLabel = tk.Label(root, textvariable=livesText, width=16, font=('Arial', 14), fg='yellow', bg='black')
    scoreLabel.place(x=550, y=12)

def tkPlaceStartMenu(root, window_size):
    startButton = tkCreateAndPlaceButton(root, 'Start', 16, 14, [(int(window_size[0]) // 2) - 90, 150])
    quitButton = tkCreateAndPlaceButton(root, 'Quit', 16, 14, [(int(window_size[0]) // 2) - 90, 200], tkDestroyWindow)

class Game:
    def __init__(self, window_size, tkWindow, title, lives, livesText):
        self.window_size = window_size
        self.tkWindow = tkWindow
        self.title = title
        self.lives = lives
        self.livesText = livesText
        self.racket = None
        self.ball = None

    def removeLife(self):
        self.lives -= 1
        self.livesText.set(str(self.lives))

        if self.lives == 0:
            self.tkWindow.quit()

def tkInitTkinter(root, window_size, window_name, color, lives, livesText):
    root.title(window_name)
    root.geometry('x'.join(window_size))
    root.configure(bg=color)

    menubar = tk.Menu(root)
    menu_file = tk.Menu(menubar, tearoff=0)
    menu_file.add_command(label="Option 1")
    menu_file.add_command(label="Option 2")

    menubar.add_cascade(label="Settings", menu=menu_file)
    root.config(menu=menubar)

    game = Game(window_size, root, window_name, lives, livesText)

    return root, game

class Racket:
    def __init__(self, window_size):
        self.offset = 0
        self.color = 'blue'
        self.width = 100
        self.posx = int(window_size[0]) // 2 - 50
        self.speed = 10

    def move_left(self):
        if  self.posx > 0:
            self.posx -= self.speed

    def move_right(self):
        if self.posx + self.width < 980:
            self.posx += self.speed

def tkPlaceGameCanvas(root, window_size):
    gameCanvas = tk.Canvas(root, width=980, height=620, bg='black')
    gameCanvas.place(x=10, y=60)
    return gameCanvas

def tkPlaceRacket(root, window_size):
    racket = Racket(window_size)
    racket_widget = tk.Canvas(root, width=racket.width, height=10, bg=racket.color)
    racket_widget.place(x=racket.posx, y=580)
    racket.widget = racket_widget 
    return racket

#0 = left, 1 = right
def tkMoveRacket(racket, direction):
    if direction == 0:
        racket.move_left()
    else:
        racket.move_right()
    
    racket.widget.place(x=racket.posx, y=580)

class Brique:
    def __init__(self, window_size, posx=10, posy=10):
        self.offset = 0
        self.color = 'red'
        self.width = int(window_size[0]) / 10
        self.posx = posx
        self.posy = posy
        self.widget = None

    def destroy(self):
        self.widget.destroy()

def tkPlaceBrique(root, window_size):
    brique = Brique(window_size, posx=10, posy=10)
    brique_widget = tk.Canvas(root, width=brique.width, height=20, bg=brique.color)
    brique_widget.place(x=brique.posx, y=brique.posy)
    brique.widget = brique_widget
    return brique

def tkPlaceAllBriques(root, gapx, gapy, padding, window_size):
    briques = []
    cols = 8
    brick_width = int(window_size[0]) / (cols + 1)
    brick_height = 20

    total_grid_width = cols * brick_width + (cols - 1) * gapx + cols*2
    start_x = (int(window_size[0]) - total_grid_width) / 2

    for y in range(3):
        for x in range(cols):
            posx = start_x + x * (brick_width + gapx)
            posy = padding + y * (brick_height + gapy)
            brique = Brique(window_size, posx=posx, posy=posy)

            widget = tk.Canvas(root, width=brick_width, height=brick_height, bg=brique.color)
            widget.place(x=posx, y=posy)
            brique.widget = widget

            briques.append(brique)

    return briques



class Ball:
    def __init__(self, window_size, speed, game):
        self.posx = int(window_size[0]) // 2 - 10
        self.posy = 300 
        self.radius = 5
        self.speed = speed
        self.angle = random.randint(45, 135)
        self.game = game
        
        self.speed_x = self.speed * random.choice([-1, 1])
        self.speed_y = self.speed * random.choice([-1, 1])
        
    def move(self, game, racket):
        self.posx += self.speed_x
        self.posy += self.speed_y

        if self.posy == 600:
            game.removeLife()

        """ 
                ball_edge_x = self.posx + self.radius
                if 565 < self.posy < 590:
                    if racket.posx <= ball_edge_x <= racket.posx + racket.width:
                        self.speed_y *= -1
                    elif (racket.posx - 5) <= ball_edge_x <= (racket.posx + 5) or (racket.posx + racket.width - 5) <= ball_edge_x <= (racket.posx + racket.width + 5):
                        self.speed_x *= -1
        """
        ball_edge_x = self.posx + self.radius
        if (565 < self.posy < 590) and self.speed_y >0:
            if (racket.posx) <= ball_edge_x <= (racket.posx + racket.width):

                self.speed_y *= -1

        #racket_left=racket.posx - 

        if self.posx <= 0 or self.posx >= 980 - self.radius * 2:
            self.speed_x *= -1
        if self.posy <= 0 or self.posy >= 620 - self.radius * 2:
            self.speed_y *= -1

def tkPlaceBall(game, root, window_size, racket, briques, fps=200):
    ball = Ball(window_size, speed = 2, game = game)
    
    ball_widget = tk.Canvas(root, width=ball.radius * 2, height=ball.radius * 2, highlightthickness=0, bg='black')
    ball_widget.place(x=ball.posx, y=ball.posy)
    ball_widget.create_oval(0, 0, ball.radius * 2, ball.radius * 2, fill='red', outline='black')
    ball.widget = ball_widget

    def tkUpdateBall():
        ball.move(game, racket)
        ball.widget.place(x=ball.posx, y=ball.posy)

        for brique in briques:
            ball_left = ball.posx
            ball_right = ball.posx + 2 * ball.radius
            ball_top = ball.posy
            ball_bottom = ball.posy + 2 * ball.radius

            brick_left = brique.posx
            brick_right = brique.posx + brique.width
            brick_top = brique.posy
            brick_bottom = brique.posy + 20  # brick height is 20

            # Check if bounding boxes overlap
            if (ball_right > brick_left and
                ball_left < brick_right and
                ball_bottom > brick_top and
                ball_top < brick_bottom):
                
                brique.destroy()
                briques.remove(brique)
                ball.speed_y *= -1
                break

        root.after(1000 // fps, tkUpdateBall)

    tkUpdateBall() 
    return ball
