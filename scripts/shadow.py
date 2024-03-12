from engine import *

class Shadow(GameObject):
    def __init__(self, game, z_pos, apply_speed=True):
        GameObject.__init__(self, game, z_pos)
        self.apply_speed = apply_speed
    def render(self, scene):
        objs = scene.get_objects_by_tags("#shadow")
        for object in objs:
            if self.apply_speed:
                position = (object.pos[0] + object.shadow_offset[0] + object.vel[0], object.pos[1] + object.shadow_offset[1] + object.vel[1])
            else:
                position = (object.pos[0] + object.shadow_offset[0], object.pos[1] + object.shadow_offset[1])
            self.game.render(self.game.assets["shadow"], position)