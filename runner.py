import pygame
from sys import exit
from random import randint, choice

DISPLAY_WIDTH = 800
DISPLAY_HEIGHT = 400
DISPLAY_TITLE = 'Pixel Runner'
SPEED = 1


class Background(pygame.sprite.Sprite):
    def __init__(self, number, *args):
        self.image = pygame.image.load('graphics/background.png').convert()
        self.rect = self.image.get_rect()
        self._layer = -10
        pygame.sprite.Sprite.__init__(self, *args)
        self.moved = 0
        self.number = number
        self.rect.x = self.rect.width * self.number

    def update(self):
        self.rect.move_ip(-SPEED, 0)
        self.moved += SPEED

        if self.moved >= self.rect.width:
            self.rect.x = self.rect.width * self.number
            self.moved = 0


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        walk_1 = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
        walk_2 = pygame.image.load('graphics/player/player_walk_2.png').convert_alpha()
        self.walk = [walk_1, walk_2]
        self.animation_index = 0
        self.jump = pygame.image.load('graphics/player/jump.png').convert_alpha()
        self.image = self.walk[self.animation_index]
        self.rect = self.image.get_rect(midbottom=(80, 300))
        self.gravity = 0
        self.jump_sound = pygame.mixer.Sound('audio/jump.mp3')
        self.jump_sound.set_volume(0.1)

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom == 300:
            self.gravity = -20
            self.jump_sound.play()

    def animation_state(self):
        if self.rect.bottom < 300:
            self.image = self.jump
        else:
            self.animation_index += 0.1
            self.image = self.walk[int(self.animation_index) % 2]

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, obstacle_type):
        super().__init__()
        if obstacle_type == 'fly':
            frame_1 = pygame.image.load('graphics/fly/fly1.png').convert_alpha()
            frame_2 = pygame.image.load('graphics/fly/fly2.png').convert_alpha()
            self.frames = [frame_1, frame_2]
            y_pos = 210
        else:
            frame_1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
            frame_2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
            self.frames = [frame_1, frame_2]
            y_pos = 300

        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom=(randint(900, 1100), y_pos))

    def animation_state(self):
        self.animation_index += 0.1
        self.image = self.frames[int(self.animation_index) % 2]

    def update(self):
        self.animation_state()
        self.rect.x -= (SPEED + 3)
        self.destroy()

    def destroy(self):
        if self.rect.x <= 0 - self.rect.width:
            self.kill()


def restart_scene():
    if language == 'English':
        score_message = font.render(f'Your score : {score}', False, (111, 196, 169))
    elif language == 'Turkce':
        score_message = font.render(f'Skorunuz : {score}', False, (111, 196, 169))
    else:
        score_message = font.render(f'Twoj wynik : {score}', False, (111, 196, 169))
    score_message_rectangle = score_message.get_rect(center=(400, 80))
    screen.blit(score_message, score_message_rectangle)
    screen.blit(player_stand, player_stand_rectangle)
    screen.blit(game_message, game_message_rectangle)
    screen.blit(settings_icon, settings_rect)
    player.sprite.rect.bottom = 300


def start_scene():
    screen.blit(game_name, game_name_rectangle)
    screen.blit(player_stand, player_stand_rectangle)
    screen.blit(game_message, game_message_rectangle)
    screen.blit(settings_icon, settings_rect)


def settings_scene():
    language_message = font.render('' + language, False, (111, 196, 169))
    language_rect = language_message.get_rect(center=(400, 300))

    screen.blit(language_message, language_rect)
    screen.blit(return_icon, return_rect)
    screen.blit(turkish_icon, turkish_rect)
    screen.blit(english_icon, english_rect)
    screen.blit(polish_icon, polish_rect)


# Game variables
pygame.init()
screen = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
pygame.display.set_caption(DISPLAY_TITLE)
icon = pygame.image.load('graphics/appicon.png').convert_alpha()
pygame.display.set_icon(icon)
clock = pygame.time.Clock()
game_running = False
start_time = 0
score = 0
font = pygame.font.Font('font/pixeltype.ttf', 50)
bg_music = pygame.mixer.Sound('audio/music.wav')
bg_music.set_volume(0.1)
death_sound = pygame.mixer.Sound('audio/death.mp3')
death_sound.set_volume(0.1)

settings_icon = pygame.image.load('graphics/icons/settings.png')
settings_rect = settings_icon.get_rect(midbottom=(50, 375))

