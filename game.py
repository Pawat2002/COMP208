import pygame
from pygame.locals import *
import pygame.mixer

pygame.mixer.init()

pygame.mixer.music.load("arcade_music.mp3")
pygame.mixer.music.play(-1)

pygame.init()

clock = pygame.time.Clock()
fps = 60

screen_width = 800
screen_height = 800

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Treasure Trove : The Coin Conquest")

# define game tile size
tile_size = 40
status1 = 0  # status for player 1
status2 = 0  # status for player 2
total_lives = 3
main_menu = True

# load imgs
bg = pygame.image.load('bg.png')
gameover_img = pygame.image.load('gameover.png')
start_img = pygame.image.load('start.png')
quit_img = pygame.image.load("quit.png")


class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.image = pygame.transform.scale(self.image, (120, 80))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.clicked = False

    def draw(self):
        action = False

        screen.blit(self.image, self.rect)
        # mouse position
        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                action = True
                self.clicked = True
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
        return action


# sound effects
jumpSound = pygame.mixer.Sound("jump.wav")
coinSound = pygame.mixer.Sound("coinSound.mp3")
gameoverSound = pygame.mixer.Sound("gameoverSound.mp3")


def bg_music():
    if not pygame.mixer.music.get_busy():
        # Load audio file
        pygame.mixer.music.load("arcade_music.mp3")
        # play the music
        pygame.mixer.music.play(-1)
        # set bg_music volume
        pygame.mixer.music.set_volume(0.2)


# create player
class Player():
    def __init__(self, x, y):
        img = pygame.image.load('people.png')
        self.image = pygame.transform.scale(img, (40, 80))
        self.original_image = self.image  # Store original image for flipping
        # obtain position of people
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.vel_y = 0
        self.jumped = False  # track if player has jumped
        self.on_ground = True  # Track if player is on the ground
        #self.lives = 3
        self.started_moving = False  # Track if the player has started moving
        self.jumpSound = pygame.mixer.Sound("jump.wav")
        self.gameoverSound = pygame.mixer.Sound("gameoverSound.mp3")

        # Timer
        self.initial_time = pygame.time.get_ticks()  # Initial time in milliseconds
        self.timer = 30  # Initial time in seconds
        self.timer_font = pygame.font.Font(None, 36)  # Font for timer display
        self.lives_font = pygame.font.Font(None, 36)  # Font for lives display

    def reset_timer(self):
        self.initial_time = pygame.time.get_ticks()  # Reset the initial time
        self.timer = 30  # Reset the timer to its initial value

    # movement of people
    def update(self, status1, total_lives):
        dx = 0
        dy = 0

        if total_lives > 0:
            if status1 == 0:
                # get keypresses
                key = pygame.key.get_pressed()
                if key[pygame.K_UP] and self.jumped == False and self.on_ground:
                    self.vel_y = -15
                    self.jumped = True
                    self.on_ground = False  # Update on_ground status
                    self.started_moving = True  # Player has started moving
                    self.jumpSound.play()
                if key[pygame.K_UP] == False:
                    self.jumped = False
                if key[pygame.K_LEFT]:
                    dx -= 5
                    self.image = pygame.transform.flip(self.original_image, True, False)  # Flip the image horizontally
                    self.started_moving = True  # Player has started moving
                if key[pygame.K_RIGHT]:
                    dx += 5
                    self.image = self.original_image  # Reset the image to its original state
                    self.started_moving = True  # Player has started moving

                # Timer starts when the player starts moving
                if self.started_moving:
                    # add gravity
                    self.vel_y += 1
                    if self.vel_y > 3:
                        self.vel_y = 3

                    dy += self.vel_y

                    # check collision
                    for tile in world.tile_list:
                        # x direction
                        if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                            # check if below the ground eg jumping
                            dx = 0

                        # y direction
                        if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                            # check if below the ground eg jumping
                            if self.vel_y < 0:
                                dy = tile[1].bottom - self.rect.top
                                self.vel_y = 0
                                self.on_ground = False  # Update on_ground status

                            # falling
                            elif self.vel_y >= 0:
                                dy = tile[1].top - self.rect.bottom
                                self.vel_y = 0
                                self.on_ground = True  # Update on_ground status

                    # check collision with enemies
                    if pygame.sprite.spritecollide(self, enemy_group, False):
                        status1 = -1
                        total_lives -= 1  # Decrease lives when colliding with enemies
                        self.initial_time = pygame.time.get_ticks()  # Reset the timer

                    # Timer update
                    if self.started_moving:
                        current_time = pygame.time.get_ticks()  # Current time in milliseconds
                        elapsed_seconds = (current_time - self.initial_time) // 1000  # Elapsed time in seconds
                        self.timer = max(0, 30 - elapsed_seconds)  # Calculate remaining time

                        if self.timer == 0:  # Timer has run out
                            total_lives -= 1  # Decrease lives by 1
                            self.initial_time = pygame.time.get_ticks()  # Reset initial time
                            self.rect.x = 100  # Reset player's position
                            self.rect.y = screen_height - 130
                            if total_lives == 0:  # No more lives left
                                status1 = -1  # Set status1 to indicate game over
                                self.rect.x = 100  # Reset player's position
                                self.rect.y = screen_height - 130

                    # update player coordinates
                    self.rect.x += dx
                    self.rect.y += dy

                    # Check if player reaches the door
                    if pygame.sprite.spritecollide(self, door_group, False):
                        status1 = 1

                # Draw player onto screen
                screen.blit(self.image, self.rect)
                #pygame.draw.rect(screen, (255, 255, 255), self.rect, 2)

                # Draw timer
                #timer_text = self.timer_font.render("Time: " + str(self.timer), True, (255, 255, 255))
                #screen.blit(timer_text, (630, 38))

                # Draw lives
                #lives_text = self.lives_font.render("Lives: " + str(self.lives), True, (255, 255, 255))
                #screen.blit(lives_text, (530, 38))

            elif status1 == -1:
                self.rect.x = 70
                self.rect.y = screen_height - 130
                status1 = 0  # reset game with player died


            elif status1 == 1:  # reaches the door
                self.rect.x = 70
                self.rect.y = screen_height - 130
                status1 = 2

        if total_lives == 0:  # cant reset game with player have no lives left
            status1 = -1
            gameover_button.draw()
            self.gameoverSound.play()

        return status1, total_lives


