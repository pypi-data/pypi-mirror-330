import pygame,sys
import time,teon

import teon.functions
from teon.entity import Entity

from teon.mouse import minstance
from teon.camera import cinstance
from teon.window import winstance

from teon.level import Level,LevelEditor

from teon.functions import rt_key,_get_color_value,_key_map

import teon.functions

class Teon:
    _instances = []
    _offset = (0,0)
    _offput = (0,0)
    _win_screen_size = (0,0)
    def __init__(self,**kwargs):


        pygame.init()
        
        self.debug = kwargs.get("debug", False)
        self.key_press_time = kwargs.get("key_press_time",0.2)
        self.frustum_culling = kwargs.get("frustum_culling",False)
        self.entity_counter = kwargs.get("entity_counter",True)
        self.aspect_borders = kwargs.get("aspect_borders",False)
        self.aspect_borders_color = kwargs.get("aspect_borders_color",(0,0,0))
        self.fullsreen_key = kwargs.get("fullscreen_key",None)
        self._antialiasing = kwargs.get("antialiasing",True)
        self._background_color = _get_color_value(kwargs.get("background_color",(0,0,0)))

        teon.other.antialiasing = self._antialiasing

        self.restrict = {key: False for key in _key_map}
        self.restrict["wheel up"] = False
        self.restrict["wheel down"] = False

        self.window = winstance
        self.window._init(self,**kwargs)
        self.time = pygame.time.Clock()
        Teon._instances.append(self)
        self.camera = cinstance
        self.camera._init(**kwargs)

        self._last_window_size = self.window.size
        self._last_window_position = self.window._get_window_position()

        self._zoom = 1

        self.level_editor = LevelEditor()
        Entity.level_editor = self.level_editor

        Level(index = 0)

        self.level_editor.set_active_level(0)

        
        teon.functions.ASPECT_SIZE = self.window.aspect_ratio
        if self.window.size.x / self.window.size.y > (teon.functions.ASPECT_SIZE[0] / teon.functions.ASPECT_SIZE[1]):
            self._left_border = pygame.Rect(0, 0, (self.window.size.x - int(self.window.size.y * (teon.functions.ASPECT_SIZE[0] / teon.functions.ASPECT_SIZE[1]))) // 2, self.window.size.y)
            self._right_border = pygame.Rect(self.window.size.x - (self.window.size.x - int(self.window.size.y * (teon.functions.ASPECT_SIZE[0] / teon.functions.ASPECT_SIZE[1]))) // 2, 0, (self.window.size.x - int(self.window.size.y * (teon.functions.ASPECT_SIZE[0] / teon.functions.ASPECT_SIZE[1]))) // 2, self.window.size.y)
            
            Teon._offput = teon.functions._repair_vec2((self._left_border.width,0))

            Teon._win_screen_size = (pygame.display.get_surface().get_width() - (self._left_border.width * 2),pygame.display.get_surface().get_height())

        elif self.window.size.x / self.window.size.y < (teon.functions.ASPECT_SIZE[0] / teon.functions.ASPECT_SIZE[1]):
            self._left_border = pygame.Rect(0, 0, self.window.size.x, (self.window.size.y - int(self.window.size.x / (teon.functions.ASPECT_SIZE[0] / teon.functions.ASPECT_SIZE[1]))) // 2)
            self._right_border = pygame.Rect(0, self.window.size.y - (self.window.size.y - int(self.window.size.x / (teon.functions.ASPECT_SIZE[0] / teon.functions.ASPECT_SIZE[1]))) // 2, self.window.size.x, (self.window.size.y - int(self.window.size.x / (teon.functions.ASPECT_SIZE[0] / teon.functions.ASPECT_SIZE[1]))) // 2)

            Teon._offput = teon.functions._repair_vec2((0,self._left_border.height))
            
            Teon._win_screen_size = (pygame.display.get_surface().get_width(),pygame.display.get_surface().get_height() - (self._left_border.height * 2))


        else:
            self._left_border = -1
            Teon._win_screen_size = (pygame.display.get_surface().get_width(),pygame.display.get_surface().get_height())

        self.mouse = minstance
        self.mouse._init(self,**kwargs)
        

    def input(self,key):
        pass

    @property
    def zoom(self):
        return self._zoom
    
    @zoom.setter
    def zoom(self,value):
        self._zoom = value
        teon.functions.ZOOM = self._zoom
        self._adapt_all_entities()

    @property
    def entities(self):
        entities = []
        for level in self.level_editor.levels:
            for entity in level.entities:
                if not entity.has_tag("_entity_counter_text"):
                    entities.append(entity)
        return entities
    
    @property
    def antialiasing(self):
        return self._antialiasing
    
    @antialiasing.setter
    def antialiasing(self,value):
        self._antialiasing = value
        teon.other.antialiasing = self._antialiasing

    def _adapt_all_entities(self):
        self.window.size = pygame.display.get_surface().get_size()
        if self.window.size.x / self.window.size.y > (teon.functions.ASPECT_SIZE[0] / teon.functions.ASPECT_SIZE[1]):
            self._left_border = pygame.Rect(0, 0, (self.window.size.x - int(self.window.size.y * (teon.functions.ASPECT_SIZE[0] / teon.functions.ASPECT_SIZE[1]))) // 2, self.window.size.y)
            self._right_border = pygame.Rect(self.window.size.x - (self.window.size.x - int(self.window.size.y * (teon.functions.ASPECT_SIZE[0] / teon.functions.ASPECT_SIZE[1]))) // 2, 0, (self.window.size.x - int(self.window.size.y * (teon.functions.ASPECT_SIZE[0] / teon.functions.ASPECT_SIZE[1]))) // 2, self.window.size.y)
                        
            Teon._offput = teon.functions._repair_vec2((self._left_border.width,0))

            Teon._win_screen_size = (pygame.display.get_surface().get_width() - (self._left_border.width * 2),pygame.display.get_surface().get_height())

        elif self.window.size.x / self.window.size.y < (teon.functions.ASPECT_SIZE[0] / teon.functions.ASPECT_SIZE[1]):
            self._left_border = pygame.Rect(0, 0, self.window.size.x, (self.window.size.y - int(self.window.size.x / (teon.functions.ASPECT_SIZE[0] / teon.functions.ASPECT_SIZE[1]))) // 2)
            self._right_border = pygame.Rect(0, self.window.size.y - (self.window.size.y - int(self.window.size.x / (teon.functions.ASPECT_SIZE[0] / teon.functions.ASPECT_SIZE[1]))) // 2, self.window.size.x, (self.window.size.y - int(self.window.size.x / (teon.functions.ASPECT_SIZE[0] / teon.functions.ASPECT_SIZE[1]))) // 2)

            Teon._offput = teon.functions._repair_vec2((0,self._left_border.height))
                    
            Teon._win_screen_size = (pygame.display.get_surface().get_width(),pygame.display.get_surface().get_height() - (self._left_border.height * 2))


        else:
            self._left_border = -1
            Teon._offput = (0,0)
            Teon._win_screen_size = (pygame.display.get_surface().get_width(),pygame.display.get_surface().get_height())
        for entity in self.entities:
            if not entity.is_ui:
                entity._upt_scale_def(teon.functions.scale_def())
                entity.position = (entity.rposition.x,entity.rposition.y)
                entity.scale = (entity.rscale.x,entity.rscale.y)
        
    def _adapt_all(self):
        self.window.size = pygame.display.get_surface().get_size()
        if self.window.size.x / self.window.size.y > (teon.functions.ASPECT_SIZE[0] / teon.functions.ASPECT_SIZE[1]):
            self._left_border = pygame.Rect(0, 0, (self.window.size.x - int(self.window.size.y * (teon.functions.ASPECT_SIZE[0] / teon.functions.ASPECT_SIZE[1]))) // 2, self.window.size.y)
            self._right_border = pygame.Rect(self.window.size.x - (self.window.size.x - int(self.window.size.y * (teon.functions.ASPECT_SIZE[0] / teon.functions.ASPECT_SIZE[1]))) // 2, 0, (self.window.size.x - int(self.window.size.y * (teon.functions.ASPECT_SIZE[0] / teon.functions.ASPECT_SIZE[1]))) // 2, self.window.size.y)
                        
            Teon._offput = teon.functions._repair_vec2((self._left_border.width,0))

            Teon._win_screen_size = (pygame.display.get_surface().get_width() - (self._left_border.width * 2),pygame.display.get_surface().get_height())

        elif self.window.size.x / self.window.size.y < (teon.functions.ASPECT_SIZE[0] / teon.functions.ASPECT_SIZE[1]):
            self._left_border = pygame.Rect(0, 0, self.window.size.x, (self.window.size.y - int(self.window.size.x / (teon.functions.ASPECT_SIZE[0] / teon.functions.ASPECT_SIZE[1]))) // 2)
            self._right_border = pygame.Rect(0, self.window.size.y - (self.window.size.y - int(self.window.size.x / (teon.functions.ASPECT_SIZE[0] / teon.functions.ASPECT_SIZE[1]))) // 2, self.window.size.x, (self.window.size.y - int(self.window.size.x / (teon.functions.ASPECT_SIZE[0] / teon.functions.ASPECT_SIZE[1]))) // 2)

            Teon._offput = teon.functions._repair_vec2((0,self._left_border.height))
                    
            Teon._win_screen_size = (pygame.display.get_surface().get_width(),pygame.display.get_surface().get_height() - (self._left_border.height * 2))


        else:
            self._left_border = -1
            Teon._offput = (0,0)
            Teon._win_screen_size = (pygame.display.get_surface().get_width(),pygame.display.get_surface().get_height())
        for entity in self.entities:
            entity._upt_scale_def(teon.functions.scale_def())
            entity.position = (entity.rposition.x,entity.rposition.y)
            entity.scale = (entity.rscale.x,entity.rscale.y)
        self._entity_counter_text.position = (self._entity_counter_text.rposition.x,self._entity_counter_text.rposition.y)
        self._entity_counter_text.scale = (self._entity_counter_text.rscale.y,self._entity_counter_text.rscale.y)

    @property
    def background_color(self):
        return self._background_color
    
    @background_color.setter
    def background_color(self,color):
        self._background_color = _get_color_value(color)
    
    def update(self):
        pass

    def _event(self,event):
        if event.type == pygame.WINDOWRESIZED:
            self._last_window_position = self.window._get_window_position()
            self._last_window_size = pygame.display.get_window_size()
            self.window.size = self._last_window_size
            self._adapt_all()

        elif event.type == pygame.WINDOWMAXIMIZED:
            self._last_window_position = self.window._get_window_position()
            self._last_window_size = pygame.display.get_window_size()
            self.window.size = self._last_window_size
            self.window.fullscreen = not self.window.fullscreen
            self._adapt_all()

    def _input(self,key):
        if key == self.fullsreen_key and not self.fullsreen_key == None:
            self._last_window_position = self.window._get_window_position()
            self._last_window_size = pygame.display.get_window_size()
            self.window.size = self._last_window_size
            self.window.fullscreen = not self.window.fullscreen
            self._adapt_all()

    def quit(self):
        pygame.quit()
        sys.exit()

    def input(self,key):
        pass

    def run(self,update_func = None,input_func = None):
        '''
        This is the last function of the program, nothing after this will be run. \n
        If you have a function you want to run every frame, put it in the update function.
        '''
        from teon.text import Text
        
        self._entity_counter_text = Text(text = f"Entities: {len(self.entities)}",position = (0,0),size = 30,tags = ["_entity_counter_text"],anchor = "topright",window_anchor = "topright",z = 100,antialias = True)
        
        if update_func != None:
            self.update = update_func
        
        if input_func != None:
            self.input = input_func

        while True:
            
            if len(Teon._instances) > 1:
                raise teon.other.TeonCError("More than one Teon class was initiated!")
            self.mouse.wheel.up = False
            self.mouse.wheel.down = False
            for event in pygame.event.get():
                self._event(event)

                if event.type == pygame.QUIT:
                    self.quit()
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 4 and not self.restrict["wheel up"]:
                        self.mouse.wheel.up = True
                        
                    elif event.button == 5 and not self.restrict["wheel down"]:
                        self.mouse.wheel.down = True

                if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                    key_pressed = event.key if event.type == pygame.KEYDOWN else event.button
                    key_pressed_time = time.time()
                
                elif event.type == pygame.KEYUP or event.type == pygame.MOUSEBUTTONUP:
                    if key_pressed != None:
                        key_released = event.key if event.type == pygame.KEYUP else event.button
                        if key_pressed == key_released:
                            key_released_time = time.time()
                            if key_released_time - key_pressed_time <= self.key_press_time and rt_key(key_pressed) in self.restrict and not self.restrict[rt_key(key_pressed)]:
                                for entity in self.entities:
                                    entity.input(rt_key(key_pressed))
                                self.input(rt_key(key_pressed))
                                self._input(rt_key(key_pressed))
            
                                
                        key_pressed = None

            self.mouse._update()

            self.window.display.fill(self.background_color)
            self.dt = self.time.tick(self.window.fps) / 1000

            if self.entity_counter:
                self._entity_counter_text.text = f"Entities: {len(self.entities)}"
            self._entity_counter_text.visible = self.entity_counter

            if self.dt != 0:
                self.true_fps = 1 / self.dt

            if self.aspect_borders:
                self._entity_counter_text.position = (1,0)
            else:
                self._entity_counter_text.position = (0,0)

            for entity in Entity.level_editor.active_level.entities:
                if entity.has_tag("dt"):
                    entity.dt = self.dt

            self.level_editor.lvldyt()
            self.level_editor.update()
            self.level_editor.draw(self.window)

            self.update()

            if self.debug:
                for entity in self.level_editor.active_level.entities:
                    debug_collider(entity.collider,self.camera.position)
                    if hasattr(entity,"colliders") and len(entity.colliders) > 0:
                        for _,collider in entity.colliders.items():
                            if not entity.collider.collidable:
                                debug_collider(collider,self.camera.position,(0,0,255))
                            else:
                                debug_collider(collider,self.camera.position)
            else:
                for entity in self.level_editor.active_level.entities:
                    if entity.collider.visible:
                        debug_collider(entity.collider,self.camera.position)
                    if hasattr(entity,"colliders") and len(entity.colliders) > 0:
                        for _,collider in entity.colliders.items():
                            if collider.visible:
                                if not entity.collider.collidable:
                                    debug_collider(collider,self.camera.position,(0,0,255))
                                else:
                                    debug_collider(collider,self.camera.position)

            if self.aspect_borders and not self._left_border == -1:
                pygame.draw.rect(self.window.display,teon.functions._get_color_value(self.aspect_borders_color),self._left_border)
                pygame.draw.rect(self.window.display,teon.functions._get_color_value(self.aspect_borders_color),self._right_border)

            pygame.display.update()

def debug_collider(collider,cam_pos,color = (255,0,0),**kwargs):
    '''
    Don't use this. IT WILL CRASH! \n
    jk
    '''
    if collider.shape == "square":
        if collider.parent.is_ui:
            collider = pygame.Rect(collider.x + Teon._offset[0],collider.y + Teon._offset[1],collider.width,collider.height)
        else:
            collider = pygame.Rect(collider.x - cam_pos.x * 2 + 500 * teon.functions.scale_def(),collider.y - cam_pos.y * 2 + 600 * teon.functions.scale_def(),collider.width,collider.height)
        pygame.draw.rect(pygame.display.get_surface(),collider.color,collider,kwargs.get("thickness",2))
        if collider.name is not None:
            text = teon.Text(text = collider.name,size = kwargs.get("size",10),color = collider.color)
            text.anchor = "center"
    else:
        if collider.parent.is_ui:
            pygame.draw.circle(pygame.display.get_surface(),color,(100,100),collider.radius,2)
        else:
            pygame.draw.circle(pygame.display.get_surface(),color,(collider.centerx - cam_pos.x * 2 + 500 * teon.functions.scale_def(),collider.centery - cam_pos.y * 2 + 600 * teon.functions.scale_def()),collider._radius,2)

def get_main_class():
    return Teon._instances[0]