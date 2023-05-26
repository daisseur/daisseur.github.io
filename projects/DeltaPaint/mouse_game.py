import pygame
from time import sleep
from random import randint as rd
import math
from PIL import Image
import numpy as np

def load_image(image_path):
    # Chargement de l'image
    image = pygame.image.load(image_path)

    # Récupération des dimensions de l'image
    largeur = image.get_width()
    hauteur = image.get_height()

    # Création de la surface de destination
    surface = pygame.Surface((largeur, hauteur))

    # Boucle pour placer chaque pixel sur la surface
    for x in range(largeur):
        for y in range(hauteur):
            couleur = image.get_at((x, y))
            surface.set_at((x, y), couleur)

    return surface


pygame.init()
screen = pygame.display.set_mode((740, 740))
img = load_image("Daytala-KA75.png")
screen.blit(img, (0, 0))
pygame.display.update()
sleep(0.5)
pygame.mouse.set_visible(False)
run = True
follow = True
color = (255, 255, 255)
size = 10
around = [{}]
forme = "circle"

def rcolor():
    global color
    color = (rd(0, 255), rd(0, 255), rd(0, 255))
    sleep(0.1)

def toggle():
    global follow
    global around
    if follow:
        follow = False
        del around[-1]
        around.append({})
    else:
        follow = True
    sleep(0.1)

def change_forme():
    global around
    around.append({})
    sleep(0.1)

while run:
    if around and len(around) > 1:
        screen.fill((0, 0, 0))
    else:
        screen.blit(img, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:
                size += 2
            if event.button == 5:
                size -= 2
        if event.type == pygame.QUIT:
            run = False
    mouse_btn = pygame.mouse.get_pressed()
    if True in mouse_btn:
        if mouse_btn[0]:
            change_forme()
        elif mouse_btn[1]:
            toggle()
        elif mouse_btn[2]:
            rcolor()
        print("clicked", follow, pygame.mouse.get_pressed())
    if follow:
        around[-1] = {}
        tmp = around[-1]
        x, y = pygame.mouse.get_pos()
        if forme == "circle":
            for p_x in range(x - size, x + size + 1):
                for p_y in range(y - size, y + size + 1):
                    distance = math.sqrt((p_x - x) ** 2 + (p_y - y) ** 2)
                    if distance <= size:
                        tmp[(p_x, p_y)] = color
        else:
            for p_x in range(x - size, x + size + 1):
                for p_y in range(y - size, y + size + 1):
                    tmp[(p_x, p_y)] = color


    for forme in around:
        for xy, rgb in forme.items():
            screen.set_at(xy, rgb)

    pygame.display.update()
    keys=pygame.key.get_pressed()
    if keys[pygame.K_s]:
        pixels = pygame.surfarray.pixels3d(screen)

        # Convert the pixels into an array using numpy
        array = np.array(pixels, dtype=np.uint8)
        array = np.rot90(array, k=1)
        array = np.rot90(array, k=1)
        # Use PIL to create an image from the new array of pixels
        image = Image.fromarray(array)
        # Inverser horizontalement l'image
        # image_inverse = image.transpose(Image.Transpose.FLIP_LEFT_RIGHT)

        # # Faire pivoter l'image de 90 degrés dans le sens des aiguilles d'une montre
        # image_rotate = image_inverse.rotate(-90)

        # Enregistrer l'image modifiée
        image.save('new.png')
        print("saved")
        sleep(0.1)
    elif keys[pygame.K_SPACE]:
        if forme == "circle":
            forme = "square"
        else:
            forme = "circle"
        sleep(0.1)
    elif keys[pygame.K_BACKSPACE]:
        around = [{}, {}]
        screen.fill((0, 0, 0))

pygame.quit()
quit()