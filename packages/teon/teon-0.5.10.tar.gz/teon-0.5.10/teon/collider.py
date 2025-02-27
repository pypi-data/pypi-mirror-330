import pygame

from teon.functions import scale_def,_repair_vec2

class SquareCollider(pygame.Rect):
    def __init__(self,parent,position_offset,scale_offset,**kwargs):
        super().__init__(parent.rect.topleft[0] + (position_offset[0] * scale_def()),parent.rect.topleft[1] + (position_offset[1] * scale_def()),parent.rect.width * scale_offset[0],parent.rect.height * scale_offset[1])
        from teon.core import get_main_class
        self.core = get_main_class()
        self.position_offset = _repair_vec2(position_offset)
        self.scale_offset = _repair_vec2(scale_offset)
        self.parent = parent
        self.shape = "square"
        self.name = kwargs.get("name","")
        self.visible = kwargs.get("visible",False)
        self.collidable = kwargs.get("collidable",True)
        self.scalable = kwargs.get("scalable",False)
        self.color = kwargs.get("color",(255,0,0))

        self._scale_def = self.parent._scale_def

    def _upt_scale_def(self,scale_def):
        self._scale_def = scale_def

    @property
    def hovered(self):
        if self.parent.is_ui:
            return self.collidepoint(self.core.mouse.position.x * self.core.__class__._win_screen_size[0] + self.core.__class__._offput[0],self.core.mouse.position.y * self.core.__class__._win_screen_size[1] + self.core.__class__._offput[1])
        return self.collidepoint((pygame.mouse.get_pos()[0] + self.core.camera.position.x * 2 - 500 * self._scale_def,pygame.mouse.get_pos()[1] + self.core.camera.position.y * 2 - 300 * self._scale_def))

    def update(self):
        if not self.scalable:
            self.topleft = (self.parent.rect.topleft[0] + (self.position_offset[0] * self._scale_def) + self.parent._pos.x,self.parent.rect.topleft[1] + (self.position_offset[1] * self._scale_def) + self.parent._pos.y)
        else:
            self.topleft = (self.parent.rect.topleft[0] + (self.position_offset[0] * self._scale_def * self.parent.scale.x) + self.parent._pos.x,self.parent.rect.topleft[1] + (self.position_offset[1] * self._scale_def * self.parent.scale.y) + self.parent._pos.y)
        self.width,self.height = (self.parent.rect.width * self.scale_offset[0],self.parent.rect.height * self.scale_offset[1])

class CircleCollider(pygame.Rect):
    def __init__(self,parent,position_offset,radius,**kwargs):
        super().__init__(parent.rect.topleft[0] + (position_offset[0] * scale_def()),parent.rect.topleft[1] + (position_offset[1] * scale_def()),scale_def() * radius * 2,radius * scale_def() * 2)
        from teon.core import get_main_class
        self.core = get_main_class()
        self.position_offset = _repair_vec2(position_offset)
        self.parent = parent
        self.radius = radius
        self._radius = 0
        self.shape = "circle"
        self.name = kwargs.get("name","")
        self.visible = kwargs.get("visible",False)
        self.collidable = kwargs.get("collidable",True)
        self.scalable = kwargs.get("scalable",False)
        self.color = kwargs.get("color",(255,0,0))


    @property
    def hovered(self):
        if self.parent.is_ui:
            return self.collidepoint(self.core.mouse.position.x * self.core.__class__._win_screen_size[0] + self.core.__class__._offput[0],self.core.mouse.position.y * self.core.__class__._win_screen_size[1] + self.core.__class__._offput[1])
        return ((pygame.mouse.get_pos()[0] + self.core.camera.position.x * 2 - 500 * scale_def()) - self.centerx)**2 + ((pygame.mouse.get_pos()[1] + self.core.camera.position.y * 2 - 600 * scale_def()) - self.centery)**2 <= (self._radius)**2

    def update(self):
        self.center = (self.parent.rect.topleft[0] + (self.position_offset[0] * scale_def()) + self.parent._pos.x + self.parent.rect.width / 2,self.parent.rect.topleft[1] + (self.position_offset[1] * scale_def()) + self.parent._pos.y + self.parent.rect.height / 2)
        self._radius = self.radius * scale_def() * 50
        if self.scalable:
            self._radius = self.radius * scale_def() * 50 * ((self.parent.scale.x + self.parent.scale.y) / 2)
        self.width,self.height = (self.radius * scale_def() * 50,self.radius * scale_def() * 50)