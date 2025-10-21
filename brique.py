import tkinter as tk
from tkinter import messagebox 
import numpy as np
import random
from time import sleep

class Brique:
    def __init__(self, window_size, posx=10, posy=10):
        self.offset = 0
        self.color = 'red'
        self.width = int(window_size[0]) / 10
        self.posx = posx
        self.posy = posy
        self.widget = None

    def destroy(self):
        self.widget.destroy()
