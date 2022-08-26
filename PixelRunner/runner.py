import pygame
from sys import exit

DISPLAY_WIDTH = 800
DISPLAY_HEIGHT = 400
DISPLAY_TITLE = 'Pixel Runner'


def display_score(start_time, font, screen):
    current_time = pygame.time.get_ticks() - start_time
    score_surface = font.render(f"Score :  {int(current_time / 1000)}", False, (64, 64, 64))
    score_rectangle = score_surface.get_rect(center=(400, 50))
    screen.blit(score_surface, score_rectangle)
    return int(current_time / 1000)


def run():
    pygame.init()
    screen = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
    pygame.display.set_caption(DISPLAY_TITLE)
    icon_surface = pygame.image.load('graphics/icon.png').convert_alpha()
    pygame.display.set_icon(icon_surface)

    clock = pygame.time.Clock()

    game_running = False
    start_time = 0
    score = 0

    font = pygame.font.Font('font/pixeltype.ttf', 50)

    sky_surface = pygame.image.load('graphics/sky.png').convert_alpha()
    ground_surface = pygame.image.load('graphics/ground.png').convert_alpha()

    snail_surface = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
    snail_rectangle = snail_surface.get_rect(bottomright=(800, 300))

    player_surface = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
    player_rectangle = player_surface.get_rect(bottomleft=(80, 300))
    player_gravity = 0

    # Intro/Game Over Screen
    player_stand_surface = pygame.image.load('graphics/player/player_stand.png').convert_alpha()
    player_stand_surface = pygame.transform.rotozoom(player_stand_surface, 0, 2)
    player_stand_rectangle = player_stand_surface.get_rect(center=(400, 200))

    game_name_surface = font.render('Pixel Runner', False, (111, 196, 169))
    game_name_rectangle = game_name_surface.get_rect(center=(400, 80))

    game_message_surface = font.render('Press Space to Run!', False, (111, 196, 169))
    game_message_rectangle = game_message_surface.get_rect(center=(400, 330))

    while True:

        if game_running:

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if event.type == pygame.MOUSEBUTTONDOWN and player_rectangle.bottom >= 300 and player_rectangle \
                        .collidepoint(event.pos):
                    player_gravity = -22

                if event.type == pygame.KEYDOWN and player_rectangle.bottom >= 300 and event.key == pygame.K_SPACE:
                    player_gravity = -22

            screen.blit(sky_surface, (0, 0))
            screen.blit(ground_surface, (0, 300))
            score = display_score(start_time, font, screen)

            snail_rectangle.right -= 4

            if snail_rectangle.right <= 0:
                snail_rectangle.left = 800

            screen.blit(snail_surface, snail_rectangle)

            # Player
            player_gravity += 1
            player_rectangle.y += player_gravity
            if player_rectangle.bottom >= 300:
                player_rectangle.bottom = 300
            screen.blit(player_surface, player_rectangle)

            # Collision
            if snail_rectangle.colliderect(player_rectangle):
                game_running = False
        else:
            screen.fill((94, 129, 162))
            screen.blit(player_stand_surface, player_stand_rectangle)

            screen.blit(game_message_surface, game_message_rectangle)
            if score == 0:
                screen.blit(game_name_surface, game_name_rectangle)
            else:
                score_message = font.render(f'Your score : {score}', False, (111, 196, 169))
                score_message_rectangle = score_message.get_rect(center=(400, 80))
                screen.blit(score_message, score_message_rectangle)


            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    snail_rectangle.bottomright = (800, 300)
                    start_time = pygame.time.get_ticks()
                    game_running = True

        pygame.display.update()
        clock.tick(60)


if __name__ == '__main__':
    run()
