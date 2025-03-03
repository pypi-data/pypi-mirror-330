import pygame

from teon.functions import key_pressed,scale_def,_repair_vec2,colliding
from teon.entity import Entity
from teon.other import Vec2

class Controller2D(Entity):
    _instances = []
    def __init__(self,**kwargs):
        super().__init__(**kwargs)

        self.space = False

        self._position = Vec2((self.rect.centerx,self.rect.centery))

        Controller2D._instances.append(self)
        self.tags.append("dt")

        self._occluder_rect = pygame.Rect(1,1,pygame.display.get_window_size()[0],pygame.display.get_window_size()[1])

class PlayerController2D(Controller2D):
    _instances = []
    def __init__(self,**kwargs):
        self.can_collide = kwargs.get("can_collide",True)
        super().__init__(**kwargs)
        self.controller = kwargs.get("controller","full topdown")
        self.gravity = kwargs.get("gravity",0)
        self.screen_bound = kwargs.get("screen_bound",False)
        
        self.speed = kwargs.get("speed",300)
        self.can_jump = kwargs.get("can_jump",False)
        self.jump_force = kwargs.get("jump_force",0)
        self.jump_number = kwargs.get("jump_number",1)
        self.velocity = 0
        self.jumps = self.jump_number
        self.is_ui = False

        self.direction = Vec2((0,0))

        self.dt = 0

        self.space = False

        self._position = Vec2((self.rect.centerx,self.rect.centery))

        PlayerController2D._instances.append(self)

        self.tags.append("dt")

        self._last_position = [0,0,0,0]

        self._physics_body_collision = False

    def _input(self):
        if self.controller == "platformer":
            if key_pressed("left"):
                self.direction.x = -1
            elif key_pressed("right"):
                self.direction.x = 1
            else:
                self.direction.x = 0

            if self.can_jump:
                if key_pressed("space") and self.jumps > 0 and not self.space:
                    self.velocity = -self.jump_force
                    self.jumps -= 1
                    self.space = True
                elif self.jumps > 0 and not key_pressed("space"):
                    self.space = False

        if self.controller == "topdown":
            if key_pressed("left"):
                self.direction.x = -1
                self.direction.y = 0
            elif key_pressed("right"):
                self.direction.x = 1
                self.direction.y = 0

            elif key_pressed("up"):
                self.direction.y = -1
                self.direction.x = 0
            elif key_pressed("down"):
                self.direction.y = 1
                self.direction.x = 0
            else:
                self.direction.x = 0
                self.direction.y = 0
        
        if self.controller == "full topdown":
            input_vector = Vec2()
            if key_pressed("up"):
                input_vector.y -= 1
            if key_pressed("down"):
                input_vector.y += 1
            if key_pressed("left"):
                input_vector.x -= 1
            if key_pressed("right"):
                input_vector.x += 1
            self.direction = input_vector.normalize() if input_vector else input_vector

    def _move(self):
        if self.controller == "platformer":
            self.velocity += self.gravity * self.dt
            self.position.y += self.velocity * self.dt

        speed = self.speed

        if self._physics_body_collision != False:
            speed /= self._physics_body_collision.weight
            
        self.position.x += self.direction.x * speed * self.dt

        self.position.y += self.direction.y * speed * self.dt

        self.hitbox.update()

        self._collide()

    def _collide(self):
        self._physics_body_collision = False
        if self.can_collide:
            active_level = Entity.level_editor.active_level
            if active_level and active_level.index == self.level_index:
                self.collision_sprites = active_level.entities
                for sprite in self.collision_sprites:
                    if colliding(self,sprite) and sprite is not self and sprite.collidable:
                        horizontal_overlap = max(0, min(self._last_position[2], sprite.right) - max(self._last_position[0], sprite.left))
                        vertical_overlap = max(0, min(self._last_position[3], sprite.bottom) - max(self._last_position[1], sprite.top))
                            
                        if (horizontal_overlap,vertical_overlap) == (0,0):
                            horizontal_overlap = min(self.right - sprite.left, sprite.right - self.left)
                            vertical_overlap = min(self.bottom - sprite.top, sprite.bottom - self.top)
                                
                            if abs(horizontal_overlap) < abs(vertical_overlap):
                                if self.center.x <= sprite.center.x:
                                    self.right = sprite.left
                                else:
                                    self.left = sprite.right

                            else:
                                if self.center.y <= sprite.center.y:
                                    self.bottom = sprite.top
                                    self.velocity = 0
                                    self.jumps = self.jump_number
                                else:
                                    self.top = sprite.bottom
                                    self.velocity = 0

                        elif horizontal_overlap <= vertical_overlap:
                            if self.center.x <= sprite.center.x:
                                self.right = sprite.left
                            else:
                                self.left = sprite.right

                        else:
                            if self.center.y <= sprite.center.y:
                                self.bottom = sprite.top
                                self.velocity = 0
                                self.jumps = self.jump_number
                            else:
                                self.top = sprite.bottom
                                self.velocity = 0
            
        self.hitbox.update()
        self._last_position = [self.topleft.x,self.topleft.y,self.bottomright.x,self.bottomright.y]

    def _update(self):
        super()._update()
        self._occlusion_rect.center = self.rect.center
        self._occluder_rect.center = self.rect.center
        self._update_colliders()
        self._input()
        self._move()
        if self.screen_bound:
            self._bound()