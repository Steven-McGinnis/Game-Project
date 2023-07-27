from game_logic import GameLogic
import pygame

class Sounds:
    sounds = {}
    mixers = []

    @staticmethod
    def play_music(tag):
        if tag in GameLogic.files:
            pygame.mixer.music.load(GameLogic.files[tag])
            pygame.mixer.music.set_volume(0.25)
            pygame.mixer.music.play(-1)

    @staticmethod
    def play_sound(tag, callback=None):
        if tag not in Sounds.sounds:
            if tag in GameLogic.files:
                Sounds.sounds[tag] = pygame.mixer.Sound(GameLogic.files[tag])

        if tag not in Sounds.sounds:
            return
        
        mixer = pygame.mixer.Sound.play(Sounds.sounds[tag])

        if callback:
            Sounds.mixers.append({'mixer': mixer, 'callback': callback})



    @staticmethod
    def tick():
        to_delete = []

        for mixer in Sounds.mixers:
            if not mixer['mixer'].get_busy():
                to_delete.append(mixer)
                mixer['callback']()

        for deletion in to_delete:
            Sounds.mixers.remove(deletion)