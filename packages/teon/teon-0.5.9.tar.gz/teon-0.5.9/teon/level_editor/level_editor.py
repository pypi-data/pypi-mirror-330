from teon import *
from teon.extra.controller import PlayerController2D
import pygame
import os
from ast import literal_eval

def get_relative_path(base_path, target_path):
    if target_path == None:
        return None
    base_path = os.path.normpath(base_path)
    target_path = os.path.normpath(target_path)
    base_path_lower = base_path.lower()
    target_path_lower = target_path.lower()
    if not base_path_lower.endswith(os.sep):
        base_path_lower += os.sep
    if target_path_lower.startswith(base_path_lower):
        return target_path[len(base_path):].lstrip(os.sep)
    return target_path

class REntity(Entity):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self._actual_visible = True
        self._actual_collidable = True

        self.ghost = GhostIcon(self)

    @property
    def actual_collidable(self):
        return self._actual_collidable
    
    @actual_collidable.setter
    def actual_collidable(self,value):
        self._actual_collidable = value

    @property
    def actual_visible(self):
        return self._actual_visible
    
    @actual_visible.setter
    def actual_visible(self,boolean):
        self._actual_visible = boolean
        if boolean:
            self.alpha = 1
        else:
            self.alpha = 0.6

class ScaleXText(Text):
    def __init__(self,console):
        self.console = console
        text = ""
        self.other_text = Text(size = 13,antialias = True,z = 104,color = "white",font = load_font("fonts/font.ttf"),anchor = "midleft")
        self.value = None
        if self.console.level.last_entity != None:
            text = f"{self.console.level.last_entity.scale.x}"
            self.value = self.console.level.last_entity.scale.x
        self.other_text.text = text
        super().__init__(position = (0.811,0.683),text = "X: ",anchor = "topleft",z = 103,antialias = True,size = 17,font = load_font("fonts/font.ttf"),parent = console.panel)
        self.other_text.parent = self
        self.other_text.position = (self.position.x + 0.021,self.position.y + 0.02)
        self.colli = Widget(position = (self.position.x + 0.018,self.position.y + 0.004),z = 103,scale = (0.6,0.17),anchor = "topleft",visible = True,parent = self,image = load_image("images/textbox.png"))
        self.colli_images = [load_image("images/textbox.png"),load_image("images/textbox2.png")]
        self.mode = False

        self.numbers = [f"{i}" for i in range(10)]

        self.last_value = self.value

    def input(self,key):
        get_main_class().restrict["b"] = self.mode
        if key == "left mouse" and self.colli.hovered and self.value != None:
            self.mode = True
        elif (((key == "left mouse" or key == "right mouse") and not self.colli.hovered) or key == "enter") and self.mode:
            self.mode = False
            try:
                self.value = float(self.value)
                self.console.level.last_entity.scale.x = self.value
            except:
                self.value = self.last_value
                self.console.level.last_entity.scale.x = self.value

            self.other_text.text = str(self.value)

        if self.mode:
            self.colli.image = self.colli_images[1]
            self.value = str(self.value)
            
            if key in self.numbers:
                self.value += key
            
            if key == "period":
                self.value += "."
            
            if key == "backspace":
                self.value = self.value[:-1]

            if key == "minus":
                if self.value == "":
                    self.value = "-"

            self.other_text.text = self.value
        else:
            self.colli.image = self.colli_images[0]

    def update(self):
        super().update()
        
        if not self.mode:
            if self.console.level.last_entity == None:
                self.other_text.text = ""
                self.value = None
            else: 
                self.other_text.text = f"{self.console.level.last_entity.scale.x}"
                self.value = self.console.level.last_entity.scale.x
            self.last_value = self.value

class GhostIcon(Entity):
    def __init__(self,parent):
        super().__init__(anchor = "topleft",parent = parent,scale = (0.1,0.1),image = load_image("images/ghost_icon.png"),visible = parent.actual_collidable,position = (parent.position.x - (parent.collider.width / (2 * scale_def())),parent.position.y - (parent.collider.height / (2 * scale_def()))),z = parent.z+1)

    def update(self):
        super().update()
        self.visible = not self.parent.actual_collidable
        self.position = self.parent.topleft
        self.z = self.parent.z + 1 
        self.alpha = self.parent.alpha

class ScaleYText(Text):
    def __init__(self,console):
        self.console = console
        text = ""
        self.other_text = Text(size = 13,antialias = True,z = 104,color = "white",font = load_font("fonts/font.ttf"),anchor = "midleft")
        self.value = None
        if self.console.level.last_entity != None:
            text = f"{self.console.level.last_entity.scale.y}"
            self.value = self.console.level.last_entity.scale.y
        self.other_text.text = text
        super().__init__(position = (0.9,0.683),text = "Y: ",anchor = "topleft",z = 103,antialias = True,size = 17,font = load_font("fonts/font.ttf"),parent = console.panel)
        self.other_text.parent = self
        self.other_text.position = (self.position.x + 0.021,self.position.y + 0.02)
        self.colli = Widget(position = (self.position.x + 0.018,self.position.y + 0.004),z = 103,scale = (0.6,0.17),anchor = "topleft",visible = True,parent = self,image = load_image("images/textbox.png"))
        self.colli_images = [load_image("images/textbox.png"),load_image("images/textbox2.png")]
        self.mode = False

        self.numbers = [f"{i}" for i in range(10)]

        self.last_value = self.value
    def input(self,key):
        get_main_class().restrict["b"] = self.mode
        if key == "left mouse" and self.colli.hovered and self.value != None:
            self.mode = True
        elif (((key == "left mouse" or key == "right mouse") and not self.colli.hovered) or key == "enter") and self.mode:
            self.mode = False
            try:
                self.value = float(self.value)
                self.console.level.last_entity.scale.y = self.value
            except:
                self.value = self.last_value
                self.console.level.last_entity.scale.y = self.value

            self.other_text.text = str(self.value)

        if self.mode:
            self.colli.image = self.colli_images[1]
            self.value = str(self.value)
            
            if key in self.numbers:
                self.value += key
            
            if key == "period":
                self.value += "."
            
            if key == "backspace":
                self.value = self.value[:-1]

            if key == "minus":
                if self.value == "":
                    self.value = "-"

            self.other_text.text = self.value
        else:
            self.colli.image = self.colli_images[0]

    def update(self):
        super().update()
        if not self.mode:
            if self.console.level.last_entity == None:
                self.other_text.text = ""
                self.value = None
            else: 
                self.other_text.text = f"{self.console.level.last_entity.scale.y}"
                self.value = self.console.level.last_entity.scale.y
            self.last_value = self.value

