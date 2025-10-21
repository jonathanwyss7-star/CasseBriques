import numpy as np
import random
from timeit import default_timer as timer

class Ball:
    def __init__(self, window_size, speed, game):
        self.posx = int(window_size[0]) // 2 - 10
        self.posy = 300 
        self.radius = 5
        self.speed = speed
        self.angle = random.randint(45, 135)
        self.game = game
        
        self.speed_x = self.speed * np.cos(self.angle)
        self.speed_y = self.speed * np.sin(self.angle)
        
    def move(self, game, racket, briques, ball):

        self.posx += self.speed_x
        self.posy += self.speed_y

        if self.posy > 608:
            game.removeLife()
            self.speed_y *= -1

        """
        ball_edge_x = self.posx + self.radius
        if 565 < self.posy < 590:
            if racket.posx <= ball_edge_x <= racket.posx + racket.width:
                self.speed_y *= -1
            elif (racket.posx - 5) <= ball_edge_x <= (racket.posx + 5) or (racket.posx + racket.width - 5) <= ball_edge_x <= (racket.posx + racket.width + 5):
                self.speed_x *= -1
        """
        
        ball_edge_x = self.posx + self.radius
        if (565 < self.posy < 590) and self.speed_y >0:
            if (racket.posx) <= ball_edge_x <= (racket.posx + racket.width):
                self.speed_y *= -1

        if self.posx <= 0 or self.posx >= 980 - self.radius * 2:
            self.speed_x *= -1
        if self.posy <= 0 or self.posy >= 620 - self.radius * 2:
            self.speed_y *= -1

        for brique in briques:

            #...
            ball_left = ball.posx
            ball_right = ball.posx + 2 * ball.radius
            ball_top = ball.posy
            ball_bottom = ball.posy + 2 * ball.radius

            #...
            brick_left = brique.posx
            brick_right = brique.posx + brique.width
            brick_top = brique.posy
            brick_bottom = brique.posy + 20

            #...

            if (ball_right > brick_left and
                ball_left < brick_right and
                ball_bottom > brick_top and
                ball_top < brick_bottom):

                overlap_left = ball_right - brick_left
                overlap_right = brick_right - ball_left
                overlap_top = ball_bottom - brick_top
                overlap_bottom = brick_bottom - ball_top

                min_overlap = min(overlap_left, overlap_right, overlap_top, overlap_bottom)

                if min_overlap == overlap_top or min_overlap == overlap_bottom:
                    # ...
                    ball.speed_y *= -1
                else:
                    # ...
                    ball.speed_x *= -1

                brique.destroy()
                briques.remove(brique)
                game.score += 5

                game.modifyScore(game.score)

                break