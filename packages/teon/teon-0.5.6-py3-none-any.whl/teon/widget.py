
from teon.entity import Entity
from teon.functions import _repair_vec2,mouse_pressed,scale_def
from teon.other import Timer

from teon.attributes import WidgetPosition

from teon.core import Teon

class Widget(Entity):
    def __init__(self,**kwargs):
        self.is_ui = True

        self.core = Teon
        self._anchor = kwargs.get("anchor","center")
        self.window_anchor = kwargs.get("window_anchor",None)
        
        super().__init__(**kwargs)

        

        
        
        self.held_time = kwargs.get("held_time",200)
        self._held_timer = Timer(self.held_time)
        self._held_timer.activate()
        
        self.collidable = False

        self.hovered = False
        self.held = False

        self._anchor_list = ["topleft","midleft","bottomleft","midtop","center","midbottom","topright","midright","bottomright"]

        self.anchor = self._anchor
        
        self.rposition = WidgetPosition(0,0,self)

        self.position = _repair_vec2(kwargs.get("position",(0,0)))
        
    @property
    def position(self):
        return self.rposition

    @position.setter
    def position(self,position):
        position = _repair_vec2(position)
        self.rposition.x = position.x
        self.rposition.y = position.y

    def _get_pos(self,pos):
        pos = _repair_vec2(pos)
        
        x = self.core._instances[0].window.size.x
        y = self.core._instances[0].window.size.y
        min_size = min(x,y)

        if self.core._instances[0].aspect_borders:
            return (pos.x * self.core._win_screen_size[0] + self.core._offput[0],pos.y * self.core._win_screen_size[1] + self.core._offput[1])
        elif self.window_anchor == "topleft":
            return (pos.x * min_size,pos.y * min_size)
        elif self.window_anchor == "midtop":
            return (pos.x * min_size + x / 2,pos.y * min_size)
        elif self.window_anchor == "topright":
            return (pos.x * min_size + x,pos.y * min_size)
        elif self.window_anchor == "midright":
            return (pos.x * min_size + x,pos.y * min_size + y / 2)
        elif self.window_anchor == "bottomright":
            return (pos.x * min_size + x,pos.y * min_size + y)
        elif self.window_anchor == "midbottom":
            return (pos.x * min_size + x / 2,pos.y * min_size + y)
        elif self.window_anchor == "bottomleft":
            return (pos.x * min_size,pos.y * min_size + y)
        elif self.window_anchor == "midleft":
            return (pos.x * min_size,pos.y * min_size + y / 2)
        elif self.window_anchor == "center":
            return (pos.x * min_size + x / 2,pos.y * min_size + y / 2)
        elif self.window_anchor == None:
            return (pos.x * x,pos.y * y)
        
    @property
    def anchor(self):
        return self._anchor

    @anchor.setter
    def anchor(self,anchor):
        if self.is_ui:
            if anchor in self._anchor_list:
                self._anchor = anchor
                if self.core._instances[0].aspect_borders:
                    if self._anchor == "topleft":
                        self.rect.center = self._get_pos((self.position.x + self.rect.width / 2 / self.core._win_screen_size[0],self.position.y + self.rect.height / 2 / self.core._win_screen_size[1]))
                        return
                    elif self._anchor == "center":
                        self.rect.center = self._get_pos(self.position)
                        return
                    elif self._anchor == "midright":
                        self.rect.center = self._get_pos((self.position.x - self.rect.width / 2 / self.core._win_screen_size[0],self.position.y))
                        return
                    elif self._anchor == "midleft":
                        self.rect.center = self._get_pos((self.position.x + self.rect.width / 2 / self.core._win_screen_size[0],self.position.y))
                        return
                    elif self._anchor == "midtop":
                        self.rect.center = self._get_pos((self.position.x,self._position.y + self.rect.height / 2 / self.core._win_screen_size[1]))
                        return
                    elif self._anchor == "midbottom":
                        self.rect.center = self._get_pos((self.position.x,self._position.y - self.rect.height / 2 / self.core._win_screen_size[1]))
                        return
                    elif self._anchor == "bottomleft":
                        self.rect.center = self._get_pos((self.position.x + self.rect.width / 2 / self.core._win_screen_size[0],self.position.y - self.rect.height / 2 / self.core._win_screen_size[1]))
                        return
                    elif self._anchor == "topright":
                        self.rect.center = self._get_pos((self.position.x - self.rect.width / 2 / self.core._win_screen_size[0],self.position.y + self.rect.height / 2 / self.core._win_screen_size[1]))
                        return
                    elif self._anchor == "bottomright":
                        self.rect.center = self._get_pos((self.position.x - self.rect.width / 2 / self.core._win_screen_size[0],self.position.y - self.rect.height / 2 / self.core._win_screen_size[1]))
                        return
                else:
                    if self._anchor == "topleft":
                        self.rect.center = self._get_pos((self.position.x + self.rect.width / min(self.core._instances[0].window.size.x,self.core._instances[0].window.size.y) / 2,self.position.y + self.rect.height / min(self.core._instances[0].window.size.x,self.core._instances[0].window.size.y) / 2))
                        return
                    elif self._anchor == "center":
                        self.rect.center = self._get_pos(self.position)
                        return
                    elif self._anchor == "midright":
                        self.rect.center = self._get_pos((self.position.x - self.rect.width / min(self.core._instances[0].window.size.x,self.core._instances[0].window.size.y) / 2,self.position.y))
                        return
                    elif self._anchor == "midleft":
                        self.rect.center = self._get_pos((self.position.x + self.rect.width / min(self.core._instances[0].window.size.x,self.core._instances[0].window.size.y) / 2,self.position.y))
                        return
                    elif self._anchor == "midtop":
                        self.rect.center = self._get_pos((self.position.x,self.position.y + self.rect.height / min(self.core._instances[0].window.size.x,self.core._instances[0].window.size.y) / 2))
                        return
                    elif self._anchor == "midbottom":
                        self.rect.center = self._get_pos((self.position.x,self.position.y - self.rect.height / min(self.core._instances[0].window.size.x,self.core._instances[0].window.size.y) / 2))
                        return
                    elif self._anchor == "bottomleft":
                        self.rect.center = self._get_pos((self.position.x + self.rect.width / min(self.core._instances[0].window.size.x,self.core._instances[0].window.size.y) / 2,self.position.y - self.rect.height / min(self.core._instances[0].window.size.x,self.core._instances[0].window.size.y) / 2))
                        return
                    elif self._anchor == "topright":
                        self.rect.center = self._get_pos((self.position.x - self.rect.width / min(self.core._instances[0].window.size.x,self.core._instances[0].window.size.y) / 2,self.position.y + self.rect.height / min(self.core._instances[0].window.size.x,self.core._instances[0].window.size.y) / 2))
                        return
                    elif self._anchor == "bottomright":
                        self.rect.center = self._get_pos((self.position.x - self.rect.width / min(self.core._instances[0].window.size.x,self.core._instances[0].window.size.y) / 2,self.position.y - self.rect.height / min(self.core._instances[0].window.size.x,self.core._instances[0].window.size.y) / 2))
                        return
            else:
                print("The anchor provided doesn't represent a point on the widget collider, for more help take a look at the Teon documentation.")

    def _get_held(self):
        if mouse_pressed()[0] and self.hovered:

            self._held_timer.update()
            if not self._held_timer.active:
                self.held = True
            else:
                self.held = False
        
        else:
            self._held_timer.activate()
            self.held = False

    def _update(self):
        super()._update()
        self.hitbox.update()
        self._occlusion_rect.center = self.rect.center

        self._update_colliders()
        self.hovered = self.collider.hovered
        self._get_held()