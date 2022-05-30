import pygame
import os #importerar för att kunna navigera enklare till bilderna


WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Patiens") #Namnet på fönstret
color = (100, 0, 240)
BLACK = (0, 0, 0)
fps = 60
VEL = 2 #Velocity
BULLET_VEL = 12
MAX_BULLETS = 3
RED = (255, 0, 0)
YELLOW = (255, 255, 0)


YELLOW_HIT = pygame.USEREVENT +1
RED_HIT = pygame.USEREVENT +2

SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40
BORDER = pygame.Rect(WIDTH//2 -5, 0, 10, HEIGHT)

YELLOW_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join('Assets', 'spaceship_yellow.png'))
YELLOW_SPACESHIP = pygame.transform.rotate(
    pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)


RED_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join('Assets', 'spaceship_red.png'))
RED_SPACESHIP = pygame.transform.rotate(
    pygame.transform.scale(RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)

def draw_window(red, yellow, red_bullets, yellow_bullets):
    WIN.fill(color) #Viktigt att rita bakgrunden innan allt annat, annars hamnar den över saker
    pygame.draw.rect(WIN,BLACK, BORDER)
    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y)) #använd blit för att få fram saker på skärmen, ritar saker från övre vänstra hörnet
    WIN.blit(RED_SPACESHIP, (red.x, red.y))
    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)

    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)

    pygame.display.update()

def yellow_movement(keys_pressed, yellow):
    if keys_pressed[pygame.K_a] and yellow.x -VEL > 0:  # Left
        yellow.x -= VEL
    if keys_pressed[pygame.K_d] and yellow.x + VEL + yellow.width < BORDER.x:  # Right
        yellow.x += VEL
    if keys_pressed[pygame.K_w] and yellow.y -VEL > 0:  # Up
        yellow.y -= VEL
    if keys_pressed[pygame.K_s] and yellow.y + VEL + yellow.height < HEIGHT:  # Down
        yellow.y += VEL

def red_movement(keys_pressed, red):
    if keys_pressed[pygame.K_LEFT] and red.x - VEL > BORDER.x + BORDER.width:  # Left
        red.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and red.x + VEL + red.width < WIDTH:  # Right
        red.x += VEL
    if keys_pressed[pygame.K_UP] and red.y -VEL > 0:  # Up
        red.y -= VEL
    if keys_pressed[pygame.K_DOWN] and red.y + VEL + red.height < HEIGHT:  # Down
        red.y += VEL

def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets:
        bullet.x += BULLET_VEL
        if red.colliderect(bullet): #om gul krockade med bullet
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet.x -= BULLET_VEL
        if yellow.colliderect(bullet): #om gul krockade med bullet
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)


def main():
    red = pygame.Rect(700, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    yellow = pygame.Rect(100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

    red_bullets = []
    yellow_bullets = []
    clock = pygame.time.Clock() #Cappar fps
    run = True
    while run:
        clock.tick(fps) #Cappar fps
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(yellow.x + yellow.width, (yellow.y + yellow.height)//2, 10, 5)
                    yellow_bullets.append(bullet)

                if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(red.x, (yellow.y + yellow.height) // 2, 10, 5)
                    red_bullets.append(bullet)


        handle_bullets(yellow_bullets, red_bullets, yellow, red)


        keys_pressed = pygame.key.get_pressed()
        yellow_movement(keys_pressed, yellow)
        red_movement(keys_pressed, red)

        draw_window(red, yellow, red_bullets, yellow_bullets)
    pygame.quit()

if __name__ == "__main__": #Bra att ha, sa inte riktigt varför
    main()