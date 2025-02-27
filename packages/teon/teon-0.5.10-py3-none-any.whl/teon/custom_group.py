import pygame

from random import randint
from teon.other import Timer,Vec2
from teon.functions import scale_def

class CustomGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.offset = Vec2()
        self.camera_speed = 0.1
        self.player = 0

        self.is_shaking = False

        self.shaking_strength = 0

        self.shaking_time = Timer(1)

    def shake(self,strength,time):
        self.is_shaking = True
        self.shaking_strength = strength
        self.shaking_time = Timer(time)
        self.shaking_time.activate()

    def get_class(self):
        from teon.core import Teon
        self._core_class = Teon._instances[0]

    def lerp(self, start, end, t):
        return start + (end - start) * t * self._core_class.dt

    def draw(self, surface):
        offset_x = randint(-self.shaking_strength,self.shaking_strength)
        offset_y = randint(-self.shaking_strength,self.shaking_strength)
        self.shaking_time.update()
        if not self.shaking_time.active:
            self.is_shaking = False
        else:
            self.is_shaking = True
        if self._core_class.camera.parent is not None:
            if self._core_class.camera.follow_type == "follow":
                self._core_class.camera.position.x = (self._core_class.camera.parent.rect.centerx - pygame.display.get_window_size()[0] / 2) + (500 * scale_def())
                self._core_class.camera.position.y = (self._core_class.camera.parent.rect.centery - pygame.display.get_window_size()[1] / 2) + (300 * scale_def())

            if self._core_class.camera.follow_type == "smooth follow":

                target_offset_x = (self._core_class.camera.parent.rect.centerx - pygame.display.get_window_size()[0] / 2) + (500 * scale_def())
                target_offset_y = (self._core_class.camera.parent.rect.centery - pygame.display.get_window_size()[1] / 2) + (300 * scale_def())
                self._core_class.camera.position.x = self.lerp(self._core_class.camera.position.x, target_offset_x, self._core_class.camera.speed)
                self._core_class.camera.position.y = self.lerp(self._core_class.camera.position.y, target_offset_y, self._core_class.camera.speed)
                
        if not self.is_shaking:
            offset_x,offset_y = 0,0

        sorted_sprites = sorted(self.sprites(), key=lambda sprite: (sprite.z, sprite.rect.bottom))
        self._core_class.__class__._offset = self.offset + (offset_x,offset_y)
        for sprite in sorted_sprites:
            sprite._positionn = sprite.rect.topleft + self.offset + (offset_x,offset_y)
            if sprite.visible and sprite.running:
                if sprite.is_ui:
                    surface.display.blit(sprite._image, sprite.rect.topleft)
                
                else:
                    surface.display.blit(sprite._image,(sprite.rect.topleft[0] - self._core_class.camera.pos.x + offset_x + self._core_class.camera.offset.x,sprite.rect.topleft[1] - self._core_class.camera.pos.y + offset_y + self._core_class.camera.offset.y))
                    sprite._pos = Vec2(self._core_class.camera.position.full().x + self._core_class.camera.offset.x,self._core_class.camera.pos.y + self._core_class.camera.offset.y)