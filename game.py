from timeit import default_timer as timer

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

    def removeLife(self):
        self.lives -= 1
        self.livesText.set(str(self.lives))

        if self.lives == 0:
            self.tkWindow.quit()

    def modifyScore(self, newScore):
        self.score = newScore
        self.scoreText.set(str(self.score))