return_icon = pygame.image.load('graphics/icons/return.png')
return_rect = return_icon.get_rect(midtop=(50, 25))

in_settings = False
language = 'English'

turkish_icon = pygame.image.load('graphics/icons/turkish.png')
turkish_rect = turkish_icon.get_rect(midleft=(100, 200))
english_icon = pygame.image.load('graphics/icons/english.png')
english_rect = english_icon.get_rect(midleft=(336, 200))
polish_icon = pygame.image.load('graphics/icons/polish.png')
polish_rect = polish_icon.get_rect(midleft=(564, 200))

# Groups
player = pygame.sprite.GroupSingle()
player.add(Player())
background_group = pygame.sprite.LayeredUpdates()
Background(0, background_group)
Background(1, background_group)

obstacle_group = pygame.sprite.Group()

# Intro/Game Over Screen
player_stand = pygame.image.load('graphics/player/player_stand.png').convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand, 0, 2)
player_stand_rectangle = player_stand.get_rect(center=(400, 200))

game_name = font.render('Pixel Runner', False, (111, 196, 169))
if language == 'English':
    game_message = font.render('Press Space to Run!', False, (111, 196, 169))
elif language == 'Turkce':
    game_message = font.render('Kosmak icin bosluk tusuna basin!', False, (111, 196, 169))
else:
    language = 'Polski'
    game_message = font.render('Nacisnij spacje, aby uruchomic!', False, (111, 196, 169))
game_name_rectangle = game_name.get_rect(center=(400, 80))
game_message_rectangle = game_message.get_rect(center=(400, 330))

# Timers
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1400)

snail_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(snail_animation_timer, 500)

fly_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(fly_animation_timer, 200)

difficulty_timer = pygame.USEREVENT + 4
pygame.time.set_timer(difficulty_timer, 1000)

while True:

    if game_running:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == obstacle_timer:
                obstacle_group.add(Obstacle(choice(['fly', 'snail', 'snail', 'snail'])))

            if event.type == difficulty_timer:
                SPEED += 0.1

        background_group.update()
        background_group.draw(screen)
        current_time = pygame.time.get_ticks() - start_time
        score = int(current_time / 1000)
        if language == 'English':
            score_surface = font.render(f"Score :  {int(current_time / 1000)}", False, (64, 64, 64))
        elif language == 'Turkce':
            score_surface = font.render(f"Skor :  {int(current_time / 1000)}", False, (64, 64, 64))
        else:
            score_surface = font.render(f"Wynik :  {int(current_time / 1000)}", False, (64, 64, 64))
        score_rectangle = score_surface.get_rect(center=(400, 50))
        screen.blit(score_surface, score_rectangle)
        # Player Movement
        player.draw(screen)
        player.update()

        # Obstacle Movement
        obstacle_group.draw(screen)
        obstacle_group.update()

        # Collision
        if pygame.sprite.spritecollide(player.sprite, obstacle_group, False):
            bg_music.stop()
            death_sound.play()
            game_running = False

    else:
        screen.fill((94, 129, 162))

        if in_settings:
            settings_scene()
        elif score == 0:
            start_scene()
        else:
            restart_scene()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:
                    if settings_rect.collidepoint(pygame.mouse.get_pos()):
                        in_settings = True

            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:
                    if return_rect.collidepoint(pygame.mouse.get_pos()):
                        in_settings = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:
                    if turkish_rect.collidepoint(pygame.mouse.get_pos()):
                        game_message = font.render('Kosmak icin bosluk tusuna basin!', False, (111, 196, 169))
                        game_message_rectangle = game_message.get_rect(center=(400, 330))
                        language = 'Turkce'

            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:
                    if english_rect.collidepoint(pygame.mouse.get_pos()):
                        game_message = font.render('Press Space to Run!', False, (111, 196, 169))
                        game_message_rectangle = game_message.get_rect(center=(400, 330))
                        language = 'English'

            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:
                    if polish_rect.collidepoint(pygame.mouse.get_pos()):
                        game_message = font.render('Nacisnij spacje, aby uruchomic!', False, (111, 196, 169))
                        game_message_rectangle = game_message.get_rect(center=(400, 330))
                        language = 'Polski'

            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and not in_settings:
                SPEED = 1
                obstacle_group.empty()
                bg_music.play(loops=-1)
                start_time = pygame.time.get_ticks()
                game_running = True

    pygame.display.update()
    clock.tick(60)