class AnchorSetter(Widget):
    def __init__(self,console):
        self.console = console
        super().__init__(parent = console.board,position = (0.852,0.861),scale = 0.7,z = 105,visible = False,anchor = "topleft")
        self.text = Text(text = "Anch:",size = 15,position = (self.position.x - 0.04,self.position.y -0.03),z = 104,antialias = True,anchor = "topleft",font = load_font("fonts/font.ttf"),parent = self)
        self.images = [load_image(f"images/anchor{i}.png") for i in range(0,10)]

        self.open = False
        self.index = 4

        self.button_images0 = [load_image("images/anchor_topleft0.png"),
                              load_image("images/anchor_midtop0.png"),
                              load_image("images/anchor_topright0.png"),
                              load_image("images/anchor_midleft0.png"),
                              load_image("images/anchor_center0.png"),
                              load_image("images/anchor_midright0.png"),
                              load_image("images/anchor_bottomleft0.png"),
                              load_image("images/anchor_midbottom0.png"),
                              load_image("images/anchor_bottomright0.png")]

        self.button_images1 = [load_image("images/anchor_topleft1.png"),
                               load_image("images/anchor_midtop1.png"),
                               load_image("images/anchor_topright1.png"),
                               load_image("images/anchor_midleft1.png"),
                               load_image("images/anchor_center1.png"),
                               load_image("images/anchor_midright1.png"),
                               load_image("images/anchor_bottomleft1.png"),
                               load_image("images/anchor_midbottom1.png"),
                               load_image("images/anchor_bottomright1.png")]

        self.button = Widget(position = (self.position.x + 0.035,self.position.y - 0.0121),scale = (0.5,0.5 / 3.5),parent = self,z = 104)

        self.anchors = ["topleft","midtop","topright","midleft","center","midright","bottomleft","midbottom","bottomright"]

        self.colliders["topleft"] = SquareCollider(self,(0,0),(0.333,0.333))
        self.colliders["midtop"] = SquareCollider(self,(23,0),(0.333,0.333))
        self.colliders["topright"] = SquareCollider(self,(46,0),(0.333,0.333))
        self.colliders["midleft"] = SquareCollider(self,(0,23),(0.333,0.333))
        self.colliders["center"] = SquareCollider(self,(23,23),(0.333,0.333))
        self.colliders["midright"] = SquareCollider(self,(46,23),(0.333,0.333))
        self.colliders["bottomleft"] = SquareCollider(self,(0,46),(0.333,0.333))
        self.colliders["midbottom"] = SquareCollider(self,(23,46),(0.333,0.333))
        self.colliders["bottomright"] = SquareCollider(self,(46,46),(0.333,0.333))

    def input(self,key):
        if (key == "left mouse" or key == "right mouse") and not self.hovered and self.open:
            self.visible = False
            self.open = False
        if key == "left mouse" and self.button.hovered and self.button.visible:
            self.open = not self.open
            self.visible = self.open
        if self.open and key == "left mouse" and self.hovered:
            self.open = False
            self.visible = False
            self.console.level.last_entity.anchor = self.anchors[self.index]
        

    def update(self):
        super().update()
        if self.console.level.last_entity:
            self.button.visible = True
        else:
            self.button.visible = False
        if self.button.hovered:
            self.button.image = self.button_images1[self.index]
        else:
            self.button.image = self.button_images0[self.index]
        if self.console.level.last_entity:
            self.index = self.anchors.index(self.console.level.last_entity.anchor)
            self.image = self.images[self.index + 1]
            if self.open:
                if self.hovered:
                    for  itm,collider in self.colliders.items():
                        if collider.hovered:
                            self.image = self.images[self.anchors.index(itm) + 1]
                            self.index = self.anchors.index(itm)

class SMP(Widget):
    def __init__(self,console):
        super().__init__(position = (0.694,0.019),image = load_image("images/s0.png"),anchor = "topleft",scale = (0.6,0.2),parent = console.panel)
        self.images = [load_image(f"images/s{i}.png") for i in range(13)]
        self.console = console

        self.colliders["left"] = SquareCollider(self,(0,0),(0.3433,1))
        self.colliders["middle"] = SquareCollider(self,(20,0),(0.3333,1))
        self.colliders["right"] = SquareCollider(self,(40,0),(0.3433,1))

        self.mode = 2

    def input(self,key):
        if key == "left mouse" and self.hovered:
            if self.colliders["left"].hovered:
                self.mode = 0
            elif self.colliders["middle"].hovered:
                self.mode = 1
            elif self.colliders["right"].hovered:
                self.mode = 2

    def update(self):
        super().update()
        if self.hovered:
            if self.mode == 0:
                if self.colliders["left"].hovered:
                    self.image = self.images[4]
                elif self.colliders["middle"].hovered:
                    self.image = self.images[5]
                elif self.colliders["right"].hovered:
                    self.image = self.images[6]
            elif self.mode == 1:
                if self.colliders["left"].hovered:
                    self.image = self.images[8]
                elif self.colliders["middle"].hovered:
                    self.image = self.images[7]
                elif self.colliders["right"].hovered:
                    self.image = self.images[9]
            elif self.mode == 2:
                if self.colliders["left"].hovered:
                    self.image = self.images[11]
                elif self.colliders["middle"].hovered:
                    self.image = self.images[12]
                elif self.colliders["right"].hovered:
                    self.image = self.images[10]
        else:
            if self.mode == 1:
                self.image = self.images[7]
            elif self.mode == 2:
                self.image = self.images[10]
            else:
                self.image = self.images[4]