class Player2():
    def __init__(self, x, y):
        img = pygame.image.load('people2.png')
        self.image = pygame.transform.scale(img, (40, 80))
        self.original_image = self.image  # Store original image for flipping
        # obtain position of people
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.vel_y = 0
        self.jumped = False  # track if player has jumped
        self.on_ground = True  # Track if player is on the ground
        #self.lives = 3
        self.started_moving = False  # Track if the player has started moving
        self.jumpSound = pygame.mixer.Sound("jump.wav")
        self.gameoverSound = pygame.mixer.Sound("gameoverSound.mp3")

        # Timer
        self.initial_time = pygame.time.get_ticks()  # Initial time in milliseconds
        self.timer = 30  # Initial time in seconds
        self.timer_font = pygame.font.Font(None, 36)  # Font for timer display
        self.lives_font = pygame.font.Font(None, 36)  # Font for lives display

    def reset_timer(self):
        self.initial_time = pygame.time.get_ticks()  # Reset the initial time
        self.timer = 30  # Reset the timer to its initial value

    # movement of people
    def update(self, status2, total_lives):
        dx = 0
        dy = 0

        if total_lives > 0:
            if status2 == 0:
                # get keypresses
                key = pygame.key.get_pressed()
                if key[pygame.K_w] and self.jumped == False and self.on_ground:
                    self.vel_y = -15
                    self.jumped = True
                    self.on_ground = False  # Update on_ground status
                    self.started_moving = True  # Player has started moving
                    self.jumpSound.play()
                if key[pygame.K_w] == False:
                    self.jumped = False
                if key[pygame.K_a]:
                    dx -= 5
                    self.image = pygame.transform.flip(self.original_image, True, False)  # Flip the image horizontally
                    self.started_moving = True  # Player has started moving
                if key[pygame.K_d]:
                    dx += 5
                    self.image = self.original_image  # Reset the image to its original state
                    self.started_moving = True  # Player has started moving

                # Timer starts when the player starts moving
                if self.started_moving:
                    # add gravity
                    self.vel_y += 1
                    if self.vel_y > 3:
                        self.vel_y = 3

                    dy += self.vel_y

                    # check collision
                    for tile in world.tile_list:
                        # x direction
                        if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                            # check if below the ground eg jumping
                            dx = 0

                        # y direction
                        if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                            # check if below the ground eg jumping
                            if self.vel_y < 0:
                                dy = tile[1].bottom - self.rect.top
                                self.vel_y = 0
                                self.on_ground = False  # Update on_ground status

                            # falling
                            elif self.vel_y >= 0:
                                dy = tile[1].top - self.rect.bottom
                                self.vel_y = 0
                                self.on_ground = True  # Update on_ground status

                    # check collision with enemies
                    if pygame.sprite.spritecollide(self, enemy_group, False):
                        status2 = -1
                        total_lives -= 1  # Decrease lives when colliding with enemies
                        self.initial_time = pygame.time.get_ticks()  # Reset the timer

                    # Timer update
                    current_time = pygame.time.get_ticks()  # Current time in milliseconds
                    elapsed_seconds = (current_time - self.initial_time) // 1000  # Elapsed time in seconds
                    self.timer = max(0, 30 - elapsed_seconds)  # Calculate remaining time

                    if self.timer == 0:  # Timer has run out
                        total_lives -= 1  # Decrease lives by 1
                        self.initial_time = pygame.time.get_ticks()  # Reset initial time
                        self.rect.x = 100  # Reset player's position
                        self.rect.y = screen_height - 130
                        if total_lives == 0:  # No more lives left
                            status2 = -1  # Set status1 to indicate game over
                            self.rect.x = 100  # Reset player's position
                            self.rect.y = screen_height - 130

                    # update player coordinates
                    self.rect.x += dx
                    self.rect.y += dy

                    # Check if player reaches the door
                    if pygame.sprite.spritecollide(self, door_group, False):
                        status2 = 1

                # Draw player onto screen
                screen.blit(self.image, self.rect)
                #pygame.draw.rect(screen, (255, 255, 255), self.rect, 2)

                # Draw timer
                #timer_text = self.timer_font.render("Time: " + str(self.timer), True, (255, 255, 255))
                #screen.blit(timer_text, (630, 38))

                # Draw lives
                #lives_text = self.lives_font.render("Lives: " + str(self.lives), True, (255, 255, 255))
                #screen.blit(lives_text, (530, 38))

            elif status2 == -1:
                self.rect.x = 40
                self.rect.y = screen_height - 130
                status2 = 0  # reset game with player died

            elif status2 == 1:  # reaches the door
                status2 = 2
                self.rect.x = 40
                self.rect.y = screen_height - 130

            if total_lives == 0:  # cant reset game with player have no lives left
                status2 = -1
                gameover_button.draw()
                self.gameoverSound.play()

        return status2, total_lives


