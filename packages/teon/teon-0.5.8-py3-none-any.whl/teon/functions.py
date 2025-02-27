import pygame,math,os,cv2,sys
from PIL import Image

from teon.other import _key_map,_yek_map,Vec2,_color_dict,ColorError,Timer
from teon.font import Font
from teon.animation import Animation

class TeonFunction:
    def __init__(self,func,tps,running = True):
        self._tps = tps
        self._func = func
        self.tps_timer = Timer(1000/self._tps,True,func = func,autostart = running)
        self.running = running

    @property
    def func(self):
        return self._func
    
    @func.setter
    def func(self,func):
        self._func = func
        self.tps_timer.func = self._func

    @property
    def tps(self):
        return self._tps

    @tps.setter
    def tps(self,tps):
        self._tps = tps
        self.tps_timer = Timer(1/self._tps)

    def _run(self):
        if self.running and not self.tps_timer.active:
            self.tps_timer.activate()
        elif not self.running and self.tps_timer.active:
            self.tps_timer.deactivate()

        self.tps_timer.update()

def _mp4_to_png(video_path,alpha):
    video = cv2.VideoCapture(video_path)
    frames = []
    
    while True:
        ret, frame = video.read()
        if not ret:
            break
        
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        if alpha:
            frame_surface = pygame.image.frombuffer(frame.tobytes(), frame.shape[1::-1], "RGB").convert_alpha()
        else:
            frame_surface = pygame.image.frombuffer(frame.tobytes(), frame.shape[1::-1], "RGB").convert()

        frames.append(frame_surface)
    
    video.release()
    return Animation(frames)

def _list_to_png(path,name,int_range,alpha = True):
    x,y = int_range
    prefix = name.split(".")[0]
    sufix = name.split(".")[1]
    list = []
    for i in range(x,y + 1):
        list.append(load_image(f"{path}/{prefix}{i}.{sufix}",alpha))

    return Animation(list)

def load_animation(path,name = None,int_range = None,alpha = True):

    path = path.replace("\\", "/")
    if not os.path.isabs(path):
        file_path = os.path.abspath(sys.argv[0])
        file_path = file_path.replace("\\", "/")
        strs = file_path.split("/")
        base_path = ""
        for i in range(len(strs) - 1):
            base_path += strs[i] + "/"
        path = os.path.join(base_path, path)

    if f"{path[-4]}{path[-3]}{path[-2]}{path[-1]}" == ".gif":
        animation = _gif_to_png(path,alpha)
    elif name != None:
        animation = _list_to_png(path,name,int_range,alpha)
    else:
        animation = _mp4_to_png(path,alpha)

    return animation

def _gif_to_png(gif_path,alpha = True):
    gif = Image.open(gif_path)
    frames = []
    try:
        while True:
            frame = gif.convert("RGBA")
            mode = gif.mode
            size = gif.size
            data = gif.tobytes()

            if alpha:
                pygame_image = pygame.image.fromstring(data, size, mode).convert_alpha()
            else:
                pygame_image = pygame.image.fromstring(data, size, mode).convert()

            frames.append(pygame_image)
                
            gif.seek(gif.tell() + 1)

    except EOFError:
        pass

    frames.pop(0)
    
    return Animation(frames)

class _CollidingType:
    def __init__(self,bool,entity,entities = []):
        self.colliding = bool
        self.entity = entity
        self.entities = entities

    def __bool__(self):
        return self.colliding
    
    def __repr__(self):
        return f"{self.colliding}"

def load_font(path):
    '''
    Give the font path, and it returns the loaded Font object.
    Ensures proper path handling for relative paths.
    '''
    # Normalize path separators
    path = path.replace("\\", "/")
    if not os.path.isabs(path):
        file_path = os.path.abspath(sys.argv[0])
        file_path = file_path.replace("\\", "/")
        strs = file_path.split("/")
        base_path = ""
        for i in range(len(strs) - 1):
            base_path += strs[i] + "/"
        path = os.path.join(base_path, path)
    
    return Font(path)

def _get_color(color):
    if not isinstance(color,tuple):
        try:
            return _color_dict[color]
        except:
            raise ColorError("The color provided isn't recognized, for more info check the Teon Docs")
    else:
        return color