class ClassText(Text):
    def __init__(self,console):
        self.console = console
        text = ""
        self.other_text = Text(size = 11,antialias = True,z = 104,color = "white",font = load_font("fonts/font.ttf"),anchor = "midleft")
        self.value = None
        if self.console.level.last_entity != None:
            text = f"{self.console.level.last_entity.actual_class}"
            self.value = self.console.level.last_entity.actual_class
        self.other_text.text = text
        super().__init__(position = (0.811,0.795),text = "Class: ",anchor = "topleft",z = 103,antialias = True,size = 15,font = load_font("fonts/font.ttf"),parent = console.panel)
        self.other_text.parent = self
        self.other_text.position = (self.position.x + 0.053,self.position.y + 0.018)
        self.colli = Widget(position = (self.position.x + 0.049,self.position.y + 0.004),z = 103,scale = (0.8340,0.15),anchor = "topleft",visible = True,parent = self,image = load_image("images/textbox.png"))
        self.colli_images = [load_image("images/textbox.png"),load_image("images/textbox2.png")]
        self.mode = False

        self.allowed = 'abcdefghijklmnopqrstuvwxyz1234567890_'

        self.last_value = self.value
    def input(self,key):
        if key == "left mouse" and self.colli.hovered and self.value != None:
            self.mode = True
        elif (((key == "left mouse" or key == "right mouse") and not self.colli.hovered) or key == "enter") and self.mode:
            self.mode = False
            try:
                self.console.level.last_entity.actual_class = self.value
            except:
                self.value = self.last_value
                self.console.level.last_entity.actual_class = self.value

            self.other_text.text = str(self.value)

        if self.mode:
            self.colli.image = self.colli_images[1]
            self.value = str(self.value)
            
            if key in self.allowed:
                if key_pressed("left shift") and key in 'abcdefghijklmnopqrstuvwxyz':
                    self.value += str(key).capitalize()
                elif not key_pressed('left shift'):
                    self.value += key
            
            if key == "backspace":
                self.value = self.value[:-1]

            self.other_text.text = self.value
        else:
            self.colli.image = self.colli_images[0]

    def update(self):
        super().update()
        if not self.mode:
            if self.console.level.last_entity == None:
                self.other_text.text = ""
                self.value = None
            else: 
                self.other_text.text = f"{self.console.level.last_entity.actual_class}"
                self.value = self.console.level.last_entity.actual_class
            self.last_value = self.value

class SnapToGrid(Widget):
    def __init__(self,console):
        super().__init__(position = (0.768,0.019),anchor = "topleft",scale = 0.2,z = 100,image = load_image("images/stg0.png"),parent = console.panel)
        self.is_ui = True
        self.console = console

        self.images = [load_image("images/stg0.png"), load_image("images/stg1.png"), load_image("images/stg2.png")]

        self.on = False

    def input(self,key):
        if key == "left mouse" and self.hovered:
            self.on = not self.on
            if self.on:
                self.image = self.images[2]

    def update(self):
        super().update()
        if not self.on:
            if self.hovered:
                self.image = self.images[1]
            else:
                self.image = self.images[0]

class PositionZText(Text):
    def __init__(self,console):
        self.console = console
        text = ""
        self.other_text = Text(size = 13,antialias = True,z = 104,color = "white",font = load_font("fonts/font.ttf"),anchor = "midleft")
        self.value = None
        if self.console.level.last_entity != None:
            text = f"{self.console.level.last_entity.z}"
            self.value = self.console.level.last_entity.z
        self.other_text.text = text
        super().__init__(position = (0.811,0.755),text = "Z: ",anchor = "topleft",z = 103,antialias = True,size = 17,font = load_font("fonts/font.ttf"),parent = console.panel)
        self.other_text.parent = self
        self.other_text.position = (self.position.x + 0.02,self.position.y + 0.02)
        self.colli = Widget(position = (self.position.x + 0.017,self.position.y + 0.004),z = 103,scale = (0.6,0.17),anchor = "topleft",visible = True,parent = self,image = load_image("images/textbox.png"))
        self.colli_images = [load_image("images/textbox.png"),load_image("images/textbox2.png")]
        self.mode = False

        self.numbers = [f"{i}" for i in range(10)]

        self.last_value = self.value
    def input(self,key):
        if key == "left mouse" and self.colli.hovered and self.value != None:
            self.mode = True
        elif (((key == "left mouse" or key == "right mouse") and not self.colli.hovered) or key == "enter") and self.mode:
            self.mode = False
            try:
                self.value = int(self.value)
                self.console.level.last_entity.z = self.value
            except:
                self.value = self.last_value
                self.console.level.last_entity.z = self.value

            self.other_text.text = str(self.value)

        if self.mode:
            self.colli.image = self.colli_images[1]
            self.value = str(self.value)
            
            if key in self.numbers:
                self.value += key
            
            if key == "backspace":
                self.value = self.value[:-1]

            if key == "minus":
                if self.value == "":
                    self.value = "-"

            self.other_text.text = self.value
        else:
            self.colli.image = self.colli_images[0]

    def update(self):
        super().update()
        if not self.mode:
            if self.console.level.last_entity == None:
                self.other_text.text = ""
                self.value = None
            else: 
                self.other_text.text = f"{self.console.level.last_entity.z}"
                self.value = self.console.level.last_entity.z
            self.last_value = self.value

