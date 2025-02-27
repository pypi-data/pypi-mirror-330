from teon.other import Vec2
from teon.functions import scale_def
import pygame,teon
class Position:
    def __init__(self, x=0, y=0, entity=None):
        from teon.core import Teon
        self.core = Teon
        self._x = x
        self._y = y
        self._entity = entity

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        self._x = value
        self._entity.rect.centerx = self._x * scale_def() + self.core._offput[0]
        self._entity.anchor = self._entity._anchor
        self._entity.hitbox.update()
        self._entity._update_colliders()
        if self._entity._parent != None:
            self._entity._parent_offset.x = self._x - self._entity.parent.position.x

    def full(self):
        return Vec2(self._x * scale_def() + self.core._offput[0],self._y * scale_def() + self.core._offput[1])

    def _set_x(self,x):
        self._x = x
        self._entity.rect.centerx = self._x * scale_def() + self.core._offput[0]
        self._entity.anchor = self._entity._anchor
        if hasattr(self._entity,"_collide"):
            self._entity._collide()

    def _set_y(self,y):
        self._y = y
        self._entity.rect.centery = self._y * scale_def() + self.core._offput[1]
        self._entity.anchor = self._entity._anchor
        if hasattr(self._entity,"_collide"):
            self._entity._collide()
        
    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self._y = value
        self._entity.rect.centery = self._y * scale_def() + self.core._offput[1]
        self._entity.anchor = self._entity._anchor
        self._entity.hitbox.update()
        self._entity._update_colliders()
        if self._entity._parent != None:
            self._entity._parent_offset.y = self._y - self._entity.parent.position.y

    def __add__(self,value):
        return Vec2(self.x + value[0],self.y + value[1])
    
    def __sub__(self,value):
        return Vec2(self.x - value[0],self.y - value[1])

    def __iadd__(self, value):
        dx, dy = value
        
        if isinstance(dx,Vec2):
            dx = dx.x
        if isinstance(dy,Vec2):
            dy = dy.y

        self.x = self._x + dx
        self.y = self._y + dy

        self._entity.hitbox.update()
        self._entity._update_colliders()

        return self

    def __isub__(self, value):
        dx,dy = value
        
        if isinstance(dx,Vec2):
            dx = dx.x
        if isinstance(dy,Vec2):
            dy = dy.y

        self.x = self._x - dx
        self.y = self._y - dy

        self._entity.hitbox.update()
        self._entity._update_colliders()

        return self
    
    def __repr__(self):
        return f"({self._x},{self._y})"
    
    def __getitem__(self,key):
        return (self.x,self.y)[key]
    
class CoScale:
    def __init__(self, x=0, y=0, entity=None):
        self._x = x
        self._y = y
        self._entity = entity

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        self._x = value
        self._entity.rect.width = self._x * scale_def() * self._entity._default_scale_value.x
        self._entity.anchor = self._entity._anchor

    def _set_x(self,x):
        self._x = x

    def _set_y(self,y):
        self._y = y
        
    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self._y = value
        self._entity.rect.height = self._y * scale_def() * self._entity._default_scale_value.y
        self._entity.anchor = self._entity._anchor

    def __iadd__(self, value):
        dx, dy = value
        
        if isinstance(dx,Vec2):
            dx = dx.x
        if isinstance(dy,Vec2):
            dy = dy.y

        self.x = self._x + dx
        self.y = self._y + dy

        self._entity.anchor = self._entity._anchor

        if self._entity.parent != None:
            self._entity._parent_offset.x = self._entity.parent.position.x - self.x
            self._entity._parent_offset.y = self._entity.parent.position.y - self.y

        return self

    def __isub__(self, value):
        dx,dy = value
        
        if isinstance(dx,Vec2):
            dx = dx.x
        if isinstance(dy,Vec2):
            dy = dy.y

        self.x = self._x - dx
        self.y = self._y - dy

        self._entity.anchor = self._entity._anchor

        if self._entity.parent != None:
            self._entity._parent_offset.x = self._entity.parent.position.x - self.x
            self._entity._parent_offset.y = self._entity.parent.position.y - self.y

        return self
    
    def __repr__(self):
        return f"({self._x},{self._y})"
    
    def __getitem__(self,key):
        return (self.x,self.y)[key]

