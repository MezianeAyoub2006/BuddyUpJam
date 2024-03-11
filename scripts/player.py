from engine import *
import pygame

class Player(Entity, Animated):
    def __init__(self, game, pos):
        Entity.__init__(self, game, pos, (12, 8), (5,11), z_pos = 10)
        Animated.__init__(self, game.assets["player_sprite"])
        self.vel[0] = 2
        self.collide = True
        self.dir = "up"
        self.flip = False
        self.go_up = True
        self.speed = 2
        self.move = False
        self.tags.append("@Player")
        self.tags.append("#shadow")
        self.shadow_offset = (-6, 0)

    def update(self, scene):
        super().update(scene)
        self.z_pos = (self.rect().bottom / 100)
        self.movements()

    def movements(self):
        self.stop = False
        keys = self.game.get_pressed()
        if (keys[pygame.K_LEFT] and keys[pygame.K_RIGHT]) or (keys[pygame.K_UP] and keys[pygame.K_DOWN]):
            self.stop = True
        elif (keys[pygame.K_DOWN] or keys[pygame.K_UP]) and keys[pygame.K_LEFT]:
            self.dir = "left"
            self.flip = False
        elif (keys[pygame.K_DOWN] or keys[pygame.K_UP]) and keys[pygame.K_RIGHT]:
            self.dir = "right"
            self.flip = True
        elif keys[pygame.K_UP]:
            self.dir = "up"
        elif keys[pygame.K_DOWN]:
            self.dir = "down"
        elif keys[pygame.K_LEFT]:
            self.dir = "left"
            self.flip = False
        elif keys[pygame.K_RIGHT]:
            self.dir = "right"
            self.flip = True
        if keys[pygame.K_UP]:
            self.go_up = True
        if keys[pygame.K_DOWN]:
            self.go_up = False
        self.vel = [(int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT]))*self.speed,(int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP]))*self.speed]
        if self.stop : self.vel = [0, 0]
        if abs(self.vel[0]) == abs(self.vel[1]) != 0:
            self.vel[0] *= (1/1.41)
            self.vel[1] *= (1/1.41)

        if (keys[pygame.K_DOWN] or keys[pygame.K_LEFT] or keys[pygame.K_RIGHT] or keys[pygame.K_UP]) and not self.stop:
            self.move = True
        else:
            self.move = False

        self.animate(self.game.get_dt())
        self.animation_cycle()


    def animation_cycle(self):
        if self.move:
            self.set_animation_speed(0.3)
            if self.go_up:
                self.set_animation(1)
            else:
                self.set_animation(0)    
        else:
            self.set_animation_speed(0.05)
            if self.go_up:
                self.set_animation(3)
            else:
                self.set_animation(2)

    def render(self, scene):
        self.image = pygame.transform.flip(self.animations[self.animation][int(self.animation_cursor)-1], not self.flip, False)
        Entity.render(self)
