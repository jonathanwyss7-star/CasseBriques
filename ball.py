"""
TOUBI Mouaad et Jonathan Wyss
07/10/2025 08:00
Classe qui définit la balle
"""

import numpy as np
import random

class Ball:
    def __init__(self, window_size, speed, game):
        self.posx = int(window_size[0]) // 2 - 10
        self.posy = 300 
        self.radius = 5
        self.speed = speed
        self.angle = random.randint(45, 135)
        self.game = game
        
        # Vitesse en x et y calculée à partir de l'angle et de la vitesse
        self.speed_x = self.speed * np.cos(self.angle)
        self.speed_y = self.speed * np.sin(self.angle)
        
    # Déplacement de la balle
    def move(self, root, game, window, gameCanvas, racket, briques, ball, window_size, livesText, scoreText):
        self.posx += self.speed_x
        self.posy += self.speed_y

        # Si la balle tombe sous l'écran, retirer une vie
        if self.posy > 608:
            game.removeLife(gameCanvas, root, window, window_size, livesText, scoreText)
            self.widget.destroy()
            window.tkPlaceBall(game, root, window, window_size, gameCanvas, briques, livesText, scoreText, fps=250)
            return True

        # Rebond sur la raquette
        ball_edge_x = self.posx + self.radius
        if (565 < self.posy < 590) and self.speed_y > 0:
            if racket.posx <= ball_edge_x <= (racket.posx + racket.width):
                self.speed_y *= -1

        # Rebond sur les bords de la fenêtre
        if self.posx <= 0 or self.posx >= 980 - self.radius * 2:
            self.speed_x *= -1
        if self.posy <= 0 or self.posy >= 620 - self.radius * 2:
            self.speed_y *= -1

        # Collision avec les briques
        for brique in briques:
            ball_left = ball.posx
            ball_right = ball.posx + 2 * ball.radius
            ball_top = ball.posy
            ball_bottom = ball.posy + 2 * ball.radius

            brick_left = brique.posx
            brick_right = brique.posx + brique.width
            brick_top = brique.posy
            brick_bottom = brique.posy + 20

            if (ball_right > brick_left and
                ball_left < brick_right and
                ball_bottom > brick_top and
                ball_top < brick_bottom):

                # Déterminer la direction du rebond
                overlap_left = ball_right - brick_left
                overlap_right = brick_right - ball_left
                overlap_top = ball_bottom - brick_top
                overlap_bottom = brick_bottom - ball_top
                min_overlap = min(overlap_left, overlap_right, overlap_top, overlap_bottom)

                if min_overlap == overlap_top or min_overlap == overlap_bottom:
                    self.speed_y *= -1
                else:
                    self.speed_x *= -1

                # Détruire la brique et mettre à jour le score
                briques.remove(brique)
                game.destroyBrique(game, brique, gameCanvas, root, window, window_size, livesText, scoreText)
                game.score += 1
                game.modifyScore(game.score)

                break

        return False
