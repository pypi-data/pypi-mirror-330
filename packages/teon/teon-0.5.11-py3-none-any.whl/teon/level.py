import os,sys
from ast import literal_eval
from teon.entity import Entity
from teon.functions import load_image
from teon.custom_group import CustomGroup
from teon.extra.controller import Controller2D
class Level:
    def __init__(self,index=0):
        self.index = index
        self.entities = CustomGroup()
        self.active = False

        Entity.level_editor.add_level(self)

        self.done = False

    def add_entity(self, entity):
        self.entities.add(entity)

    def load(self,path):
        contents = 0
        path = path.replace("\\", "/")
        if not os.path.isabs(path):
            file_path = os.path.abspath(sys.argv[0])
            file_path = file_path.replace("\\", "/")
            strs = file_path.split("/")
            base_path = ""
            for i in range(len(strs) - 1):
                base_path += strs[i] + "/"
            path = os.path.join(base_path, path)
        with open(path,"r") as file:
            contents = literal_eval(file.read())
        entities = contents[0]
        images = contents[1]

        for ent in entities:
            ent = literal_eval(ent)
            if ent[0] in globals():
                globals()[ent[0]](image = load_image(images[ent[1]]),position = ent[2],scale = ent[3],visible = ent[4],collidable = ent[5],z = ent[6],anchor = ent[7])

    def remove_entity(self, entity):
        if entity in self.entities:
            self.entities.remove(entity)

    def add_player(self):
        if len(Controller2D._instances) == 1 and not self.done:
            self.done = True

    def draw(self, surface):
        self.entities.draw(surface)

    def update(self):
        for entity in self.entities:
            if entity.running and entity.updating:
                entity.update()

class LevelEditor:
    def __init__(self):
        self.levels = []
        self.active_level = None
        self.other_entities = []

    def add_level(self, level):
        self.levels.append(level)
        ents = []
        for entity in self.other_entities:
            if entity.level_index == level.index:
                self.add_entity_to_level(entity)
                ents.append(entity)
        for entity in ents:
            self.other_entities.pop(self.other_entities.index(entity))

    def lvldyt(self):
        for level in self.levels:
            level.add_player()
            level.entities.get_class()

    def add_entity_to_level(self, entity):
        level_index = entity._level_index
        for level in self.levels:
            if level.index == level_index:
                level.add_entity(entity)
                return
        self.other_entities.append(entity)

    def remove_entity_from_level(self,entity,level_index):
        self.levels[level_index].entities.remove(entity)

    def set_active_level(self, level_index):
        '''
        Give the index of the level of the level itself
        '''

        if isinstance(level_index,Level):
            level_index = level_index.index

        if 0 <= level_index < len(self.levels):
            if self.active_level is not None:
                self.active_level.active = False
            self.active_level = self.levels[level_index]
            self.active_level.active = True

    def draw(self, surface):
        if self.active_level and self.active_level.active:
            self.active_level.draw(surface)

    def update(self):
        if self.active_level and self.active_level.active:
            for entity in self.active_level.entities:
                entity._update()
            self.active_level.update()