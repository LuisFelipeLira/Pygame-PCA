import pygame
import shelve

from catador import Carro
from player import Player
from lixos import LixoL
from lixos import LixoR
from lixos import tiro
from time import sleep


import math
import time
from random import randint
import os


os.environ['SDL_VIDEO_CENTERED'] = '1'

WIDTH = 980
HEIGHT = 720



pygame.init()
save = shelve.open('save')
pygame.display.set_caption("Trash Cleaner")
screen = pygame.display.set_mode((WIDTH, HEIGHT))
#Lançar_group = pygame.sprite.Group()


# Iniciando imagens, sons e fontes e arquivos

titulo = pygame.image.load('imagens/menu/titulo.png')
fundo = pygame.image.load('imagens/menu/fundo.png')

jogar = pygame.image.load('imagens/menu/jogar.png')
jogaralt = pygame.image.load('imagens/menu/jogaralt.png')

sair = pygame.image.load('imagens/menu/sair.png')
sairalt = pygame.image.load('imagens/menu/sairalt.png')

config = pygame.image.load('imagens/menu/config.png')
configalt = pygame.image.load('imagens/menu/configalt.png')


#music = pygame.mixer.Sound('Sons/music.wav')
#passos = pygame.mixer.Sound('Sons/passos.wav')

# Menu
def menu():
    # Coloca as imagens
    screen.blit(fundo, (0, 0))
    screen.blit(titulo, (WIDTH / 4.5, 0))
    screen.blit(jogar, (WIDTH / 3.1, 300))
    # screen.blit(jogaralt, (WIDTH / 4,0))
    screen.blit(sair, (WIDTH / 3, 460))
    # screen.blit(sairalt, (WIDTH / 4,0))
    screen.blit(config, (900, 0))
    # screen.blit(configalt, (800,0))
    pygame.display.flip()

    # Eventos clicáveis do Menu

    while pygame.event.wait() or pygame.event.get():

        # Pega a posição do mouse e
        # (Posição hitbox direita) > Posição X do mouse > (Posição hitbox esquerda) and (Posição hitbox baixo)
        # > Posição Y do mouse > (Posição hitbox cima) então:

        mouse = pygame.mouse.get_pos()

        if WIDTH / 3.1 + 359 > mouse[0] > WIDTH / 3.1 and 300 + 142 > mouse[1] > 300:
            screen.blit(jogaralt, (WIDTH / 3.3, 288))
            if pygame.mouse.get_pressed()[0]:
                jogo()

        else:
            screen.blit(jogar, (WIDTH / 3.1, 300))

        if WIDTH / 3 + 316 > mouse[0] > WIDTH / 3 and 460 + 115 > mouse[1] > 460:
            screen.blit(sairalt, (WIDTH / 3, 460))
            if pygame.mouse.get_pressed()[0]:
                quit()
        else:
            screen.blit(sair, (WIDTH / 3, 460))

        if 900 + 67 > mouse[0] > 900 and 0 + 67 > mouse[1] > 0:
            screen.blit(configalt, (899, -1))

        else:
            screen.blit(config, (900, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        pygame.display.flip()

font_name = pygame.font.match_font('arial')
def text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, (255,255,255,0))
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


# Game
def jogo():
    # objetos
    temporizador = 0

    pontos = 0
    pontosfeitos = 0
    timer = 0
    contagem = 0

    objectGroup = pygame.sprite.Group()

    #lixos = LixoL(objectGroup)
    #lixos.rect.center = [100, 100]
    #lixos2 = LixoL(objectGroup)
    #lixos.rect.center = [200, 200]
    #lixos3 = LixoL(objectGroup)
    #lixos.rect.center = [300, 300]


    Lixo_group = pygame.sprite.Group()
    tiro_group = pygame.sprite.Group()
    #lixoL = LixoL()
    #lixoR = LixoR()
    #Lixo_group.add(lixoL)
    #Lixo_group.add(lixoR)

    Player_group = pygame.sprite.Group()
    player = Player()
    Player_group.add(player)

    Carro_group = pygame.sprite.Group()
    carro = Carro()
    Carro_group.add(carro)

    all_group = pygame.sprite.Group()
    #all_group.add(player)
    #all_group.add(carro)
    #all_group.add(lançar)
    #all_group.add(lixoL)
    #all_group.add(lixoR)

    # Fundo
    bg = pygame.image.load('Imagens/jogo/fundosemobjetos.png').convert()
    bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))
    bg_y = 0

    # Sounds
    andar = pygame.mixer.Sound('Sons/passos.wav')

    # Música

    # pygame.mixer_music.load("Sons/music.wav")
    # pygame.mixer.music.play(-1)

    # enemies_spd = 0

    clock = pygame.time.Clock()
    while True:
        clock.tick(150)

        # Faz o Fundo continuar infinito
        bg_y1 = bg_y % bg.get_height()
        bg_y += 2
        screen.blit(bg, (0, bg_y1 - bg.get_height()))
        if bg_y1 < HEIGHT:
            screen.blit(bg, (0, bg_y1))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    menu()
                if event.key == pygame.K_SPACE:
                    atirar = tiro(objectGroup, tiro_group)
                    if pontosfeitos >= 1:
                        atirar.rect.center = player.rect.center
                        pontosfeitos -= 1


        timer += 1
        if timer == 60:
            #time.sleep(0.1)
            timer = 0
            lixol = LixoL(objectGroup, Lixo_group)
            lixor = LixoR(objectGroup, Lixo_group)



        # Update
        objectGroup.update()
        #objectGroup.draw(screen)

        #colisão
        if pygame.sprite.groupcollide(Lixo_group, Player_group, True, False):
            pontosfeitos += 1

        if pygame.sprite.groupcollide(tiro_group, Carro_group, True, False):
            pontos += 2

        #Lixo_group.update()
        #Lixo_group.draw(screen)

        objectGroup.draw(screen)

        Player_group.update()
        Player_group.draw(screen)

        Carro_group.update()
        Carro_group.draw(screen)

        all_group.update()
        all_group.draw(screen)

        text(screen, f"PONTOS: {pontos}", 30, 500, 0)
        text(screen, f"Lixos na Mochila: {pontosfeitos}", 30, 250, 0)
        text(screen, f"Faltam {contagem} segundos", 30, 750, 0)


        pygame.display.update()
        screen.fill((0, 0, 0))
menu()
pygame.quit()
