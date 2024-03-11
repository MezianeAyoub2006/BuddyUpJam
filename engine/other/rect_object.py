from engine.core.game_object import *

class RectObject(GameObject):
    def __init__(self, game, rect, z_pos, collide = False, show = False, color = (255,0,0), alpha = 125):
        GameObject.__init__(self, game, z_pos)
        self.rect = rect
        self.collide = collide
        self.show = show
        self.color = color
        self.alpha = alpha
        self.tags.append("@Rect")
    def render(self, scene):
        if self.show:
            self.game.render_rect(self.rect, self.color, alpha=self.alpha)