class PositionXText(Text):
    def __init__(self,console):
        self.console = console
        text = ""
        self.other_text = Text(size = 13,antialias = True,z = 104,color = "white",font = load_font("fonts/font.ttf"),anchor = "midleft")
        self.value = None
        if self.console.level.last_entity != None:
            text = f"{self.console.level.last_entity.position.x}"
            self.value = self.console.level.last_entity.position.x
        self.other_text.text = text
        super().__init__(position = (0.811,0.63),text = "X: ",anchor = "topleft",z = 103,antialias = True,size = 17,font = load_font("fonts/font.ttf"),parent = console.panel)
        self.other_text.parent = self
        self.other_text.position = (self.position.x + 0.021,self.position.y + 0.02)
        self.colli = Widget(position = (self.position.x + 0.018,self.position.y + 0.004),z = 103,scale = (0.6,0.17),anchor = "topleft",visible = True,parent = self,image = load_image("images/textbox.png"))
        self.colli_images = [load_image("images/textbox.png"),load_image("images/textbox2.png")]
        self.mode = False

        self.numbers = [f"{i}" for i in range(10)]

        self.last_value = self.value
    def input(self,key):
        if key == "left mouse" and self.colli.hovered and self.value != None:
            self.mode = True
        elif (((key == "left mouse" or key == "right mouse") and not self.colli.hovered) or key == "enter") and self.mode:
            self.mode = False
            try:
                self.value = int(self.value)
                self.console.level.last_entity.position.x = self.value
            except:
                self.value = self.last_value
                self.console.level.last_entity.position.x = self.value

            self.other_text.text = str(self.value)

        if self.mode:
            self.colli.image = self.colli_images[1]
            self.value = str(self.value)
            
            if key in self.numbers:
                self.value += key
            
            if key == "backspace":
                self.value = self.value[:-1]

            if key == "minus":
                if self.value == "":
                    self.value = "-"

            self.other_text.text = self.value
        else:
            self.colli.image = self.colli_images[0]

    def update(self):
        super().update()
        if not self.mode:
            if self.console.level.last_entity == None:
                self.other_text.text = ""
                self.value = None
            else: 
                self.other_text.text = f"{self.console.level.last_entity.position.x}"
                self.value = self.console.level.last_entity.position.x
            self.last_value = self.value

class PositionYText(Text):
    def __init__(self,console):
        self.console = console
        text = ""
        self.other_text = Text(size = 13,antialias = True,z = 104,color = "white",font = load_font("fonts/font.ttf"),anchor = "midleft")
        self.value = None
        if self.console.level.last_entity != None:
            text = f"{self.console.level.last_entity.position.y}"
            self.value = self.console.level.last_entity.position.y
        self.other_text.text = text
        super().__init__(position = (0.9,0.63),text = "Y: ",anchor = "topleft",z = 103,antialias = True,size = 17,font = load_font("fonts/font.ttf"),parent = console.panel)
        self.other_text.parent = self
        self.other_text.position = (self.position.x + 0.021,self.position.y + 0.02)
        self.colli = Widget(position = (self.position.x + 0.018,self.position.y + 0.004),z = 103,scale = (0.6,0.17),anchor = "topleft",visible = True,parent = self,image = load_image("images/textbox.png"))
        self.colli_images = [load_image("images/textbox.png"),load_image("images/textbox2.png")]
        self.mode = False

        self.numbers = [f"{i}" for i in range(10)]

        self.last_value = self.value

    def input(self,key):
        if key == "left mouse" and self.colli.hovered and self.value != None:
            self.mode = True
        elif (((key == "left mouse" or key == "right mouse") and not self.colli.hovered) or key == "enter") and self.mode:
            self.mode = False
            try:
                self.value = int(self.value)
                self.console.level.last_entity.position.y = self.value
            except:
                self.value = self.last_value
                self.console.level.last_entity.position.y = self.value

            self.other_text.text = str(self.value)

        if self.mode:
            self.colli.image = self.colli_images[1]
            self.value = str(self.value)
            
            if key in self.numbers:
                self.value += key
            
            if key == "backspace":
                self.value = self.value[:-1]

            if key == "minus":
                if self.value == "":
                    self.value = "-"

            self.other_text.text = self.value
        else:
            self.colli.image = self.colli_images[0]

    def update(self):
        super().update()
        if not self.mode:
            if self.console.level.last_entity == None:
                self.other_text.text = ""
                self.value = None
            else: 
                self.other_text.text = f"{self.console.level.last_entity.position.y}"
                self.value = self.console.level.last_entity.position.y
            self.last_value = self.value

class Texts:
    def __init__(self,console):
        self.console = console
        self.posx = PositionXText(self.console)
        self.posy = PositionYText(self.console)
        Text(anchor = "topleft",position = (0.811,0.619),z = 104,size = 12,antialias = True,text = "Position",parent = self.console.panel)

        self.sclx = ScaleXText(self.console)
        self.scly = ScaleYText(self.console)
        Text(anchor = "topleft",position = (0.811,0.672),z = 104,size = 12,antialias = True,text = "Scale",parent = self.console.panel)

        self.posz = PositionZText(self.console)

        self.clas = ClassText(self.console)

class BoolPanel(Widget):
    def __init__(self,parent,position,stater):
        super().__init__(parent = parent,position = position,image = load_image("images/bool_up0.png"),scale = (0.3,0.143),anchor = "topleft",z = 104)
        self.images = [load_image("images/bool_up0.png"),
                       load_image("images/bool_up1.png"),
                       load_image("images/bool_down00.png"),
                       load_image("images/bool_down01.png"),
                       load_image("images/bool_down02.png"),
                       load_image("images/bool_down10.png"),
                       load_image("images/bool_down11.png"),
                       load_image("images/bool_down12.png")]
        
        self.colliders["top"] = SquareCollider(self,(0,0),(1,0.5),scalable = True)
        self.colliders["bottom"] = SquareCollider(self,(0,50),(1,0.5),scalable = True)

        self.stater = stater

        self.state = True
        self.open = False

    def input(self,key):
        if self.open and self.colliders["bottom"].hovered and key == "left mouse" and self.parent.console.level.last_entity:
            self.state = not self.state
            self.open = False
            self.parent.act(self.state)
            return
        if key == "left mouse" and self.hovered:
            self.open = not self.open
        if not self.hovered:
            self.open = False

    def update(self):
        super().update()
        if self.parent.console.level.last_entity:
            if self.stater == "collidable":
                self.state = self.parent.console.level.last_entity.actual_collidable
            elif self.stater == "visible":
                self.state = self.parent.console.level.last_entity.actual_visible
            else:
                self.state = self.parent.console.level.last_entity.actual_class
            self.visible = True
            if self.open:
                self.scale.y = 0.2861
                if self.state:
                    if self.colliders["top"].hovered:
                        self.image = self.images[3]
                    elif self.colliders["bottom"].hovered:
                        self.image = self.images[4]
                    else:
                        self.image = self.images[2]
                else:
                    if self.colliders["top"].hovered:
                        self.image = self.images[6]
                    elif self.colliders["bottom"].hovered:
                        self.image = self.images[7]
                    else:
                        self.image = self.images[5]
            else:
                self.scale.y = 0.143
                if self.state:
                    self.image = self.images[0]
                else:
                    self.image = self.images[1]
        else:
            self.visible = False

