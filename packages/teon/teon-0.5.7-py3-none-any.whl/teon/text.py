import pygame,teon

from teon.widget import Widget
from teon.functions import scale_def
from teon.font import Font
from teon.collider import SquareCollider

class Text(Widget):
    def __init__(self, **kwargs):
        '''
        Text class used to display text in the UI and in the game world. \n

        Keyword Arguments: \n
        antialias: self explanatory \n
        background_color: the background color of the text, default is None \n 
        is_ui: if True, the text will stay on the screen and not move \n 
        color: the color of the text \n 
        font can either be a literal font or teon.Font class \n
        anchor: offset the text based on the collider anchor
        '''
        self._font = kwargs.get("font",None)
        self._text = kwargs.get("text","Text")
        self._size = kwargs.get("size",30)
        self._antialias = kwargs.get("antialias", False)
        self._background_color = kwargs.get("background_color", None)
        self._color = kwargs.get("color", (255, 255, 255))
        self._screen_bound = kwargs.get("screen_bound",False)

        super().__init__(**kwargs)
        
        self._render_text()

        self.rect = self.image.get_rect(center = (self.rect.center))
        self.hitbox = SquareCollider(self,(0,0),(1,1))

        self.is_ui = kwargs.get("is_ui", True)
        self.collidable = False

    def _render_text(self):
        """Helper method to render text."""
        if isinstance(self._font, Font):
            font = self._font.path
        else:
            font = self._font
        if self.is_ui:
            self._image = pygame.font.Font(font, int(self._size * scale_def() / teon.functions.ZOOM)).render(self._text, self._antialias, self._color, self._background_color)
        else:
            self._image = pygame.font.Font(font, int(self._size * scale_def())).render(self._text, self._antialias, self._color, self._background_color)
        self._default_image = self._image
        self.rect = self.image.get_rect(center = (self.rect.center))
        self.hitbox = SquareCollider(self,(0,0),(1,1))

    @property
    def background_color(self):
        return self._background_color

    @background_color.setter
    def background_color(self,color):
        self._background_color = color
        self._render_text()

    @property
    def antialias(self):
        return self._antialias

    @antialias.setter
    def antialias(self,bool):
        self._antialias = bool
        self._render_text()

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, color):
        self._color = color
        self._render_text()

    @property
    def size(self):
        return int(self._size / scale_def())

    @size.setter
    def size(self, size):
        self._size = int(size * scale_def())
        self._render_text()

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, text):
        self._text = text
        self._render_text()
    
    def update(self):
        super().update()
        self.anchor = self._anchor