class Scale:
    def __init__(self, x=0, y=0, entity=None):
        self._x = x
        self._y = y
        self._entity = entity

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        self._x = value
        if hasattr(self._entity,"is_ui") and self._entity.is_ui:
            self._entity._image = pygame.transform.scale(self._entity._default_image,(self._x * scale_def() * self._entity._default_scale_value.x / teon.functions.ZOOM,self._y * scale_def() * self._entity._default_scale_value.y / teon.functions.ZOOM)).convert_alpha()
        else:
            self._entity._image = pygame.transform.scale(self._entity._default_image,(self._x * scale_def() * self._entity._default_scale_value.x,self._y * scale_def() * self._entity._default_scale_value.y)).convert_alpha()
        self._entity.rect.width = self._entity.image.get_width()
        self._entity.anchor = self._entity._anchor

    def _set_x(self,x):
        self._x = x

    def _set_y(self,y):
        self._y = y
        
    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self._y = value
        if hasattr(self._entity,"is_ui") and self._entity.is_ui:
            self._entity._image = pygame.transform.scale(self._entity._default_image,(self._x * scale_def() * self._entity._default_scale_value.x / teon.functions.ZOOM,self._y * scale_def() * self._entity._default_scale_value.y / teon.functions.ZOOM)).convert_alpha()
        else:
            self._entity._image = pygame.transform.scale(self._entity._default_image,(self._x * scale_def() * self._entity._default_scale_value.x,self._y * scale_def() * self._entity._default_scale_value.y)).convert_alpha()
        self._entity.rect.height = self._entity.image.get_height()
        self._entity.anchor = self._entity._anchor

    def __iadd__(self, value):
        dx, dy = value
        
        if isinstance(dx,Vec2):
            dx = dx.x
        if isinstance(dy,Vec2):
            dy = dy.y

        self.x = self._x + dx
        self.y = self._y + dy

        self._entity.anchor = self._entity._anchor

        if self._entity.parent != None:
            self._entity._parent_offset.x = self._entity.parent.position.x - self.x
            self._entity._parent_offset.y = self._entity.parent.position.y - self.y

        return self

    def __isub__(self, value):
        dx,dy = value
        
        if isinstance(dx,Vec2):
            dx = dx.x
        if isinstance(dy,Vec2):
            dy = dy.y

        self.x = self._x - dx
        self.y = self._y - dy

        self._entity.anchor = self._entity._anchor

        if self._entity.parent != None:
            self._entity._parent_offset.x = self._entity.parent.position.x - self.x
            self._entity._parent_offset.y = self._entity.parent.position.y - self.y

        return self
    
    def __repr__(self):
        return f"({self._x},{self._y})"
    
    def __getitem__(self,key):
        return (self.x,self.y)[key]
        
class WidgetPosition:
    def __init__(self, x=0, y=0, entity=None):
        from teon.core import Teon
        self.core = Teon
        self._x = x
        self._y = y
        self._entity = entity

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        self._x = value
        if self.core._instances[0].aspect_borders:
            self._entity.rect.centerx = self._x * self.core._win_screen_size[0] + self.core._offput[0]
        else:
            self._entity.rect.centerx = self._x * min(self.core._instances[0].window.size.x,self.core._instances[0].window.size.y)
        self._entity.anchor = self._entity._anchor
        if self._entity.parent != None:
            self._entity._parent_offset.x = self.x - self._entity.parent.position.x

    def _set_x(self,x):
        self._x = x
        if self.core._instances[0].aspect_borders:
            self._entity.rect.centerx = self._x * self.core._win_screen_size[0] + self.core._offput[0]
        else:
            self._entity.rect.centerx = self._x * min(self.core._instances[0].window.size.x,self.core._instances[0].window.size.y)
        self._entity.anchor = self._entity._anchor

    def _set_y(self,y):
        self._y = y
        if self.core._instances[0].aspect_borders:
            self._entity.rect.centery = self._y * self.core._win_screen_size[1] + self.core._offput[1]
        else:
            if self._entity.window_anchor == "topleft":
                self._entity.rect.centery = self._y * min(self.core._instances[0].window.size.x,self.core._instances[0].window.size.y)

        self._entity.anchor = self._entity._anchor

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self._y = value
        if self.core._instances[0].aspect_borders:
            self._entity.rect.centery = self._y * self.core._win_screen_size[1] + self.core._offput[1]
        else:
            if self._entity.window_anchor == "topleft":
                self._entity.rect.centery = self._y * min(self.core._instances[0].window.size.x,self.core._instances[0].window.size.y)

        self._entity.anchor = self._entity._anchor
        if self._entity.parent != None:
            self._entity._parent_offset.y = self.y - self._entity.parent.position.y

    def __iadd__(self, value):
        dx, dy = value
        
        if isinstance(dx,Vec2):
            dx = dx.x
        if isinstance(dy,Vec2):
            dy = dy.y

        self.x = self._x + dx
        self.y = self._y + dy

        self._entity.anchor = self._entity._anchor

        if self._entity.parent != None:
            self._entity._parent_offset.x = self._entity.parent.position.x - self.x
            self._entity._parent_offset.y = self._entity.parent.position.y - self.y

        return self

    def __isub__(self, value):
        dx,dy = value
        
        if isinstance(dx,Vec2):
            dx = dx.x
        if isinstance(dy,Vec2):
            dy = dy.y

        self.x = self._x - dx
        self.y = self._y - dy

        self._entity.anchor = self._entity._anchor

        if self._entity.parent != None:
            self._entity._parent_offset.x = self._entity.parent.position.x - self.x
            self._entity._parent_offset.y = self._entity.parent.position.y - self.y

        return self
    
    def __repr__(self):
        return f"({self._x},{self._y})"
    
    def __getitem__(self,key):
        return (self.x,self.y)[key]
    