class VisibleSetter(Text):
    def __init__(self,console):
        super().__init__(parent = console.panel,position = (0.811,0.73),anchor = "topleft",text = "Visible:",size = 16,z = 104,antialias = True)
        self.bool_panel = BoolPanel(self,(self.position.x + 0.042,self.position.y - 0.004),"visible")
        self.console = console

    def act(self,state):
        self.console.level.last_entity.actual_visible = state

class CollidableSetter(Text):
    def __init__(self,console):
        super().__init__(parent = console.panel,position = (0.895,0.73),anchor = "topleft",text = "Collidable:",size = 16,z = 104,antialias = True)
        self.bool_panel = BoolPanel(self,(self.position.x + 0.06,self.position.y - 0.004),"collidable")
        self.console = console

    def act(self,state):
        self.console.level.last_entity.actual_collidable = state

class ImportButton(Widget):
    def __init__(self,console):
        super().__init__(parent = console.panel,anchor = "topleft",position = (0.811,0.019),scale = (0.7,0.2),z = 101,image = load_image("images/import0.png"))
        self.images = [load_image(f"images/import{i}.png") for i in range(0,2)]
        self.console = console

    def input(self,key):
        if key == "left mouse" and self.hovered:
            from tkinter import filedialog
            file_path = filedialog.askopenfilename(title="Select an Image",filetypes=[("Select Image or Level File", "*.png;*.jpg;*.jpeg;*.dat"), ("All Files", "*.*")])
            if file_path != "":
                path1 = file_path.split(".")
                if path1[-1] == "dat":
                    self.console.level.add_level(file_path)
                elif "png" in path1[-1] or "jpg" in path1[-1] or "jpeg" in path1[-1]:
                    self.console.board.add_image(file_path)
            

    def update(self):
        super().update()
        if self.hovered:
            self.image = self.images[1]
        else:
            self.image = self.images[0]

class ExportButton(Widget):
    def __init__(self,console):
        super().__init__(parent = console.panel,anchor = "topleft",position = (0.89,0.019),scale = (0.7,0.2),z = 101,image = load_image("images/export0.png"))
        self.images = [load_image(f"images/export{i}.png") for i in range(0,2)]
        self.console = console
        self.folder_path = ""

    def input(self,key):
        if key == "left mouse" and self.hovered:
            import tkinter as tk
            from tkinter import filedialog, messagebox

            def save_dat_file():
                # Create the root Tkinter window
                root = tk.Tk()
                root.withdraw()  # Hide the root window

                # Open a Save As dialog
                file_path = filedialog.asksaveasfilename(
                    title="Save As",
                    defaultextension=".dat",
                    filetypes=[("DAT files", "*.dat"), ("All files", "*.*")]
                )

                if not file_path:  # User pressed cancel or closed the dialog
                    return
                
                self.console.level.export(file_path)

            # Call the function
            save_dat_file()
    
    def update(self):
        super().update()
        if self.hovered:
            self.image = self.images[1]
        else:
            self.image = self.images[0]

class FolderButton(Widget):
    def __init__(self,console):
        super().__init__(parent = console.panel,anchor = "topleft",position = (0.969,0.019),scale = 0.2,z = 101,image = load_image("images/folder0.png"))
        self.images = [load_image(f"images/folder{i}.png") for i in range(0,2)]
        self.console = console
        self.folder_path = ""

        self.text = Text(parent = self,position = (0.811,0.0745),anchor = "midleft",z = 101,text = f"Folder: {self.folder_path}",size = 11,antialias = True)

    def input(self,key):
        if key == "left mouse" and self.hovered:
            from tkinter import filedialog

            folder_path = filedialog.askdirectory()

            self.folder_path = folder_path

            self.text.text = f"Folder: {self.get_folder(self.folder_path)}"

    def get_folder(self,strr:str):
        strr = strr.split("/")
        try:
            return f"{strr[-2]}/{strr[-1]}"
        except:
            return strr[-1]

    def update(self):
        super().update()
        if self.hovered:
            self.image = self.images[1]
        else:
            self.image = self.images[0]

class DeletePanel(Widget):
    def __init__(self,parent):
        super().__init__(position = (0.5,0.5),scale = (0.6,0.4),visible = False,z = 103,anchor = "topleft",parent = parent,image = load_image("images/delete0.png"))
        self.colliders = {"top":SquareCollider(self,(0,0),(1,0.5)),"bottom":SquareCollider(self,(0,20),(1,0.5))}

        self.images = [load_image(f"images/delete{i}.png") for i in range(0,3)]

        self.state = [False,False]

    def update(self):
        super().update()
        if not self.hovered:
            self.image = self.images[0]
            self.state = [False,False]
        elif self.colliders["top"].hovered:
            self.image = self.images[1]
            self.state = [True,False]
        elif self.colliders["bottom"].hovered:
            self.image = self.images[2]
            self.state = [False,True]
        
