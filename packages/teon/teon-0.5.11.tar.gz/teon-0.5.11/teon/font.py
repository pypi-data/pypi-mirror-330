import pygame

class Font(pygame.font.Font):
    def __init__(self,font_path = None):
        super().__init__(font_path,10)
        self.path = font_path