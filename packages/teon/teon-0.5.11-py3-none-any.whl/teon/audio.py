import pygame

pygame.mixer.init()

class Song:
    def __init__(self, path):
        self.song = pygame.mixer.Sound(path)
        self.channel = None

    def play(self, loops=0):
        self.channel = self.song.play(loops=loops)

    def stop(self):
        if self.channel:
            self.channel.stop()

    def pause(self):
        if self.channel and self.channel.get_busy():
            self.channel.pause()

    def unpause(self):
        if self.channel:
            self.channel.unpause()

    def set_volume(self, volume):
        self.song.set_volume(volume)

class Sound:
    def __init__(self, path):
        self.effect = pygame.mixer.Sound(path)

    def play(self):
        self.effect.play()

    def set_volume(self,volume):
        self.effect.set_volume(volume)

def load_sound(path):
    return Sound(path)

def load_song(path):
    return Song(path)