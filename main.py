"""
    heavily based on this example: https://gamedevacademy.org/a-comprehensive-introduction-to-pygame/
"""

import pygame
import sys
import random

pygame.init()
 
BACKGROUND_COLOUR = (0, 0, 0) 
WINDOW_SIZE = (700,400)
screen_options = 0
GRAVITY = 980

#advanced - fullscreen - query the modes and choose the highest resolution one
#print(pygame.display.Info())
# modes = sorted(pygame.display.list_modes())
# screen_options = pygame.FULLSCREEN|pygame.DOUBLEBUF|pygame.HWSURFACE
# WINDOW_SIZE = modes[-1]

screen = pygame.display.set_mode(WINDOW_SIZE, screen_options)

screenrect = pygame.Rect((0,0),WINDOW_SIZE)       # the rectangle for screen space
cullrect = screenrect.inflate(50, 50)             # the rectangle for 'culling' entities

pygame.display.set_caption("Blob launcher")
 
clock = pygame.time.Clock()

game_time = 0  # Millisecond counter

all_sprites = pygame.sprite.Group()

class Entity(pygame.sprite.Sprite):
    """Inherited by any object in the game."""
    def __init__(self, x, y, width, height):
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect(x, y, width, height)
        all_sprites.add(self)
    def update(self, dt):
        pass    # do nothing
    def remove(self):
        all_sprites.remove(self)

class Blob(Entity):
    """
    A green blob, start with a random speed and direction, falls under gravity
    doesn't collide or bounce, dies when it is too far off-screen
    """
    def __init__(self, x, y, width, height):
        super(Blob, self).__init__(x, y, width, height)
        self.image = pygame.Surface(self.rect.size)
        self.image.fill((0,255,0))
        self.velocity = (random.randrange(-200, 200),random.randrange(-200,0))
    def update(self, dt):
        self.rect.x += self.velocity[0]*dt
        self.rect.y += self.velocity[1]*dt
        self.velocity = (self.velocity[0], self.velocity[1]+GRAVITY*dt)
        if not cullrect.contains(self.rect):
            self.remove()

class Counter(Entity):
    def __init__(self):
        super(Counter, self).__init__(0,0,200,200)
        self.font = pygame.font.Font(None, 50)
        self.lastcount = None
        self.update(0)
        self.rect = self.image.get_rect()

    def update(self, dt):
        if len(all_sprites) != self.lastcount:
            # only draw the text if it has changed (an optimisation)
            self.lastcount = len(all_sprites)
            msg = "Sprites: %d" % self.lastcount
            self.image = self.font.render(msg, 0, pygame.Color("white"))

Counter()

exit = False
while not exit:
    dt = clock.get_time()
    game_time += dt

    # Listen for events - see http://www.pygame.org/docs/ref/event.html
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit = True
        elif event.type == pygame.KEYDOWN:
            if event.key==27: #ESC
                exit = True
            print(event)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            a = Blob(event.pos[0], event.pos[1], 20, 20)
            #print(event)

    for sprite in all_sprites:
        sprite.update(dt/1000.0)

    screen.fill(BACKGROUND_COLOUR)
    all_sprites.draw(screen)

    pygame.display.flip()
 
    clock.tick(20)

pygame.quit()
sys.exit()
