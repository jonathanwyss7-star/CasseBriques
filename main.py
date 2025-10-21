import tkinter as tk
import racket
import window as windowClass

root = tk.Tk()
lives = 3
livesText = tk.StringVar(root, value=str(lives))
scoreText = tk.StringVar(root, value=str(0))

WINDOW_SIZE = ['1000', '700']

#...
window = windowClass.Window()
window.tkWindow = root

#...
root, game = window.tkInitTkinter(root, WINDOW_SIZE, 'Casse brique', 'black', lives, livesText, 0, scoreText)

#...
window.tkPlaceScore(root, scoreText)
window.tkPlaceLives(root, livesText)

window.tkPlaceStartMenu(root, WINDOW_SIZE)

gameCanvas = window.tkPlaceGameCanvas(root, WINDOW_SIZE)

racket = window.tkPlaceRacket(gameCanvas, WINDOW_SIZE)
game.racket = racket

briques = window.tkPlaceAllBriques(gameCanvas, 7, 7, 20, WINDOW_SIZE)
game.briques = briques

root.bind("<Left>", lambda event: racket.moveRacket(racket, 0))
root.bind("<Right>", lambda event: racket.moveRacket(racket, 1))

ball = window.tkPlaceBall(game, gameCanvas, WINDOW_SIZE, fps=150)

root.mainloop()