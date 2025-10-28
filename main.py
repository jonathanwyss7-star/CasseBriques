"""
todo: entetes fichiers, commentaires,  readme etc...
"""

import tkinter as tk
import racket
import window as windowClass
from timeit import default_timer as timer

root = tk.Tk()
lives = 7
livesText = tk.StringVar(root, value=str(lives))
scoreText = tk.StringVar(root, value=str(0))

WINDOW_SIZE = ['1000', '700']

#...
window = windowClass.Window()
window.tkWindow = root

#...
root, game = window.tkInitTkinter(root, WINDOW_SIZE, 'Casse brique', 'black', lives, livesText, 0, scoreText)

#...
window.tkPlaceStartMenu(root, game, window, WINDOW_SIZE, livesText, scoreText)

root.mainloop()