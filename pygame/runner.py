import pygame
from sys import exit

DISPLAY_WIDTH = 800
DISPLAY_HEIGHT = 400
DISPLAY_TITLE = 'Runner'


def run():
    pygame.init()
    screen = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
    pygame.display.set_caption(DISPLAY_TITLE)

    clock = pygame.time.Clock()

    font = pygame.font.Font('font/pixeltype.ttf', 50)

    sky_surface = pygame.image.load('graphics/sky.png').convert_alpha()
    ground_surface = pygame.image.load('graphics/ground.png').convert_alpha()

    score_surface = font.render('My game', False, (64, 64, 64))
    score_rectangle = score_surface.get_rect(center=(400, 50))

    snail_surface = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
    snail_rectangle = snail_surface.get_rect(bottomright=(800, 300))

    player_surface = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
    player_rectangle = player_surface.get_rect(bottomleft=(80, 300))
    player_gravity = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            # if event.type == pygame.MOUSEMOTION:
            #    if player_rectangle.collidepoint(event.pos):
            #        print('collision')
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player_gravity = -20

        screen.blit(sky_surface, (0, 0))
        screen.blit(ground_surface, (0, 300))
        pygame.draw.rect(screen, '#c0e8ec', score_rectangle, 0, 6)
        screen.blit(score_surface, score_rectangle)

        snail_rectangle.right -= 4

        if snail_rectangle.right <= 0:
            snail_rectangle.left = 800

        screen.blit(snail_surface, snail_rectangle)

        # Player
        player_gravity += 1
        player_rectangle.y += player_gravity
        screen.blit(player_surface, player_rectangle)

        # pressed_keys = pygame.key.get_pressed()
        # if pressed_keys[pygame.K_SPACE]:
        #    print('jump')

        # if player_rectangle.colliderect(snail_rectangle):
        #    print('collision')

        # mouse_position = pygame.mouse.get_pos()
        # if player_rectangle.collidepoint(mouse_position):
        #    print(pygame.mouse.get_pressed())
        pygame.display.update()
        clock.tick(60)


if __name__ == '__main__':
    run()
