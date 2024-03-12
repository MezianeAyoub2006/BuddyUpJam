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
        mapped_key_move_left = keys[pygame.K_LEFT] or keys[pygame.K_a]
        mapped_key_move_right = keys[pygame.K_RIGHT] or keys[pygame.K_d]
        mapped_key_move_up = keys[pygame.K_UP] or keys[pygame.K_w]
        mapped_key_move_down = keys[pygame.K_DOWN] or keys[pygame.K_s]
        if (mapped_key_move_left and mapped_key_move_right) or (mapped_key_move_up and mapped_key_move_down):
            self.stop = True
        elif (mapped_key_move_down or mapped_key_move_up) and mapped_key_move_left:
            self.dir = "left"
            self.flip = False
        elif (mapped_key_move_down or mapped_key_move_up) and mapped_key_move_right:
            self.dir = "right"
            self.flip = True
        elif mapped_key_move_up:
            self.dir = "up"
        elif mapped_key_move_down:
            self.dir = "down"
        elif mapped_key_move_left:
            self.dir = "left"
            self.flip = False
        elif mapped_key_move_right:
            self.dir = "right"
            self.flip = True
        if mapped_key_move_up:
            self.go_up = True
        if mapped_key_move_down:
            self.go_up = False
        self.vel = [(int(mapped_key_move_right) - int(mapped_key_move_left))*self.speed,(int(mapped_key_move_down) - int(mapped_key_move_up))*self.speed]
        if self.stop : self.vel = [0, 0]
        if abs(self.vel[0]) == abs(self.vel[1]) != 0:
            self.vel[0] *= (1/1.41)
            self.vel[1] *= (1/1.41)

        if (mapped_key_move_down or mapped_key_move_left or mapped_key_move_right or mapped_key_move_up) and not self.stop:
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
