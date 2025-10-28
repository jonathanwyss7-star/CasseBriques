"""
TOUBI Mouaad et Jonathan Wyss
07/10/2025 08:00
Classe qui gère la raquette
"""

class Racket:
    def __init__(self, window_size):
        """Initialise la raquette"""
        self.color = 'blue'
        self.width = 100
        self.posx = int(window_size[0]) // 2 - 50  # Centre
        self.speed = 10
        self.offset = 0

    def move_left(self):
        """Déplace la raquette vers la gauche"""
        if self.posx > 0:
            self.posx -= self.speed

    def move_right(self):
        """Déplace la raquette vers la droite"""
        if self.posx + self.width < 980:
            self.posx += self.speed

    def moveRacket(self, racket, direction):
        """
        Déplace la raquette selon direction
        Entrée: racket Racket, direction int (0 = gauche, 1 = droite)
        """
        if direction == 0:
            racket.move_left()
        else:
            racket.move_right()

        # Mettre à jour le widget graphique
        racket.widget.place(x=racket.posx, y=580)