class Board(Widget):
    def __init__(self,console):
        super().__init__(position = (0.9,0.35),scale = (0.5724 * 3.1,1 * 3.1),z = 102,image = load_image("images/board0.png"),parent = console.panel)
        self.images = [load_image(f"images/board{i}.png") for i in range(0,29)]
        
        self.console = console

        self.index = None

        self.delete_panel = DeletePanel(self)

        self.defaults = [[(1,1),True,True,"Entity",0,"center"] for _ in range(28)]
        self.image_files = [None for _ in range(len(self.images) - 2)]
        self.buttons = [Widget(position = (0.8340,0.1300),z = 101,parent = self,scale = 0.445,anchor = "center",tags = [0,None],visible = False),
                        Widget(position = (0.8780,0.1300),z = 101,parent = self,scale = 0.445,anchor = "center",tags = [1,None],visible = False),
                        Widget(position = (0.9230,0.1300),z = 101,parent = self,scale = 0.445,anchor = "center",tags = [2,None],visible = False),
                        Widget(position = (0.9665,0.1300),z = 101,parent = self,scale = 0.445,anchor = "center",tags = [3,None],visible = False),
                        Widget(position = (0.8340,0.2038),z = 101,parent = self,scale = 0.445,anchor = "center",tags = [4,None],visible = False),
                        Widget(position = (0.8780,0.2038),z = 101,parent = self,scale = 0.445,anchor = "center",tags = [5,None],visible = False),
                        Widget(position = (0.9230,0.2038),z = 101,parent = self,scale = 0.445,anchor = "center",tags = [6,None],visible = False),
                        Widget(position = (0.9665,0.2038),z = 101,parent = self,scale = 0.445,anchor = "center",tags = [7,None],visible = False),
                        Widget(position = (0.8340,0.2770),z = 101,parent = self,scale = 0.445,anchor = "center",tags = [8,None],visible = False),
                        Widget(position = (0.8780,0.2770),z = 101,parent = self,scale = 0.445,anchor = "center",tags = [9,None],visible = False),
                        Widget(position = (0.9230,0.2770),z = 101,parent = self,scale = 0.445,anchor = "center",tags = [10,None],visible = False),
                        Widget(position = (0.9665,0.2770),z = 101,parent = self,scale = 0.445,anchor = "center",tags = [11,None],visible = False),
                        Widget(position = (0.8340,0.3502),z = 101,parent = self,scale = 0.445,anchor = "center",tags = [12,None],visible = False),
                        Widget(position = (0.8780,0.3502),z = 101,parent = self,scale = 0.445,anchor = "center",tags = [13,None],visible = False),
                        Widget(position = (0.9230,0.3502),z = 101,parent = self,scale = 0.445,anchor = "center",tags = [14,None],visible = False),
                        Widget(position = (0.9665,0.3502),z = 101,parent = self,scale = 0.445,anchor = "center",tags = [15,None],visible = False),
                        Widget(position = (0.8340,0.4234),z = 101,parent = self,scale = 0.445,anchor = "center",tags = [16,None],visible = False),
                        Widget(position = (0.8780,0.4234),z = 101,parent = self,scale = 0.445,anchor = "center",tags = [17,None],visible = False),
                        Widget(position = (0.9230,0.4234),z = 101,parent = self,scale = 0.445,anchor = "center",tags = [18,None],visible = False),
                        Widget(position = (0.9665,0.4234),z = 101,parent = self,scale = 0.445,anchor = "center",tags = [19,None],visible = False),
                        Widget(position = (0.8340,0.4966),z = 101,parent = self,scale = 0.445,anchor = "center",tags = [20,None],visible = False),
                        Widget(position = (0.8780,0.4996),z = 101,parent = self,scale = 0.445,anchor = "center",tags = [21,None],visible = False),
                        Widget(position = (0.9230,0.4996),z = 101,parent = self,scale = 0.445,anchor = "center",tags = [22,None],visible = False),
                        Widget(position = (0.9665,0.4996),z = 101,parent = self,scale = 0.445,anchor = "center",tags = [23,None],visible = False),
                        Widget(position = (0.8340,0.5698),z = 101,parent = self,scale = 0.445,anchor = "center",tags = [24,None],visible = False),
                        Widget(position = (0.8780,0.5698),z = 101,parent = self,scale = 0.445,anchor = "center",tags = [25,None],visible = False),
                        Widget(position = (0.9230,0.5698),z = 101,parent = self,scale = 0.445,anchor = "center",tags = [26,None],visible = False),
                        Widget(position = (0.9665,0.5698),z = 101,parent = self,scale = 0.445,anchor = "center",tags = [27,None],visible = False)]
        
        self.image_buttons = [Widget(position = (0.8340,0.1300),z = 101,parent = self,scale = 0.445,anchor = "center",tags = [0,None],visible = False),
                              Widget(position = (0.8780,0.1300),z = 101,parent = self,scale = 0.445,anchor = "center",tags = [1,None],visible = False),
                              Widget(position = (0.9230,0.1300),z = 101,parent = self,scale = 0.445,anchor = "center",tags = [2,None],visible = False),
                              Widget(position = (0.9665,0.1300),z = 101,parent = self,scale = 0.445,anchor = "center",tags = [3,None],visible = False),
                              Widget(position = (0.8340,0.2038),z = 101,parent = self,scale = 0.445,anchor = "center",tags = [4,None],visible = False),
                              Widget(position = (0.8780,0.2038),z = 101,parent = self,scale = 0.445,anchor = "center",tags = [5,None],visible = False),
                              Widget(position = (0.9230,0.2038),z = 101,parent = self,scale = 0.445,anchor = "center",tags = [6,None],visible = False),
                              Widget(position = (0.9665,0.2038),z = 101,parent = self,scale = 0.445,anchor = "center",tags = [7,None],visible = False),
                              Widget(position = (0.8340,0.2770),z = 101,parent = self,scale = 0.445,anchor = "center",tags = [8,None],visible = False),
                              Widget(position = (0.8780,0.2770),z = 101,parent = self,scale = 0.445,anchor = "center",tags = [9,None],visible = False),
                              Widget(position = (0.9230,0.2770),z = 101,parent = self,scale = 0.445,anchor = "center",tags = [10,None],visible = False),
                              Widget(position = (0.9665,0.2770),z = 101,parent = self,scale = 0.445,anchor = "center",tags = [11,None],visible = False),
                              Widget(position = (0.8340,0.3502),z = 101,parent = self,scale = 0.445,anchor = "center",tags = [12,None],visible = False),
                              Widget(position = (0.8780,0.3502),z = 101,parent = self,scale = 0.445,anchor = "center",tags = [13,None],visible = False),
                              Widget(position = (0.9230,0.3502),z = 101,parent = self,scale = 0.445,anchor = "center",tags = [14,None],visible = False),
                              Widget(position = (0.9665,0.3502),z = 101,parent = self,scale = 0.445,anchor = "center",tags = [15,None],visible = False),
                              Widget(position = (0.8340,0.4234),z = 101,parent = self,scale = 0.445,anchor = "center",tags = [16,None],visible = False),
                              Widget(position = (0.8780,0.4234),z = 101,parent = self,scale = 0.445,anchor = "center",tags = [17,None],visible = False),
                              Widget(position = (0.9230,0.4234),z = 101,parent = self,scale = 0.445,anchor = "center",tags = [18,None],visible = False),
                              Widget(position = (0.9665,0.4234),z = 101,parent = self,scale = 0.445,anchor = "center",tags = [19,None],visible = False),
                              Widget(position = (0.8340,0.4996),z = 101,parent = self,scale = 0.445,anchor = "center",tags = [20,None],visible = False),
                              Widget(position = (0.8780,0.4996),z = 101,parent = self,scale = 0.445,anchor = "center",tags = [21,None],visible = False),
                              Widget(position = (0.9230,0.4996),z = 101,parent = self,scale = 0.445,anchor = "center",tags = [22,None],visible = False),
                              Widget(position = (0.9665,0.4996),z = 101,parent = self,scale = 0.445,anchor = "center",tags = [23,None],visible = False),
                              Widget(position = (0.8340,0.5698),z = 101,parent = self,scale = 0.445,anchor = "center",tags = [24,None],visible = False),
                              Widget(position = (0.8780,0.5698),z = 101,parent = self,scale = 0.445,anchor = "center",tags = [25,None],visible = False),
                              Widget(position = (0.9230,0.5698),z = 101,parent = self,scale = 0.445,anchor = "center",tags = [26,None],visible = False),
                              Widget(position = (0.9665,0.5698),z = 101,parent = self,scale = 0.445,anchor = "center",tags = [27,None],visible = False)]

    def input(self,key):
        if not self.delete_panel.hovered and self.delete_panel.visible:
            self.delete_panel.visible = False

        if key == "f5":
            if self.index != None:
                self.delete_panel_button = self.image_buttons[self.index]
                self.delete_panel_button.visible = False
                self.delete_panel_button.scale = 0.445
                self.delete_panel_button.tags[1] = None
                self.delete_panel.visible = False
                self.image_files[self.image_buttons.index(self.delete_panel_button)] = None
                self.index = None
                self.console.level.remove_entities(self.image_buttons.index(self.delete_panel_button))

        if key == "f7":
            if self.index != None:
                if self.console.level.last_entity:
                    current_default = [self.console.level.last_entity.scale,self.console.level.last_entity.actual_visible,self.console.level.last_entity.actual_collidable,self.console.level.last_entity.actual_class,self.console.level.last_entity.z,self.console.level.last_entity.anchor]
                    self.defaults[self.index] = current_default
                    self.delete_panel.visible = False

        if key == "left mouse" and self.parent.hovered and not self.delete_panel.visible: 
            for button in self.buttons:
                if button.hovered:
                    self.image = self.images[button.tags[0] + 1]
                    self.index = button.tags[0]
                    break

        elif key == "left mouse" and self.parent.hovered and self.delete_panel.visible:
            if self.delete_panel.state[0]:
                self.delete_panel_button.visible = False
                self.delete_panel_button.scale = 0.445
                self.delete_panel_button.tags[1] = None
                self.delete_panel.visible = False
                self.image_files[self.image_buttons.index(self.delete_panel_button)] = None
                self.index = None
                self.console.level.remove_entities(self.image_buttons.index(self.delete_panel_button))
            elif self.delete_panel.state[1]:
                if self.index != None:
                    if self.console.level.last_entity:
                        current_default = [self.console.level.last_entity.scale,self.console.level.last_entity.actual_visible,self.console.level.last_entity.actual_collidable,self.console.level.last_entity.actual_class,self.console.level.last_entity.z,self.console.level.last_entity.anchor]
                        self.defaults[self.index] = current_default
                        print(self.defaults,current_default)
                self.delete_panel.visible = False

        if key == "right mouse" and self.hovered:
            self.delete_panel_button = None
            for button in self.buttons:
                if button.hovered:
                    self.delete_panel_button = self.image_buttons[self.buttons.index(button)]
                    break
            
            if not self.delete_panel_button == None:
                self.delete_panel.position = get_main_class().mouse.position
                self.delete_panel.visible = True
    
    def add_image(self,image_path):
        if not image_path in self.image_files:
            for img in self.image_files:
                if img == None:
                    num = self.image_files.index(img)
                    self.image_files[self.image_files.index(img)] = image_path
                    break
            image = load_image(image_path)
            button = self.image_buttons[num]
            button.image = image
            button.tags[1] = image_path
            button.visible = True
            x,y = image.get_size()
            if x > y:
                max_x = 0.445
                max_y = 0.445 / x * y
            elif y > x:
                max_y = 0.445
                max_x = 0.445 / y * x
            else:
                max_x,max_y = 0.445,0.445
            button.scale = (max_x,max_y)

