"""
TOUBI Mouaad et Jonathan Wyss
07/10/2025 08:00
Script principal du jeu
"""

import tkinter as tk
import racket
import window as windowClass

root = tk.Tk()

lives = 7
livesText = tk.StringVar(root, value=str(lives))
scoreText = tk.StringVar(root, value=str(0))

WINDOW_SIZE = ['1000', '700']

# Création de l'objet Window
window = windowClass.Window()
window.tkWindow = root

# Initialise le jeu et Tkinter
root, game = window.tkInitTkinter(root, WINDOW_SIZE, 'Casse brique', 'black', lives, livesText, 0, scoreText)

# Menu de départ (Start / Quit)
window.tkPlaceStartMenu(root, game, window, WINDOW_SIZE, livesText, scoreText)

root.mainloop()
