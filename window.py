import tkinter as tk
from brique import Brique
from racket import Racket
from game import Game
from ball import Ball
from tkinter import messagebox

def show_rules():
    try:
        with open("readme", "r") as file:
            content = file.read()
        messagebox.showinfo("Rules", content)
    except FileNotFoundError:
        messagebox.showerror("Error", "File 'readme' not found!")

class Window:
    def __init__(self):
        self.game = None
        self.tkWindow = None

    def tkInitTkinter(self, root, window_size, window_name, color, lives, livesText, score, scoreText):
        root.title(window_name)
        root.geometry('x'.join(window_size))
        root.configure(bg=color)

        menubar = tk.Menu(root)
        menu_file = tk.Menu(menubar, tearoff=0)
        menu_file.add_command(label="Option 1")
        menu_file.add_command(label="Option 2")

        menubar.add_cascade(label="Settings", menu=menu_file)
        #make open file "readme" and display content
        menubar.add_command(label="Rules", command=show_rules)
        root.config(menu=menubar)

        game = Game(window_size, root, window_name, lives, livesText, score, scoreText)

        return root, game

    def tkDestroyWindow(self, root):
        root.destroy()

    def makeGameWindow(self, root, game, window, WINDOW_SIZE, livesText, scoreText):
        gameCanvas = window.tkPlaceGameCanvas(root, WINDOW_SIZE)

        racket = window.tkPlaceRacket(gameCanvas, WINDOW_SIZE)
        game.racket = racket

        briques = window.tkPlaceAllBriques(gameCanvas, 7, 7, 20, WINDOW_SIZE)
        game.briques = briques

        root.bind("<Left>", lambda event: racket.moveRacket(racket, 0))
        root.bind("<Right>", lambda event: racket.moveRacket(racket, 1))

        window.tkPlaceBall(game, gameCanvas, window, WINDOW_SIZE, gameCanvas, briques, livesText, scoreText, fps=1000)

        window.tkPlaceScore(root, scoreText)
        window.tkPlaceLives(root, livesText)

    def tkCreateAndPlaceButton(self, root, text, width, font_size, pos=[0, 0], tkDestroyWindow=None, color='black', bg=None):
        button = tk.Button(root, text=text, width=width, font=('Arial', font_size), fg=color, bg=bg, command=lambda:  self.tkDestroyWindow(root,))
        button.place(x=pos[0], y=pos[1])
        return button

    def tkPlaceScore(self, root, scoreText):
        scoreLabel = tk.Label(root, textvariable=scoreText, width=5, font=('Arial', 14), fg='yellow', bg='black')
        scoreLabel.place(x=700, y=12)
        scoreLabelPrefix = tk.Label(root, text="Score: ", width=5, font=('Arial', 14), fg='yellow', bg='black')
        scoreLabelPrefix.place(x=660, y=12)

    def tkPlaceLives(self, root, livesText):
        livesLabelNum = tk.Label(root, textvariable=livesText, width=5, font=('Arial', 14), fg='yellow', bg='black')
        livesLabelNum.place(x=583, y=12)
        livesLabelPrefix = tk.Label(root, text="Lives: ", width=5, font=('Arial', 14), fg='yellow', bg='black')
        livesLabelPrefix.place(x=546, y=12)

    def tkPlaceStartMenu(self, root, game, window, window_size, livesText, scoreText):
        startButton = tk.Button(
            root,
            text='Start',
            width=16,
            font=('Arial', 14),
            command=lambda: self.makeGameWindow(root, game, window, window_size, livesText, scoreText)
        )
        startButton.place(x=(int(window_size[0]) // 2) - 90, y=150)

        quitButton =  self.tkCreateAndPlaceButton(root, 'Quit', 16, 14, [(int(window_size[0]) // 2) - 90, 200])

    def tkPlaceGameCanvas(self, root, window_size):
        gameCanvas = tk.Canvas(root, width=980, height=620, bg='black')
        gameCanvas.place(x=10, y=60)
        return gameCanvas

    def tkPlaceRacket(self, root, window_size):
        racket = Racket(window_size)
        racket_widget = tk.Canvas(root, width=racket.width, height=10, bg=racket.color)
        racket_widget.place(x=racket.posx, y=580)
        racket.widget = racket_widget 
        return racket

    def tkPlaceBrique(self, root, window_size):
        brique = Brique(window_size, posx=10, posy=10)
        brique_widget = tk.Canvas(root, width=brique.width, height=20, bg=brique.color)
        brique_widget.place(x=brique.posx, y=brique.posy)
        brique.widget = brique_widget
        return brique

    def tkPlaceAllBriques(self, root, gapx, gapy, padding, window_size):
        briques = []
        cols = 8
        brick_width = int(window_size[0]) / (cols + 1)
        brick_height = 20

        total_grid_width = cols * brick_width + (cols - 1) * gapx + cols*2
        start_x = (int(window_size[0]) - total_grid_width) / 2

        for y in range(1):
            for x in range(1):
                posx = start_x + x * (brick_width + gapx)
                posy = padding + y * (brick_height + gapy)
                brique = Brique(window_size, posx=posx, posy=posy)

                widget = tk.Canvas(root, width=brick_width, height=brick_height, bg=brique.color)
                widget.place(x=posx, y=posy)
                brique.widget = widget

                briques.append(brique)

        return briques
    
    def tkPlaceBall(self, game, root, window, window_size, gameCanvas, briques, livesText, scoreText, fps=1000):
        ball = Ball(window_size, speed=2, game=game)
        ball_widget = tk.Canvas(root, width=ball.radius*2, height=ball.radius*2, highlightthickness=0, bg='black')
        ball_widget.place(x=ball.posx, y=ball.posy)
        ball_widget.create_oval(0, 0, ball.radius*2, ball.radius*2, fill=game.currentBallColor, outline='black')
        ball.widget = ball_widget
        game.ball = ball  # save reference here

        def tkUpdateBall():
            destroyed = ball.move(root, game, window, gameCanvas, game.racket, briques, ball, window_size, livesText, scoreText)
            if not destroyed:
                if len(briques) != 0:
                    ball.widget.place(x=ball.posx, y=ball.posy)
                    ball.after_id = root.after(1000 // fps, tkUpdateBall)  # store after_id
        tkUpdateBall()
        return ball
