import time
from pygame.locals import *
import pygame

# Constants bàsiques del joc
AMPLADA = 800
ALTURA = 600
BACKGROUND_IMAGE = 'assets/fons.png'
MUSICA_FONS = 'assets/music.mp3'
WHITE = (255, 255, 255)
MAGENTA = (255, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
guanyador = 0

# Variables de control del joc
pantalla_actual = 1  # Controla quina pantalla es mostra (menú, crèdits, joc, victòria)
game_win_sound_played = False  # Evita que el so de victòria es repeteixi
pos_y_fons = 0  # Posició del fons per a l'animació
temps_inici = 0  # Temps inicial per a l'augment de velocitat

# Jugador 1: configuració inicial
player_image = pygame.image.load('assets/nau.png')
player_rect = player_image.get_rect(midbottom=(AMPLADA // 2, ALTURA - 10))
velocitat_nau = 5
vides_jugador1 = 3
puntuacio_jugador1 = 0  # Puntuació del jugador 1

# Jugador 2: configuració inicial
player_image2 = pygame.image.load('assets/nau2.png')
player_rect2 = player_image2.get_rect(midbottom=(AMPLADA // 2, ALTURA - 500))
velocitat_nau2 = 5
vides_jugador2 = 3
puntuacio_jugador2 = 0  # Puntuació del jugador 2

# Vides: imatges dels cors
vides_jugador1_image = pygame.image.load('assets/cor.png')
vides_jugador2_image = pygame.image.load('assets/cor2.png')

# Bales: diferents colors per a cada jugador
bala_imatge_j1 = pygame.Surface((4, 10))  # Bala del jugador 1 (verda)
bala_imatge_j1.fill(GREEN)
bala_imatge_j2 = pygame.Surface((4, 10))  # Bala del jugador 2 (vermella)
bala_imatge_j2.fill(RED)
bales_jugador1 = []
bales_jugador2 = []
velocitat_bales = 15
temps_entre_bales = 500
temps_ultima_bala_jugador1 = 0
temps_ultima_bala_jugador2 = 0

# Inicialització de Pygame
pygame.init()
pantalla = pygame.display.set_mode((AMPLADA, ALTURA))
pygame.display.set_caption("SpaceInvaders")

# Càrrega de sons
pygame.mixer.music.load(MUSICA_FONS)
pygame.mixer.music.set_volume(0.06)
pygame.mixer.music.play(-1)
LASER_SHOOT_SOUND = pygame.mixer.Sound('assets/lasersound.mp3')
GAME_WIN_SOUND = pygame.mixer.Sound('assets/winsound.wav')
HIT_SOUND = pygame.mixer.Sound('assets/hitsound.wav')  # So quan un jugador rep dany

# Control de FPS
clock = pygame.time.Clock()
fps = 60

# Funció per dibuixar el fons amb animació
def imprimir_pantalla_fons(image):
    global pos_y_fons
    background = pygame.image.load(image).convert()
    pantalla.blit(background, (0, pos_y_fons))  # Dibuixa el fons en la posició actual
    pantalla.blit(background, (0, pos_y_fons - ALTURA))  # Dibuixa una còpia per sobre per fer l'efecte continu
    pos_y_fons += 1  # Mou el fons cap avall
    if pos_y_fons >= ALTURA:  # Si arriba al final, reinicia la posició
        pos_y_fons = 0

# Funció per mostrar el menú principal
def show_menu():
    imprimir_pantalla_fons(BACKGROUND_IMAGE)
    text0 = "SPACE INVADERS!"
    text1 = "1. Començar partida"
    text2 = "2. Veure crèdits"
    text3 = "3. Sortir"
    font0 = pygame.font.SysFont(None, 85)
    font1 = pygame.font.SysFont(None, 55)
    img0 = font0.render(text0, True, GREEN)
    img1 = font1.render(text1, True, MAGENTA)
    img2 = font1.render(text2, True, MAGENTA)
    img3 = font1.render(text3, True, RED)
    pantalla.blit(img0, (120, 30))
    pantalla.blit(img1, (180, 200))
    pantalla.blit(img2, (180, 300))
    pantalla.blit(img3, (180, 400))

# Funció per mostrar els crèdits
def show_credits():
    imprimir_pantalla_fons(BACKGROUND_IMAGE)
    text0 = "SPACE INVADERS"
    text1 = "Programació:"
    text2 = "Gràfics:"
    text3 = "Música:"
    text4 = "Sons:"
    text5 = "Abel Bernal"
    text6 = "Música sense copyright"
    text7 = "Mixkit i Tunetank"
    text11 = "Xavi Sancho i Abel Bernal"
    font0 = pygame.font.SysFont(None, 85)
    font1 = pygame.font.SysFont(None, 60)
    font2 = pygame.font.SysFont(None, 50)
    img0 = font0.render(text0, True, GREEN)
    img1 = font1.render(text1, True, MAGENTA)
    img2 = font1.render(text2, True, MAGENTA)
    img3 = font1.render(text3, True, MAGENTA)
    img4 = font1.render(text4, True, MAGENTA)
    img5 = font2.render(text5, True, GREEN)
    img6 = font2.render(text6, True, GREEN)
    img7 = font2.render(text7, True, GREEN)
    img8 = font2.render(text11, True, GREEN)
    pantalla.blit(img0, (120, 30))
    pantalla.blit(img1, (180, 200))
    pantalla.blit(img2, (180, 300))
    pantalla.blit(img5, (300, 350))
    pantalla.blit(img3, (180, 400))
    pantalla.blit(img6, (300, 450))
    pantalla.blit(img4, (180, 500))
    pantalla.blit(img7, (300, 550))
    pantalla.blit(img8, (300, 250))

# Bucle principal del joc
while True:
    current_time = pygame.time.get_ticks()

    # Gestió d'esdeveniments
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

        if pantalla_actual == 1:  # Menú principal
            if event.type == KEYDOWN:
                if event.key == K_3:
                    pygame.quit()
                if event.key == K_1:
                    pantalla_actual = 3
                    game_win_sound_played = False
                    temps_inici = pygame.time.get_ticks()  # Reinicia el temporitzador
                if event.key == K_2:
                    pantalla_actual = 2

        if pantalla_actual == 2:  # Crèdits
            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    pantalla_actual = 1

        if pantalla_actual == 3:  # Joc
            if event.type == KEYDOWN:
                if event.key == K_w and current_time - temps_ultima_bala_jugador1 >= temps_entre_bales:
                    bales_jugador1.append(pygame.Rect(player_rect.centerx - 2, player_rect.top, 4, 10))
                    temps_ultima_bala_jugador1 = current_time
                    LASER_SHOOT_SOUND.play()
                if event.key == K_UP and current_time - temps_ultima_bala_jugador2 >= temps_entre_bales:
                    bales_jugador2.append(pygame.Rect(player_rect2.centerx - 2, player_rect2.bottom - 10, 4, 10))
                    temps_ultima_bala_jugador2 = current_time
                    LASER_SHOOT_SOUND.play()

        if pantalla_actual == 4:  # Pantalla de victòria
            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    vides_jugador1 = 3
                    vides_jugador2 = 3
                    puntuacio_jugador1 = 0  # Reinicia puntuacions
                    puntuacio_jugador2 = 0
                    pantalla_actual = 1
                    game_win_sound_played = False
                    bales_jugador1.clear()
                    bales_jugador2.clear()

    # Actualització de les pantalles
    if pantalla_actual == 1:  # Mostra el menú
        show_menu()

    if pantalla_actual == 2:  # Mostra els crèdits
        show_credits()

    if pantalla_actual == 3:  # Lògica del joc
        # Ajusta la velocitat segons el temps transcorregut
        temps_transcorregut = (pygame.time.get_ticks() - temps_inici) // 1000
        velocitat_nau = 5 + (temps_transcorregut // 10)  # Augmenta cada 10 segons
        velocitat_nau2 = 5 + (temps_transcorregut // 10)

        # Moviment de les naus
        keys = pygame.key.get_pressed()
        if keys[K_a]:
            player_rect.x -= velocitat_nau
        if keys[K_d]:
            player_rect.x += velocitat_nau
        if keys[K_LEFT]:
            player_rect2.x -= velocitat_nau2
        if keys[K_RIGHT]:
            player_rect2.x += velocitat_nau2

        player_rect.clamp_ip(pantalla.get_rect())
        player_rect2.clamp_ip(pantalla.get_rect())

        # Dibuixa el fons animat
        imprimir_pantalla_fons(BACKGROUND_IMAGE)

        # Gestió de bales del jugador 1
        for bala in bales_jugador1[:]:
            bala.y -= velocitat_bales
            if bala.bottom < 0 or bala.top > ALTURA:
                bales_jugador1.remove(bala)
            else:
                pantalla.blit(bala_imatge_j1, bala)
            if player_rect2.colliderect(bala):
                bales_jugador1.remove(bala)
                vides_jugador2 -= 1
                puntuacio_jugador1 += 10  # Suma punts
                HIT_SOUND.play()  # So de dany
                print("vides jugador 2:", vides_jugador2)

        # Gestió de bales del jugador 2
        for bala in bales_jugador2[:]:
            bala.y += velocitat_bales
            if bala.bottom < 0 or bala.top > ALTURA:
                bales_jugador2.remove(bala)
            else:
                pantalla.blit(bala_imatge_j2, bala)
            if player_rect.colliderect(bala):
                bales_jugador2.remove(bala)
                vides_jugador1 -= 1
                puntuacio_jugador2 += 10  # Suma punts
                HIT_SOUND.play()  # So de dany
                print("vides jugador 1:", vides_jugador1)

        # Dibuixa les naus
        pantalla.blit(player_image, player_rect)
        pantalla.blit(player_image2, player_rect2)

        # Dibuixa les vides
        if vides_jugador1 >= 3:
            pantalla.blit(vides_jugador1_image, (700, 550))
        if vides_jugador1 >= 2:
            pantalla.blit(vides_jugador1_image, (720, 550))
        if vides_jugador1 >= 1:
            pantalla.blit(vides_jugador1_image, (740, 550))

        if vides_jugador2 >= 1:
            pantalla.blit(vides_jugador2_image, (20, 10))
        if vides_jugador2 >= 2:
            pantalla.blit(vides_jugador2_image, (40, 10))
        if vides_jugador2 >= 3:
            pantalla.blit(vides_jugador2_image, (60, 10))

        # Dibuixa la puntuació
        font = pygame.font.SysFont(None, 40)
        puntuacio1 = font.render(f"P1: {puntuacio_jugador1}", True, WHITE)
        puntuacio2 = font.render(f"P2: {puntuacio_jugador2}", True, WHITE)
        pantalla.blit(puntuacio1, (700, 520))  # Puntuació jugador 1 a sobre dels cors
        pantalla.blit(puntuacio2, (10, 50))   # Puntuació jugador 2

        # Comprova si algun jugador ha perdut
        if vides_jugador1 <= 0 or vides_jugador2 <= 0:
            guanyador = 1 if vides_jugador2 > 0 else 2
            pantalla_actual = 4
            if not game_win_sound_played:
                GAME_WIN_SOUND.play()
                game_win_sound_played = True

    if pantalla_actual == 4:  # Pantalla de victòria
        imprimir_pantalla_fons('assets/gameover.png')
        text = "Jugador " + str(guanyador) + " Wins!"
        text2 = "Prem SPACE per tornar al menú"
        font = pygame.font.SysFont(None, 50)
        font2 = pygame.font.SysFont(None, 40)
        img = font.render(text, True, MAGENTA)
        img2 = font2.render(text2, True, WHITE)
        pantalla.blit(img, (250, 280))
        pantalla.blit(img2, (200, 350))  # Missatge per tornar al menú

    # Actualitza la pantalla i controla els FPS
    pygame.display.update()
    clock.tick(fps)
