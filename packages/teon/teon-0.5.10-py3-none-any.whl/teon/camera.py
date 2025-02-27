from teon.attributes import CPosition
from teon.functions import _repair_vec2
class Camera:
    def __init__(self):
        self._position = _repair_vec2((0,0))
        self.pos = self._position
        self.position = self.position.x,self.position.y

        self._offset = _repair_vec2((0,0))
        self.offset = self.offset.x,self.offset.y

        self.speed = 5

        self.parent = None
        self.follow_type = "smooth follow"

        self.is_init = False

    def _init(self,**kwargs):
        from teon.core import get_main_class
        self._core = get_main_class()
        self.is_init = True
        self._position = _repair_vec2(kwargs.get("position",self.position))
        self.pos = self._position
        self._position = CPosition(self._position.x,self._position.y,self)
        self.position = self.position.x,self.position.y

        self._offset = _repair_vec2(kwargs.get("offset",self.offset))
        self._offset = CPosition(self._offset.x,self._offset.y,self)
        self.offset = self.offset.x,self.offset.y

        self.speed = kwargs.get("speed",self.speed)

        self.parent = kwargs.get("parent",self.parent)
        self.follow_type = kwargs.get("follow_type",self.follow_type)

    @property
    def offset(self):
        return self._offset
    
    @offset.setter
    def offset(self,position):
        position = _repair_vec2(position)
        self._offset.x = position.x
        self._offset.y = position.y

    @property
    def zoom(self):
        return self._core.zoom
    
    @zoom.setter
    def zoom(self,value):
        self._core.zoom = value

    @property
    def position(self):
        return self._position
    
    @position.setter
    def position(self,position):
        position = _repair_vec2(position)
        self._position.x = position.x
        self._position.y = position.y

    def __repr__(self):
        return f"Position:{round(self.position.x,2)},{round(self.position.y,2)},Offset:{self.offset},Parent:{self.parent},Speed:{self.speed},Follow Type:{self.follow_type}"

cinstance = Camera()