from engine.core.game_object import *
import pygame

class OffGridObject(GameObject):
    def __init__(self, game, pos, id, tileset, z_pos):
        GameObject.__init__(self, game, z_pos)
        self.pos = pos
        self.id = id
        self.tileset = tileset
        self.init_z_pos = z_pos

    def update(self, scene):
        bounding_rect = self.game.assets[self.tileset][self.id].get_bounding_rect()
        self.z_pos = ((bounding_rect.bottom+self.pos[1]) / 100 + self.init_z_pos) 

    def render(self, scene):
        display_size = self.game.get_display_size()
        offset = self.game.rendering_offset
        for pos in [self.pos, (self.pos[0]+self.game.tile_size, self.pos[1]), (self.pos[0], self.pos[1]+self.game.tile_size), (self.pos[0]+self.game.tile_size, self.pos[1]+self.game.tile_size)]:
            if self.game.camera[0] - display_size[0]/2 - offset[0] <= pos[0] <= self.game.camera[0] + display_size[0]/2 + offset[0] and self.game.camera[1] - display_size[1]/2 - offset[1] <= pos[1] <= self.game.camera[1] + display_size[1]/2 + offset[1]:
                self.game.rendered_objects += 1
                self.game.render(self.game.assets[self.tileset][self.id], self.pos)
                return


