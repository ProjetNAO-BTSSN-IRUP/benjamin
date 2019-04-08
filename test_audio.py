import pygame

pygame.init()
pygame.mixer.init(44100, -16, 2, 2048)

pygame.display.set_mode((200, 100))
pygame.mixer.music.load("tomorrow.mp3")
pygame.mixer.music.play()

clock = pygame.time.Clock()
clock.tick(10)

while pygame.mixer.music.get_busy():
    pygame.event.poll()
    clock.tick(10)
