from teon.other import Timer

class Animation:
    def __init__(self,animation,speed = 12):
        self.images = animation
        self._speed = speed
        self._timer = Timer(1000/self._speed)

    @property
    def speed(self):
        return self._speed

    @speed.setter
    def speed(self,speed):
        self._speed = speed
        self._timer = Timer(1000/self._speed)