class World():
    def __init__(self, data):
        self.tile_list = []
        brick_img = pygame.image.load('brick.png')
        block_img = pygame.image.load('block.png')
        row_count = 0
        for row in data:
            col_count = 0
            for tile in row:
                if tile == 1:
                    img = pygame.transform.scale(brick_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = tile_size * col_count
                    img_rect.y = tile_size * row_count
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 2:
                    coin = Coin(col_count * tile_size, row_count * tile_size)
                    coin_group.add(coin)

                if tile == 3:
                    img = pygame.transform.scale(block_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = tile_size * col_count
                    img_rect.y = tile_size * row_count
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 4:
                    enemy = Enemy(col_count * tile_size, row_count * tile_size)
                    enemy_group.add(enemy)

                if tile == 5:
                    door = Door(col_count * tile_size, row_count * tile_size)
                    door_group.add(door)
                col_count += 1
            row_count += 1

    # draw world to screen
    def draw(self):
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])
            #pygame.draw.rect(screen, (255, 255, 255), tile[1], 2)


# create enemy
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("enemy.png")
        self.image = pygame.transform.scale(self.image, (40, 40))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Door(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("door.png")
        self.image = pygame.transform.scale(self.image, (40, 40))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("coin.png")
        self.image = pygame.transform.scale(self.image, (30, 30))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.coinSound = pygame.mixer.Sound("coinSound.mp3")


# select positions for world
level1_world = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 5, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 3, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 3, 0, 0, 3, 3, 3, 3, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 4, 0, 0, 2, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 3, 3, 3, 0, 0, 3, 1],
    [1, 0, 0, 0, 0, 3, 3, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 3, 3, 0, 0, 3, 3, 3, 3, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 3, 3, 3, 3, 3, 3, 3, 3, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 2, 4, 1],
    [1, 0, 0, 0, 0, 3, 3, 3, 3, 3, 0, 0, 0, 0, 3, 0, 0, 3, 3, 1],
    [1, 0, 0, 0, 3, 3, 3, 3, 3, 3, 3, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 0, 0, 4, 0, 0, 1],
    [1, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 1],
]

