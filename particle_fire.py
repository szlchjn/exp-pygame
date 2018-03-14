import pygame
import pygame.gfxdraw
import random

class Particle(object):
    def __init__(self, x, y, r):
        self.r = r
        self.x = x
        self.y = y
        self.alpha = random.randint(20, 255)
        self.temp = 255
        self.live = True

    def show(self):
        if self.live:
#            pygame.draw.circle(screen, [255, 255, 255], [self.x, self.y], self.r, 1)
            pygame.gfxdraw.filled_circle(screen, self.x, self.y, self.r, [255, self.temp, 0, self.alpha])

    def update(self):
        self.x = round(self.x + random.uniform(-3, 3))
        self.y = round(self.y + random.uniform(-4, -1))
        self.alpha -= random.randint(1, 3)
        if counter % 30 == 0:
            self.r -= 1
        if self.alpha <= 0:
            self.live = False
        if self.temp - 3 >= 0:
            self.temp -= 3

width, height = 400, 400

pygame.init()
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
counter = 0

particles = []

end = False
while not end:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            end = True

    screen.fill([25, 25, 25])

    for i in range(10):
       particles.append(Particle(200, 380, random.randint(8, 10)))
       particles.append(Particle(180, 370, random.randint(8, 10)))
       particles.append(Particle(220, 370, random.randint(8, 10)))


    for particle in particles[::-1]:
        if particle.live:
            particle.show()
            particle.update()
        else:
            particles.remove(particle)

    print(len(particles))
    clock.tick(60)
    pygame.display.flip()
    counter += 1

pygame.quit()