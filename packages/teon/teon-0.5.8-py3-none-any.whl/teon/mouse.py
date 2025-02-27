import pygame

from teon.attributes import MousePosition,MouseWPosition
from teon.functions import scale_def,_repair_vec2

class Mouse:
    def __init__(self):
        self.wheel = Wheel()
        self.wheel.up = False
        self.wheel.down = False

        self.position = _repair_vec2((0,0))
        self.world_position = _repair_vec2((0,0))

    def _init(self,core,**kwargs):
        self._core = core

        self.position = MouseWPosition((pygame.mouse.get_pos()[0] - self._core.__class__._offput[0]) / self._core.window.size.x,(pygame.mouse.get_pos()[1] - self._core.__class__._offput[1]) / self._core.window.size.y)
        self.world_position = MousePosition(self._core.camera.position.x + pygame.mouse.get_pos()[0] - self._core.__class__._offput[0],self._core.camera.position.y + pygame.mouse.get_pos()[1] - self._core.__class__._offput[1])

        self._visible = kwargs.get("mouse_visible",True)

        pygame.mouse.set_visible(self.visible)

    def _update(self):
        self.position._x = round((pygame.mouse.get_pos()[0] - self._core.__class__._offput[0]) / self._core.__class__._win_screen_size[0],3)
        self.position._y = round(((pygame.mouse.get_pos()[1] - self._core.__class__._offput[1]) / self._core.__class__._win_screen_size[1]),3)
        self.world_position._x = int((self._core.camera.position.x + pygame.mouse.get_pos()[0] - self._core.__class__._offput[0]) / scale_def()) - 500
        self.world_position._y = int((self._core.camera.position.y + pygame.mouse.get_pos()[1] - self._core.__class__._offput[1]) / scale_def()) - 300
    
    @property
    def visible(self):
        return self._visible
    
    @visible.setter
    def visible(self,value):
        self._visible = value
        pygame.mouse.set_visible(self._visible)
    
    def __repr__(self):
        return f"Position:{self.position},World Position:{self.world_position},Wheel:({self.wheel.up},{self.wheel.down}),Visible:{self.visible}"

class Wheel:
    def __init__(self):
        self.up = False
        self.down = False

    def __repr__(self):
        return f"Up: {self.up},Down: {self.down}"
    
minstance = Mouse()