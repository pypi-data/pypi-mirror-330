import pygame
import math

from teon.functions import scale_def,_repair_vec2,_get_color_value,TeonFunction
from teon.other import Vec2
from teon.collider import SquareCollider
from teon.attributes import Position,Scale


def shake_screen(strength,time):
    Entity.level_editor.active_level.entities.shake(strength,time)

class Entity(pygame.sprite.Sprite):

    level_editor = None

    def __init__(self,**kwargs):
        """
        Main Entity class for Teon.

        Keyword Arguments: \n
        image: image of the entity, supports transparency
        """
        super().__init__()
        self._image = kwargs.get("image")
        collider = kwargs.get("collider")
        z = kwargs.get("z", 0)
        self._position = _repair_vec2(kwargs.get("position", Vec2((0,0))))
        self._rotation = kwargs.get("rotation", 0)
        vis = kwargs.get("visible", True)
        self._scale_def = scale_def()
        collidable = kwargs.get("collidable", True)
        self.updating = kwargs.get("updating",True)
        self.tags = kwargs.get("tags",[])
        self.running = kwargs.get("running",True)
        self._color = _get_color_value(kwargs.get("color",(255,255,255)))
        
        self._level_index = kwargs.get("lindex",0)
        self._alpha = kwargs.get("alpha",1)
        self._collider_size = 0

        self.animations = kwargs.get("animations",{})
        self.current_animation = -1
        self.animating = False

        if not self._image:
            self._image = pygame.Surface((100,100))
            self._image.fill(self._color)

        self._pos = Vec2(0,0)

        self._index = -1

        self._positionn = 0

        self.collidable = collidable
        self.visible = vis
        self.z = z

        self.functions = kwargs.get("functions",{})

        self._default_scale_value = Vec2(100,100)

        if isinstance(kwargs.get("scale",(1,1)),tuple):
            self._scale = kwargs.get("scale",(1,1))
        elif isinstance(kwargs.get("scale"),int) or isinstance(kwargs.get("scale"),float):
            self._scale = Vec2(kwargs.get("scale"),kwargs.get("scale"))

        x = self._position[0]
        y = self._position[1]
        x = x * scale_def()
        y = y * scale_def()
        self._position = Vec2((x,y))
        self._scale = (self._scale[0],self._scale[1])
        self.rscale = Scale(self._scale[0],self._scale[1],self)
        self.rect = self._image.get_rect(center = self._position)
        self.hitbox = SquareCollider(self,(0,0),(1,1))
        self._anchor_list = ["topleft","midleft","bottomleft","midtop","center","midbottom","topright","midright","bottomright"]

        self._anchor = kwargs.get("anchor","center")
        self.rposition = Position(0,0,self)

        self.parent = kwargs.get("parent",None)
        self.colliders = kwargs.get("colliders",{})
        self.position = (self.rect.centerx,self.rect.centery)

        self._default_image = self._image
        self.scale = (self.rscale.x,self.rscale.y)

        

        if collider is not None:
            self.hitbox = SquareCollider(self,collider[0],collider[1])

        if self._rotation != 0:
            self.image = pygame.transform.rotozoom(self.image,self._rotation,1)

        if Entity.level_editor:
            Entity.level_editor.add_entity_to_level(self)
        
        self._occlusion_rect = pygame.Rect(self.rect.x,self.rect.y,self.image.get_width() * 1.1,self.image.get_height() * 1.1)

        if not hasattr(self,"is_ui"):
            self.is_ui = kwargs.get("is_ui", False)
            self.position = _repair_vec2(kwargs.get("position", Vec2((0,0))))

        

        

    def _upt_scale_def(self,scale_def):
        self._scale_def = scale_def
        for collider in self.colliders:
            collider._upt_scale_def(self._scale_def)

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self,parent):
        if parent != None and isinstance(parent,Entity):
            self._parent = parent
            self._parent_offset = Vec2(self.position.x - self._parent.position.x,self.position.y - self._parent.position.y)
        else:
            self._parent = None
            self._parent_offset = Vec2(0,0)

    @property
    def anchor(self):
        return self._anchor

    @anchor.setter
    def anchor(self,anchor):
        self._anchor = anchor
        if anchor in self._anchor_list:
            self._anchor = anchor
                
            if self._anchor == "topleft":
                self.rect.center = (self.position.full().x + self.rect.width / 2,self.position.full().y + self.rect.height / 2)
            elif self._anchor == "center":
                self.rect.center = (self.position.full().x,self.position.full().y)
            elif self._anchor == "midright":
                self.rect.center = (self.position.full().x - self.rect.width / 2,self.position.full().y)
            elif self._anchor == "midleft":
                self.rect.center = (self.position.full().x + self.rect.width / 2,self.position.full().y)
            elif self._anchor == "midtop":
                self.rect.center = (self.position.full().x,self.position.full().y + self.rect.height / 2)
            elif self._anchor == "midbottom":
                self.rect.center = (self.position.full().x,self.position.full().y - self.rect.height / 2)
            elif self._anchor == "bottomleft":
                self.rect.center = (self.position.full().x + self.rect.width / 2,self.position.full().y - self.rect.height / 2)
            elif self._anchor == "topright":
                self.rect.center = (self.position.full().x - self.rect.width / 2,self.position.full().y + self.rect.height / 2)
            elif self._anchor == "bottomright":
                self.rect.center = (self.position.full().x - self.rect.width / 2,self.position.full().y - self.rect.height / 2)
        else:
            print("The anchor provided doesn't represent a point on the entity collider, for more help take a look at the Teon documentation.")

    @property
    def left(self):
        return self.topleft.x
    
    @left.setter
    def left(self,value):
        self.topleft = (value,self.topleft.y)
    
    @property
    def right(self):
        return self.topright.x
    
    @right.setter
    def right(self,value):
        self.topright = (value,self.topright.y)
    
    @property
    def top(self):
        return self.topleft.y
    
    @top.setter
    def top(self,value):
        self.topleft = (self.topleft.x,value)
    
    @property
    def bottom(self):
        return self.bottomleft.y
    
    @bottom.setter
    def bottom(self,value):
        self.bottomleft = (self.bottomleft.x,value)

    @property
    def topleft(self):
        if self.anchor == "center":
            return Vec2(self.position.x - (self.scale.x * 50), self.position.y - (self.scale.y * 50))
        elif self.anchor == "topleft":
            return self.position
        elif self.anchor == "midtop":
            return Vec2(self.position.x - (self.scale.x * 50), self.position.y)
        elif self.anchor == "topright":
            return Vec2(self.position.x - (self.scale.x * 100), self.position.y)
        elif self.anchor == "midright":
            return Vec2(self.position.x - (self.scale.x * 100), self.position.y - (self.scale.y * 50))
        elif self.anchor == "bottomright":
            return Vec2(self.position.x - (self.scale.x * 100), self.position.y - (self.scale.y * 100))
        elif self.anchor == "midbottom":
            return Vec2(self.position.x - (self.scale.x * 50), self.position.y - (self.scale.y * 100))
        elif self.anchor == "bottomleft":
            return Vec2(self.position.x, self.position.y - (self.scale.y * 100))
        elif self.anchor == "midleft":
            return Vec2(self.position.x, self.position.y - (self.scale.y * 50))

    @topleft.setter
    def topleft(self, value):
        offset = self.topleft - self.position
        self.position = value - offset

    @property
    def midtop(self):
        return Vec2(self.topleft.x,self.topleft.y) + Vec2(self.scale.x * 50, 0)

    @midtop.setter
    def midtop(self, value):
        offset = self.midtop - self.position
        self.position = value - offset

    @property
    def topright(self):
        return Vec2(self.topleft.x,self.topleft.y) + Vec2(self.scale.x * 100, 0)

    @topright.setter
    def topright(self, value):
        offset = self.topright - self.position
        self.position = value - offset

    @property
    def midright(self):
        return Vec2(self.topleft.x,self.topleft.y) + Vec2(self.scale.x * 100, self.scale.y * 50)

    @midright.setter
    def midright(self, value):
        offset = self.midright - self.position
        self.position = value - offset

    @property
    def bottomright(self):
        return Vec2(self.topleft.x,self.topleft.y) + Vec2(self.scale.x * 100, self.scale.y * 100)

    @bottomright.setter
    def bottomright(self, value):
        offset = self.bottomright - self.position
        self.position = value - offset

    @property
    def midbottom(self):
        return Vec2(self.topleft.x,self.topleft.y) + Vec2(self.scale.x * 50, self.scale.y * 100)

    @midbottom.setter
    def midbottom(self, value):
        offset = self.midbottom - self.position
        self.position = value - offset

    @property
    def bottomleft(self):
        return Vec2(self.topleft.x,self.topleft.y) + Vec2(0, self.scale.y * 100)

    @bottomleft.setter
    def bottomleft(self, value):
        offset = self.bottomleft - self.position
        self.position = value - offset

    @property
    def midleft(self):
        return Vec2(self.topleft.x,self.topleft.y) + Vec2(0, self.scale.y * 50)

    @midleft.setter
    def midleft(self, value):
        offset = self.midleft - self.position
        self.position = value - offset

    @property
    def center(self):
        return Vec2(self.topleft.x,self.topleft.y) + Vec2(self.scale.x * 50, self.scale.y * 50)

    @center.setter
    def center(self, value):
        offset = self.center - self.position
        self.position = value - offset



    @property
    def color(self):
        return self._color
    
    @color.setter
    def color(self,color):
        self._color = _get_color_value(color)
        self.image.fill(self._color)

    def add_func(self,func,key,tps,running = True):
        self.functions[key] = TeonFunction(func,tps,running)

    def remove_func(self,key):
        self.functions.pop(key)

    def add_tag(self,tag):
        if not tag in self.tags:
            self.tags.append(tag)

    def remove_tag(self,tag):
        if tag in self.tags:
            self.tags.pop(self.tags.index(tag))
            
    def input(self,key):
        pass

    @property
    def position(self):
        return self.rposition

    @position.setter
    def position(self,position):
        self.rposition.x = position[0]
        self.rposition.y = position[1]

    def has_tag(self,tag):
        if tag in self.tags:
            return True
        return False
    
    def _update_colliders(self):
        for _,collider in self.colliders.items():
            collider.update()

    @property
    def collider(self):
        return self.hitbox
    
    @property
    def level_index(self):
        return self._level_index

    @level_index.setter
    def level_index(self,level_index):
        index = self._level_index
        Entity.level_editor.remove_entity_from_level(self,index)
        self._level_index = level_index
        Entity.level_editor.add_entity_to_level(self)
    
    def look_at(self, target):
        '''
        Give the entity as input and it will rotate to look at the entity with the top of the image,but the hitbox doesn't change shape
        '''
        if isinstance(target,Entity):
            target = target._position
        direction = pygame.Vector2(target) - self._position
        self._rotation = math.degrees(math.atan2(-direction.y, direction.x))

        self.image = pygame.transform.rotozoom(self._default_image, self._rotation,1)

    @property
    def rotation(self):
        return self._rotation
    
    @rotation.setter
    def rotation(self,degree):
        self._rotation += degree
        self.image = pygame.transform.rotozoom(self._default_image,self._rotation,1)

    @property
    def alpha(self):
        return self._alpha

    @alpha.setter
    def alpha(self,value):
        self._alpha = value
        self._default_image.set_alpha(value * 255)
        self.image.set_alpha(value * 255)

    @property
    def image(self):
        return self._image
    
    @image.setter
    def image(self,image):
        self._default_image = image
        self._image = image
        self.scale = (self.rscale.x,self.rscale.y)

    def set_animation(self,animation_key):
            self.current_animation = self.animations[animation_key]
            self.current_animation._timer.activate()
    
    def _update_functions(self):
        for _,func in self.functions.items():
            func._run()

    @property
    def scale(self):
        return self.rscale

    @scale.setter
    def scale(self,scale):
        if isinstance(scale,int) or isinstance(scale,float):
            scale = (scale,scale)
        self.rscale.x = scale[0]
        self.rscale.y = scale[1]

    def _update(self):
        self._update_functions()
        self._update_colliders()
        self.hitbox.update()

        if not self.current_animation == -1 and self.current_animation != None:
            if self.animating:
                self.current_animation._timer.update()
                if not self.current_animation._timer.active:
                    self._index += 1
                    
                    if self._index >= len(self.current_animation.images):
                        self._index = 0
                    
                    self.image = self.current_animation.images[self._index]

                    self.current_animation._timer.activate()

        if not self.parent == None:
            self.position._set_x(self.parent.position.x + self._parent_offset.x)
            self.position._set_y(self.parent.position.y + self._parent_offset.y)
            
    def update(self):
        pass