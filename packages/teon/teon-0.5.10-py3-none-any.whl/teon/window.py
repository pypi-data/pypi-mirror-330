import pygame

from teon.functions import _repair_vec2
import teon.functions

class Window:
    def __init__(self):
        self._size = _repair_vec2((1000,600))
        self._caption = "Teon"
        self._fullscreen = False
        self._resizable = False
        self.fps = 60
        self._aspect_ratio = _repair_vec2((10,6))

    @property
    def aspect_ratio(self):
        return self._aspect_ratio
    
    @aspect_ratio.setter
    def aspect_ratio(self,tupl):
        self._aspect_ratio = _repair_vec2(tupl)
        teon.functions.ASPECT_SIZE = self._aspect_ratio
        if hasattr(self._core,"_entity_counter_text"):
            self._core._adapt_all()
        else:
            self._core._adapt_all_entities()
    
    def _init(self,core,**kwargs):
        self._size = _repair_vec2(kwargs.get("size",(1000,600)))
        self._caption = kwargs.get("caption", "Teon")
        self._fullscreen = kwargs.get("fullscreen", False)
        self._resizable = kwargs.get("resizable",False)
        self.fps = kwargs.get("fps",60)
        self._aspect_ratio = kwargs.get("aspect_ratio",(1000,600))

        self._core = core

        self._default_window_size = self._size
        
        if self._fullscreen:
            if self._resizable:
                self.display = pygame.display.set_mode(pygame.display.get_desktop_sizes()[0],pygame.RESIZABLE)
            else:
                self.display = pygame.display.set_mode(pygame.display.get_desktop_sizes()[0])
            self._size = _repair_vec2(self.display.get_size())
        else:
            if self._resizable:
                self.display = pygame.display.set_mode(self._size,pygame.RESIZABLE)
            else:
                self.display = pygame.display.set_mode(self._size)

        pygame.display.set_caption(self._caption)
        path = __file__.split("\\")
        htap = ""
        for i in range(len(path) - 1):
            htap += path[i] + "/"
        self._icon = kwargs.get("icon", pygame.image.load(htap + "icon.png"))
        
        pygame.display.set_icon(self._icon)
        
        if self._aspect_ratio == "full window":
            self._aspect_ratio = self._size

    @property
    def caption(self):
        return self._caption

    @caption.setter
    def caption(self,caption):
        self._caption = caption
        pygame.display.set_caption(self._caption)

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self,size):
        self._size = _repair_vec2(size)
        if self._fullscreen:
            if self._resizable:
                self.display = pygame.display.set_mode(pygame.display.get_desktop_sizes()[0],pygame.RESIZABLE)
            else:
                self.display = pygame.display.set_mode(pygame.display.get_desktop_sizes()[0])
        else:
            if self._resizable:
                self.display = pygame.display.set_mode((self._size.x,self._size.y),pygame.RESIZABLE)
            else:
                self.display = pygame.display.set_mode((self._size.x,self._size.y))

    @property
    def resizable(self):
        return self._resizable

    @resizable.setter
    def resizable(self,bool):
        self._resizable = bool
        if self._fullscreen:
            if self._resizable:
                self.display = pygame.display.set_mode(pygame.display.get_desktop_sizes()[0],pygame.RESIZABLE)
            else:
                self.display = pygame.display.set_mode(pygame.display.get_desktop_sizes()[0])
        else:
            if self._resizable:
                self.display = pygame.display.set_mode(self._size,pygame.RESIZABLE)
            else:
                self.display = pygame.display.set_mode(self._size)

    @property
    def icon(self):
        return self._icon
    
    @icon.setter
    def icon(self,icon):
        self._icon = icon
        pygame.display.set_icon(self._icon)

    @property
    def fullscreen(self):
        return self._fullscreen

    @fullscreen.setter
    def fullscreen(self,bool):
        self._fullscreen = bool
        if self._fullscreen:
            if self._resizable:
                self.display = pygame.display.set_mode(pygame.display.get_desktop_sizes()[0],pygame.RESIZABLE)
            else:
                self.display = pygame.display.set_mode(pygame.display.get_desktop_sizes()[0])
        else:
            if self._resizable:
                self.display = pygame.display.set_mode((self._size.x,self._size.y),pygame.RESIZABLE)
            else:
                self.display = pygame.display.set_mode((self._size.x,self._size.y))
        self.size = _repair_vec2(self.display.get_size())
        if hasattr(self._core,"_entity_counter_text"):
            self._core._adapt_all()
        else:
            self._core._adapt_all_entities()

    def __repr__(self):
        return f"Size:{self.size},FPS:{self.fps},Fullscreen:{self.fullscreen},Aspect Ratio:{self.aspect_ratio}"

winstance = Window()