def colliding(entity1,entity2,specific_collider : tuple = (False,False)):
        from teon.entity import Entity
        collider1 = entity1.hitbox

        circle1,circle2 = False,False

        

        if specific_collider[0] != False:
            collider1 = entity1.colliders[specific_collider[0]]
            if collider1.shape == "circle":
                circle1 = True
        
        if isinstance(entity2,Entity):
            collider2 = entity2.hitbox
                
            if specific_collider[1] != False:
                collider2 = entity2.colliders[specific_collider[1]]
                if collider2.shape == "circle":
                    circle2 = True

            if not circle1 and not circle2:
                return _CollidingType(collider1.colliderect(collider2),entity2)
                        
            elif circle1 and not circle2:
                # Find the closest point on the square to the circle's center
                closest_x = max(collider2.x, min(collider1.centerx, collider2.x + collider2.width))
                closest_y = max(collider2.y, min(collider1.centery, collider2.y + collider2.height))

                # Compute squared distance from closest point to circle center
                dx = closest_x - collider1.centerx
                dy = closest_y - collider1.centery
                distance_squared = dx**2 + dy**2

                return distance_squared <= (collider1._radius)**2


                    
            elif not circle1 and circle2:
                closest_x = max(collider1.x, min(collider2.centerx, collider1.x + collider1.width))
                closest_y = max(collider1.y, min(collider2.centery, collider1.y + collider1.height))

                # Compute squared distance from closest point to circle center
                dx = closest_x - collider2.centerx
                dy = closest_y - collider2.centery
                distance_squared = dx**2 + dy**2

                return distance_squared <= (collider2._radius)**2
                    
            else:
                dx = collider2.centerx - collider1.centerx
                dy = collider2.centery - collider1.centery
                distance_squared = dx**2 + dy**2

                # Compute squared sum of radii (scaled)
                combined_radius = (collider1._radius + collider2._radius)
                return distance_squared <= combined_radius**2
        
        elif isinstance(entity2,list):
            collidings = []
            first_ent = None
            for entity in entity2:
                circle2 = False
                collider = entity.collider
                if specific_collider[1] != False:
                    collider = entity.colliders[specific_collider[1]]
                    if collider.shape == "circle":
                        circle2 = True

                if not circle1 and not circle2:
                    if collider1.colliderect(collider):
                        if not first_ent:
                            first_ent = entity
                        collidings.append(entity)
                    
                elif circle1 and not circle2:
                    closest_x = max(collider.centerx, min(collider1.centerx, collider.centerx + collider.width))
                    closest_y = max(collider.centery, min(collider1.centery, collider.centery + collider.height))

                    distance = math.sqrt((closest_x - collider1.centerx) ** 2 + (closest_y - collider1.centery) ** 2)

                    return distance < collider1.radius
                
                elif not circle1 and circle2:
                    closest_x = max(collider1.centerx, min(collider.centerx, collider1.centerx + collider1.width))
                    closest_y = max(collider1.centery, min(collider.centery, collider1.centery + collider1.height))

                    distance = math.sqrt((closest_x - collider.centerx) ** 2 + (closest_y - collider.centery) ** 2)

                    return distance < collider.radius
                
                else:
                    distance = math.sqrt((collider.centerx - collider1.centerx) ** 2 + (collider.centery - collider1.centery) ** 2)
                    
                    return distance < (collider1.radius + collider.radius)
            return _CollidingType(True,first_ent,collidings)

        return _CollidingType(False,None)

def _repair_vec2(vec2):
    if isinstance(vec2,tuple):
        return Vec2(vec2[0],vec2[1])
    return vec2

def destroy(*entities):
    for entity in entities:
        if isinstance(entity,list) or isinstance(entity,tuple):
            for ent in entity:
                ent.kill()
        else:
            entity.kill()

def _get_color_value(value):
    if isinstance(value,str):
        if not "#" in value:
            return _get_color(value)
        else:
            value = value.lstrip('#')
            
            rgb = tuple(int(value[i:i+2], 16) for i in (0, 2, 4))
            
            return rgb
    elif isinstance(value,tuple):
        return value
    else:
        raise ColorError(f"The color {value} isn't recognized, the system supports only rgb anf hex color values")

def mouse_position():
    return _repair_vec2(pygame.mouse.get_pos())

def window_size():
    return _repair_vec2(pygame.display.get_window_size())

def screen_size():
    return _repair_vec2(pygame.display.get_desktop_sizes()[0])

def key_pressed(key):
    '''
    Returns true if the given key is pressed down
    '''
    if key == "left mouse":
        return mouse_pressed()[0]
    elif key == "middle mouse":
        return mouse_pressed()[1]
    elif key == "right mouse":
        return mouse_pressed()[2]
    return pygame.key.get_pressed()[tr_key(key)]

def load_image(path,alpha = True,antialias = None):
    '''
    Give the image path, and it returns the loaded image \n
    Set alpha to False for faster a game, but loose transparency
    '''
    path = path.replace("\\", "/")
    if not os.path.isabs(path):
        file_path = os.path.abspath(sys.argv[0])
        file_path = file_path.replace("\\", "/")
        strs = file_path.split("/")
        base_path = ""
        for i in range(len(strs) - 1):
            base_path += strs[i] + "/"
        path = os.path.join(base_path, path)
    from teon.other import antialiasing
    if antialias == None:
        anti = antialiasing
    else:
        anti = antialias
    if alpha:
        img = pygame.image.load(path).convert_alpha()
    else:
        img = pygame.image.load(path).convert()
    if anti:
        return pygame.transform.smoothscale(img,img.get_size()).convert_alpha()
    return img

def tr_key(key):
    '''
    Don't use this
    '''
    return _key_map[key]

def rt_key(key):
    '''
    Don't use this
    '''
    try:
        return _yek_map[key]
    except:
        return None

def mouse_pressed():
    '''
    Returns tuple(bool,bool,bool) 0 is the left mouse button, 1 is the scroll wheel, 2 is the right mouse button. \n
    Returns the current state of the mouse button, True if held down
    '''
    return pygame.mouse.get_pressed()

ASPECT_SIZE = (1000,600)
ZOOM = 1
def scale_def():
    aspect_ratio = ASPECT_SIZE[0] / ASPECT_SIZE[1]
    window_width, window_height = pygame.display.get_window_size()

    normalized_width = aspect_ratio
    normalized_height = 1

    dx = window_width / normalized_width
    dy = window_height / normalized_height

    scale_factor = min(dx, dy)
    return scale_factor * ZOOM / 600