import tkinter as tk
import funcs as f

root = tk.Tk()
lives = 100
livesText = tk.StringVar(root, value=str(lives))

WINDOW_SIZE = ['1000', '700']

root, game = f.tkInitTkinter(root, WINDOW_SIZE, 'Casse brique', 'black', lives, livesText)


f.tkPlaceScore(root)
f.tkPlaceLives(root, livesText)

f.tkPlaceStartMenu(root, WINDOW_SIZE)

gameCanvas = f.tkPlaceGameCanvas(root, WINDOW_SIZE)

racket = f.tkPlaceRacket(gameCanvas, WINDOW_SIZE)

root.bind("<Left>", lambda event: f.tkMoveRacket(racket, 0))
root.bind("<Right>", lambda event: f.tkMoveRacket(racket, 1))

ball = f.tkPlaceBall(game, gameCanvas, WINDOW_SIZE, racket, fps=100)

root.mainloop()