class CPosition:
    def __init__(self, x=0, y=0, entity=None):
        from teon.core import Teon
        self.core = Teon
        self._x = -x
        self._y = -y
        self._entity = entity

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        self._x = value
        self._entity.pos.x = self._x - (500 * scale_def())

    def full(self):
        return Vec2(self._x,self._y)
        
    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self._y = value
        self._entity.pos.y = self._y - (300 * scale_def())

    def __iadd__(self, value):
        dx, dy = value
        
        if isinstance(dx,Vec2):
            dx = dx.x
        if isinstance(dy,Vec2):
            dy = dy.y

        self.x = self._x + dx
        self.y = self._y + dy

        self._entity.anchor = self._entity._anchor

        return self

    def __isub__(self, value):
        dx,dy = value
        
        if isinstance(dx,Vec2):
            dx = dx.x
        if isinstance(dy,Vec2):
            dy = dy.y

        self.x = self._x - dx
        self.y = self._y - dy

        self._entity.anchor = self._entity._anchor

        return self
    
    def __repr__(self):
        return f"({self._x},{self._y})"
    
    def __getitem__(self,key):
        return (self.x,self.y)[key]
    
class MousePosition:
    def __init__(self, x=0, y=0, entity=None):
        from teon.core import Teon
        self.core = Teon
        self._x = x
        self._y = y

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        self._x = value

    def full(self):
        return Vec2(self._x * scale_def() + self.core._offput[0],self._y * scale_def() + self.core._offput[1])
        
    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self._y = value

    def __iadd__(self, value):
        dx, dy = value
        
        if isinstance(dx,Vec2):
            dx = dx.x
        if isinstance(dy,Vec2):
            dy = dy.y

        self.x = self._x + dx
        self.y = self._y + dy

        return self

    def __isub__(self, value):
        dx,dy = value
        
        if isinstance(dx,Vec2):
            dx = dx.x
        if isinstance(dy,Vec2):
            dy = dy.y

        self.x = self._x - dx
        self.y = self._y - dy

        return self
    
    def __repr__(self):
        return f"({self._x},{self._y})"
    
    def __getitem__(self,key):
        return (self.x,self.y)[key]
        
class MouseWPosition:
    def __init__(self, x=0, y=0, entity=None):
        from teon.core import Teon
        self.core = Teon
        self._x = x
        self._y = y

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        self._x = value

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self._y = value

    def __iadd__(self, value):
        dx, dy = value
        
        if isinstance(dx,Vec2):
            dx = dx.x
        if isinstance(dy,Vec2):
            dy = dy.y

        self.x = self._x + dx
        self.y = self._y + dy

        return self

    def __isub__(self, value):
        dx,dy = value
        
        if isinstance(dx,Vec2):
            dx = dx.x
        if isinstance(dy,Vec2):
            dy = dy.y

        self.x = self._x - dx
        self.y = self._y - dy

        return self
    
    def __repr__(self):
        return f"({self._x},{self._y})"
    
    def __getitem__(self,key):
        return (self.x,self.y)[key]