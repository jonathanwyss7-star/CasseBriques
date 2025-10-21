class Racket:
    def __init__(self, window_size):
        self.offset = 0
        self.color = 'blue'
        self.width = 100
        self.posx = int(window_size[0]) // 2 - 50
        self.speed = 10

    def move_left(self):
        if  self.posx > 0:
            self.posx -= self.speed

    def move_right(self):
        if self.posx + self.width < 980:
            self.posx += self.speed

    #0 = left, 1 = right
    def moveRacket(self, racket, direction):
        if direction == 0:
            racket.move_left()
        else:
            racket.move_right()
        
        racket.widget.place(x=racket.posx, y=580)