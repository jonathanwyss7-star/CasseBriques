from timeit import default_timer as timer
from tkinter import messagebox
import tkinter as tk

class Game:
    def __init__(self, window_size, tkWindow, title, lives, livesText, score, scoreText):
        self.window_size = window_size
        self.tkWindow = tkWindow
        self.title = title
        self.lives = lives
        self.livesText = livesText
        self.score = score
        self.scoreText = scoreText
        self.racket = None
        self.briques = None

        self.ballColor = ["red", "green"]
        self.currentBallColor = "blue"

    def removeLife(self, gameCanvas, root, window, WINDOW_SIZE, livesText, scoreText):
        self.lives -= 1
        self.livesText.set(str(self.lives))

        if self.lives == 0:
            messagebox.showinfo("Result", "You have won!")
            self.lives = 7
            self.score = 0
            self.livesText.set(str(self.lives))
            self.scoreText.set(str(self.score))
            gameCanvas.destroy()
        

    def modifyScore(self, newScore):
        self.score = newScore
        self.scoreText.set(str(self.score))

    def destroyBrique(self, game,  brique, gameCanvas, root, window, WINDOW_SIZE, livesText, scoreText):
        # remove the brick widget
        brique.widget.destroy()
        if brique in self.briques:
            self.briques.remove(brique)

        # check if all bricks are destroyed
        if len(self.briques) == 0:
            messagebox.showinfo("Result", "You have won!")
            self.lives = 7
            self.score = 0
            self.livesText.set(str(self.lives))
            self.scoreText.set(str(self.score))
            gameCanvas.destroy()
