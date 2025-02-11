import os.path
import pygame
sprites = {}
audios = {}

def load_sprites():
    path = os.path.join("assets", "sprites")
    for file in os.listdir(path):
        sprites[file.split('.')[0]] = pygame.image.load(os.path.join(path, file))

def get_sprite(name):
    return sprites[name]

def load_audios():
    path = os.path.join("assets", "audios")
    for file in os.listdir(path):
        audios[file.split('.')[0]] = pygame.mixer.Sound(os.path.join(path, file))
def play_audio(name, loops=0):
    audios[name].play(loops=loops)

def stop_audio(name):
    audios[name].stop()

def load_high_score():
    file_path = "highscore.txt"
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            try:
                return int(file.read().strip())
            except ValueError:
                return 0
    return 0

def save_high_score(high_score):
    with open("highscore.txt", "w") as file:
        file.write(str(high_score))

