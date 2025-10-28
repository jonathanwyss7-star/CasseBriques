"""
TOUBI Mouaad et Jonathan Wyss
07/10/2025 08:00
Classe qui définit la fenêtre, le menu, la musique et les objets du jeu
"""

import pygame
import tkinter as tk
from brique import Brique
from racket import Racket
from game import Game
from ball import Ball
from tkinter import messagebox

pygame.mixer.init()
pygame.mixer.music.load("song.mp3")  # Musique initiale

def show_rules():
    """Affiche les règles depuis le fichier readme"""
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
        """
        Initialise la fenêtre et le menu principal
        Entrée: root Tk, window_size list[str], window_name str, color str, lives int
                livesText StringVar, score int, scoreText StringVar
        Sortie: root Tk, game Game
        """
        root.title(window_name)
        root.geometry('x'.join(window_size))
        root.configure(bg=color)

        menubar = tk.Menu(root)
        menu_file = tk.Menu(menubar, tearoff=0)
        musicOn = tk.BooleanVar(value=True)

        # Toggle musique simple
        def toggleMusic():
            if musicOn.get():
                if not pygame.mixer.music.get_busy():
                    pygame.mixer.music.play(-1)
            else:
                pygame.mixer.music.stop()

        menu_file.add_checkbutton(
            label="Music",
            onvalue=True,
            offvalue=False,
            variable=musicOn,
            command=toggleMusic
        )

        menubar.add_cascade(label="Settings", menu=menu_file)
        menubar.add_command(label="Rules", command=show_rules)
        root.config(menu=menubar)

        # Crée l'objet game
        game = Game(window_size, root, window_name, lives, livesText, score, scoreText)
        return root, game

    def makeGameWindow(self, root, game, window, WINDOW_SIZE, livesText, scoreText):
        """
        Crée canvas, raquette, briques et balle
        Entrée: root Tk, game Game, window Window, WINDOW_SIZE list[str]
                livesText StringVar, scoreText StringVar
        """
        gameCanvas = window.tkPlaceGameCanvas(root, WINDOW_SIZE)

        # Place raquette et briques
        racket = window.tkPlaceRacket(gameCanvas, WINDOW_SIZE)
        game.racket = racket
        briques = window.tkPlaceAllBriques(gameCanvas, 7, 7, 20, WINDOW_SIZE)
        game.briques = briques

        # Bind touches gauche/droite
        root.bind("<Left>", lambda event: racket.moveRacket(racket, 0))
        root.bind("<Right>", lambda event: racket.moveRacket(racket, 1))

        # Place la balle et labels score/vies
        window.tkPlaceBall(game, gameCanvas, window, WINDOW_SIZE, gameCanvas, briques, livesText, scoreText, fps=250)
        window.tkPlaceScore(root, scoreText)
        window.tkPlaceLives(root, livesText)

    def tkPlaceAllBriques(self, root, gapx, gapy, padding, window_size):
        """
        Place toutes les briques sur le canvas
        Entrée: root Tk, gapx int, gapy int, padding int, window_size list[str]
        Sortie: list[Brique]
        """
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

    def tkPlaceBall(self, game, root, window, window_size, gameCanvas, briques, livesText, scoreText, fps=250):
        """
        Place la balle et la fait bouger automatiquement
        Entrée: game Game, root Tk, window Window, window_size list[str], gameCanvas Canvas
                briques list[Brique], livesText StringVar, scoreText StringVar, fps int
        Sortie: Ball
        """
        racket = game.racket
        ball = Ball(window_size, speed=2, game=game)

        # Change couleur balle
        newColor = game.ballColor.pop()
        game.ballColor.insert(0, game.currentBallColor)
        game.currentBallColor = newColor

        # Canvas de la balle
        ball_widget = tk.Canvas(root, width=ball.radius*2, height=ball.radius*2, highlightthickness=0, bg='black')
        ball_widget.place(x=ball.posx, y=ball.posy)
        ball_widget.create_oval(0, 0, ball.radius*2, ball.radius*2, fill=game.currentBallColor, outline='black')
        ball.widget = ball_widget
        game.ball = ball

        # Mise à jour automatique
        def tkUpdateBall():
            destroyed = ball.move(root, game, window, gameCanvas, game.racket, briques, ball, window_size, livesText, scoreText)
            if not destroyed and len(briques) != 0:
                ball.widget.place(x=ball.posx, y=ball.posy)
                ball.after_id = root.after(1000 // fps, tkUpdateBall)

        tkUpdateBall()
        return ball

    # Méthodes auxiliaires pour boutons, score, vies, canvas, raquette, briques
    def tkCreateAndPlaceButton(self, root, text, width, font_size, pos=[0, 0], tkDestroyWindow=None, color='black', bg=None):
        """Crée un bouton simple"""
        button = tk.Button(root, text=text, width=width, font=('Arial', font_size), fg=color, bg=bg, command=lambda: self.tkDestroyWindow(root,))
        button.place(x=pos[0], y=pos[1])
        return button

    def tkPlaceScore(self, root, scoreText):
        """Affiche score"""
        scoreLabel = tk.Label(root, textvariable=scoreText, width=5, font=('Arial', 14), fg='yellow', bg='black')
        scoreLabel.place(x=700, y=12)
        scoreLabelPrefix = tk.Label(root, text="Score: ", width=5, font=('Arial', 14), fg='yellow', bg='black')
        scoreLabelPrefix.place(x=660, y=12)

    def tkPlaceLives(self, root, livesText):
        """Affiche vies"""
        livesLabelNum = tk.Label(root, textvariable=livesText, width=5, font=('Arial', 14), fg='yellow', bg='black')
        livesLabelNum.place(x=583, y=12)
        livesLabelPrefix = tk.Label(root, text="Lives: ", width=5, font=('Arial', 14), fg='yellow', bg='black')
        livesLabelPrefix.place(x=546, y=12)

    def tkPlaceStartMenu(self, root, game, window, window_size, livesText, scoreText):
        """Place les boutons Start et Quit"""
        startButton = tk.Button(
            root,
            text='Start',
            width=16,
            font=('Arial', 14),
            command=lambda: self.makeGameWindow(root, game, window, window_size, livesText, scoreText)
        )
        startButton.place(x=(int(window_size[0]) // 2) - 90, y=150)
        quitButton = self.tkCreateAndPlaceButton(root, 'Quit', 16, 14, [(int(window_size[0]) // 2) - 90, 200])

    def tkPlaceGameCanvas(self, root, window_size):
        """Crée le canvas du jeu"""
        gameCanvas = tk.Canvas(root, width=980, height=620, bg='black')
        gameCanvas.place(x=10, y=60)
        return gameCanvas

    def tkPlaceRacket(self, root, window_size):
        """Place la raquette"""
        racket = Racket(window_size)
        racket_widget = tk.Canvas(root, width=racket.width, height=10, bg=racket.color)
        racket_widget.place(x=racket.posx, y=580)
        racket.widget = racket_widget
        return racket

    def tkPlaceBrique(self, root, window_size):
        """Place une brique"""
        brique = Brique(window_size, posx=10, posy=10)
        brique_widget = tk.Canvas(root, width=brique.width, height=20, bg=brique.color)
        brique_widget.place(x=brique.posx, y=brique.posy)
        brique.widget = brique_widget
        return brique

    def tkDestroyWindow(self, root):
        """Ferme la fenêtre"""
        root.destroy()
