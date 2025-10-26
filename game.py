from timeit import default_timer as timer
from tkinter import messagebox

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
            answer = messagebox.askyesno("Result", "You have lost! Do you want to play again?")
            if answer:
                try:
                    gameCanvas.destroy()
                except:
                    pass
                self.lives = 10
                self.score = 0
                self.livesText.set(str(self.lives))
                self.scoreText.set(str(self.score))
                window.makeGameWindow(root, self, window, WINDOW_SIZE, livesText, scoreText)
            else:
                try:
                    gameCanvas.destroy()
                except:
                    pass
        

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
            answer = messagebox.askyesno("Result", "You have won! Do you want to play again?")
            if answer:
                # reset stats
                self.lives = 50000  # your original starting lives
                self.score = 0
                self.livesText.set(str(self.lives))
                self.scoreText.set(str(self.score))
                # schedule new game
                print(111111111111111)
                root.after(0, lambda: window.makeGameWindow(root, self, window, WINDOW_SIZE, livesText, scoreText))
                print(22222222222222)

                # stop any running ball loop
                if hasattr(self, 'ball') and hasattr(self.ball, 'after_id'):
                    root.after_cancel(self.ball.after_id)
                gameCanvas.destroy()
            else:
                # stop any running ball loop
                if hasattr(self, 'ball') and hasattr(self.ball, 'after_id'):
                    root.after_cancel(self.ball.after_id)
                gameCanvas.destroy()
