"""
TOUBI Mouaad et Jonathan Wyss
07/10/2025 08:00
Classe qui gère l'état du jeu, score, vies et briques
"""

from tkinter import messagebox

class Game:
    def __init__(self, window_size, tkWindow, title, lives, livesText, score, scoreText):
        """Initialise le jeu"""
        self.window_size = window_size
        self.tkWindow = tkWindow
        self.title = title
        self.lives = lives
        self.livesText = livesText
        self.score = score
        self.scoreText = scoreText

        self.racket = None      # Raquette
        self.briques = None     # Liste de briques

        self.ballColor = ["red", "green"]
        self.currentBallColor = "blue"

    def removeLife(self, gameCanvas, root, window, WINDOW_SIZE, livesText, scoreText):
        """
        Retire une vie et vérifie si le joueur a perdu
        Entrée: gameCanvas Canvas, root Tk, window Window, WINDOW_SIZE list[str]
                livesText StringVar, scoreText StringVar
        """
        self.lives -= 1
        self.livesText.set(str(self.lives))

        if self.lives == 0:
            messagebox.showinfo("Result", "You have lost!")
            # Reset game
            self.lives = 7
            self.score = 0
            self.livesText.set(str(self.lives))
            self.scoreText.set(str(self.score))
            gameCanvas.destroy()

    def modifyScore(self, newScore):
        """
        Met à jour le score
        Entrée: newScore int
        """
        self.score = newScore
        self.scoreText.set(str(self.score))

    def destroyBrique(self, game, brique, gameCanvas, root, window, WINDOW_SIZE, livesText, scoreText):
        """
        Supprime une brique et vérifie si le joueur a gagné
        Entrée: game Game, brique Brique, gameCanvas Canvas
                root Tk, window Window, WINDOW_SIZE list[str], livesText StringVar, scoreText StringVar
        """
        # Enlever la brique du canvas et de la liste
        brique.widget.destroy()
        if brique in self.briques:
            self.briques.remove(brique)

        # Victoire si plus de briques
        if len(self.briques) == 0:
            messagebox.showinfo("Result", "You have won!")
            self.lives = 7
            self.score = 0
            self.livesText.set(str(self.lives))
            self.scoreText.set(str(self.score))
            gameCanvas.destroy()