level2_world = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 3, 3, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 3, 3, 0, 0, 0, 1],
    [1, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 5, 0, 1],
    [1, 0, 0, 0, 0, 3, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 3, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 3, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 3, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 4, 1],
    [1, 0, 0, 0, 0, 0, 3, 0, 0, 3, 0, 0, 3, 0, 0, 3, 0, 3, 3, 1],
    [1, 0, 0, 0, 0, 3, 3, 0, 4, 3, 0, 4, 3, 0, 4, 3, 0, 3, 3, 1],
    [1, 0, 0, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 4, 3, 3, 1],
    [1, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 1],
]

player = Player(70, screen_height - 120)
player2 = Player2(40, screen_height - 120)

enemy_group = pygame.sprite.Group()
door_group = pygame.sprite.Group()
coin_group = pygame.sprite.Group()

world = World(level1_world)
finalLevel = False

gameover_button = Button(screen_width // 2 - 75, screen_height // 2, gameover_img)
start_button = Button(screen_width // 2 - 150, screen_height // 2 - 40, start_img)
quit_button = Button(screen_width // 2 + 75, screen_height // 2 - 40, quit_img)

coins_collected = 0
coins_font = pygame.font.Font(None, 36)

run = True
while run:
    clock.tick(fps)
    screen.blit(bg, (0, 0))
    if main_menu == True:
        if start_button.draw():
            main_menu = False
        if quit_button.draw():
            run = False
    else:
        world.draw()
        enemy_group.draw(screen)
        door_group.draw(screen)
        coin_group.draw(screen)
        status1, total_lives = player.update(status1, total_lives)
        status2, total_lives = player2.update(status2, total_lives)

        # Update coins collected and render on screen
        for coin in coin_group:
            if player.rect.colliderect(coin.rect) or player2.rect.colliderect(coin.rect):
                coin_group.remove(coin)
                coins_collected += 1
                coinSound.play()

        coins_text = coins_font.render("Coins: " + str(coins_collected), True, (255, 255, 255))
        screen.blit(coins_text, (30, 30))

        # combined timer
        min_timer = min(player.timer, player2.timer)
        timer_text = player.timer_font.render("Time: " + str(min_timer), True, (255, 255, 255))
        screen.blit(timer_text, (630, 38))

        # combined lives
        #min_lives = min(player.lives, player2.lives)
        lives_text = player.lives_font.render("Lives: " + str(total_lives), True, (255, 255, 255))
        screen.blit(lives_text, (530, 38))

        if status1 == 2 and status2 == 2:
            if finalLevel:  # both reaches door
                gameover_button.draw()
            else:
                status1 = 0
                status2 = 0
                coins_collected = 0
                total_lives = 3
                player.reset_timer()  # Reset timer for player 1
                player2.reset_timer()
                world = World(level2_world)
                finalLevel = True

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()