class Panel(Widget):
    def __init__(self,console):
        super().__init__(position = (1,0),scale = (2,6),anchor = "topright",color = (50,50,50),z = 100)
        self.open = True
        self.console = console
        self.speed = 10

        self.pos = [1,1.2]

        self.tags.append("dt")

    def input(self,key):
        if key == "b":
            if not self.console.texts.clas.mode and not self.console.texts.posx.mode and not self.console.texts.posz.mode and not self.console.texts.posy.mode and not self.console.texts.sclx.mode and not self.console.texts.scly.mode:
                self.open = not self.open

    def move(self):
        if not self.open:
            self.position.x = self.position.x + (self.pos[1] - self.position.x) * self.speed * self.dt
        else:
            self.position.x = self.position.x + (self.pos[0] - self.position.x) * self.speed * self.dt

    def update(self):
        super().update()
        self.move()

class Level:
    def __init__(self,console):
        self.game = get_main_class()

        self.entities = []

        self.last_mouse_pos = (0,0)
        self.latch = False
        self.console = console 
        self.colliding = False

        self.anchor = PlayerController2D(scale = 0,visible = False,can_collide = False,speed = 300)
        self.game.camera.parent = self.anchor
        self.game.camera.speed = 10
        
        self.last_entity = None

        self.last_entity_last_pos = (0,0)

        self.panel = console.panel

        self.board = console.board

        self.caps_lock = pygame.key.get_mods() == pygame.KMOD_CAPS

    def remove_entities(self,index):
        remove = []
        for ent in self.entities:
            if ent.image_index == index:
                if self.last_entity is ent:
                    self.last_entity = None
                destroy(ent)
                remove.append(ent)
        for ent in remove:
            self.entities.pop(self.entities.index(ent))
            destroy(ent.ghost)

    def export(self,file_path):
        self.all_data = []
        self.data = []
        self.defaults = self.console.board.defaults
        defaults = []
        for default in self.defaults:
            default = [default,get_relative_path(self.console.folder_button.folder_path,self.console.board.image_files[self.defaults.index(default)])]
            defaults.append(default)
        for entity in self.entities:
            data = f"['{entity.actual_class}',{entity.image_index},{entity.position},{entity.scale},{entity.actual_visible},{entity.actual_collidable},{entity.z},'{entity.anchor}']"
            self.data.append(data)
        self.all_data.append(self.data)
        board_images = []
        for path in self.board.image_files:
            board_images.append(get_relative_path(self.console.folder_button.folder_path,path))
        self.all_data.append(board_images)
        self.all_data.append(defaults)

        try:
            with open(file_path, 'w') as file:
                file.write(f"{self.all_data}")
        except:
            pass

    def add_level(self,path):
        contents = 0
        path = path.replace("\\", "/")
        if not os.path.isabs(path):
            file_path = os.path.abspath(__file__)
            file_path = file_path.replace("\\", "/")
            base_path = os.path.dirname(os.path.dirname(file_path))
            path = os.path.join(base_path, path)
        with open(path,"r") as file:
            contents = literal_eval(file.read())
        entities = contents[0]
        images = contents[1]
        defaults = contents[2]

        for img in images:
            if not img == None:
                self.console.board.add_image(img)
        for default in defaults:
            self.console.board.defaults[self.console.board.image_files.index(default[1])] = default[0]
        
        for ent in entities:
            ent = literal_eval(ent)
            entity = REntity(image = load_image(images[ent[1]]),position = ent[2],scale = ent[3],z = ent[6],anchor = ent[7])
            entity.actual_visible = ent[4]
            entity.actual_collidable = ent[5]
            entity.image_index = ent[1]
            entity.actual_class = ent[0]
            self.entities.append(entity)
    
    def input(self,key):
        if key == "left mouse" and not self.panel.hovered and not self.console.smp.hovered and not self.console.stg.hovered and self.console.smp.mode == 2:
            if not self.board.index == None and self.board.image_files[self.board.index]:
                ent = REntity(position = (mouse.world_position),image = load_image(self.board.image_files[self.board.index]))
                ent.actual_class = self.console.board.defaults[self.console.board.index][3]
                ent.actual_collidable = self.console.board.defaults[self.console.board.index][2]
                ent.actual_visible = self.console.board.defaults[self.console.board.index][1]
                ent.scale = self.console.board.defaults[self.console.board.index][0]
                ent.z = self.console.board.defaults[self.console.board.index][4]
                ent.anchor = self.console.board.defaults[self.console.board.index][5]
                ent.image_index = self.board.index
                self.entities.append(ent)
                self.last_entity = ent

                if self.console.stg.on:
                    self.last_entity.position.x = round(self.last_entity.position.x / (self.last_entity.scale.x * 100)) * (self.last_entity.scale.x * 100)
                    self.last_entity.position.y = round(self.last_entity.position.y / (self.last_entity.scale.y * 100)) * (self.last_entity.scale.y * 100)
        
        if (key == "right mouse" or (key == "left mouse" and self.console.smp.mode == 0)) and not self.panel.hovered and not self.console.smp.hovered and not self.console.stg.hovered:
            self.last_entity = None
            for ent in sorted(self.entities,key = lambda sprite: (sprite.z,sprite.rect.bottom)):
                if ent.collider.hovered:
                    self.last_entity = ent

        if key == "delete":
            if not self.last_entity == None:
                destroy(self.last_entity)
                destroy(self.last_entity.ghost)
                self.entities.pop(self.entities.index(self.last_entity))
                self.last_entity = None

    def update(self):
        if self.last_entity and self.console.smp.mode == 1 and (self.last_entity.collider.hovered or self.colliding):
            if key_pressed("left mouse"):
                if not self.latch:
                    self.latch = True
                    self.colliding = True
                    self.last_mouse_pos = (mouse.world_position.x,mouse.world_position.y)
                    self.last_entity_last_pos = (self.last_entity.position.x,self.last_entity.position.y)
                self.last_entity.position.x = self.last_entity_last_pos[0] + mouse.world_position.x - self.last_mouse_pos[0]
                self.last_entity.position.y = self.last_entity_last_pos[1] + mouse.world_position.y - self.last_mouse_pos[1]
            else:
                self.latch = False
                self.colliding = False
            
        if self.console.stg.on and self.last_entity and not self.latch:
            self.last_entity.position.x = round(self.last_entity.position.x / (self.last_entity.scale.x * 100)) * (self.last_entity.scale.x * 100)
            self.last_entity.position.y = round(self.last_entity.position.y / (self.last_entity.scale.y * 100)) * (self.last_entity.scale.y * 100)
        if not self.last_entity == None:
            pygame.draw.rect(self.game.window.display,(255,255,255),pygame.Rect(self.last_entity.collider.x - camera.position.x * 2 + 500 * scale_def(),self.last_entity.collider.y - camera.position.y * 2 + 600 * scale_def(),self.last_entity.collider.width,self.last_entity.collider.height),2,2)
        self.caps_lock = pygame.key.get_mods() == pygame.KMOD_CAPS
        self.anchor.speed = 300
        if self.caps_lock:
            self.anchor.speed = 1200

class Console:
    def __init__(self):
        self.panel = Panel(self)
        self.board = Board(self)
        self.level = Level(self)
        self.import_button = ImportButton(self)
        self.export_button = ExportButton(self)
        self.folder_button = FolderButton(self)
        self.texts = Texts(self)
        self.visible_setter = VisibleSetter(self)
        self.collidable_setter = CollidableSetter(self)
        self.anchor_setter = AnchorSetter(self)
        self.stg = SnapToGrid(self)
        self.smp = SMP(self)

game = Teon(fullscreen = True,entity_counter = False,aspect_borders = True,background_color = (15,15,15),fps = 60)
console = Console()
def update():
    console.level.update()
def input(key):
    console.level.input(key)
    if key == "escape":
        game.quit()
        
game.run(update,input)