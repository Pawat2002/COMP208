import pygame
from pygame.locals import *

pygame.init()

clock = pygame.time.Clock()
fps = 60

screen_width = 800
screen_height = 800

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Fire boy and Water girl")

# define game tile size
tile_size = 40
game_over = 0
main_menu = True


# load imgs
bg = pygame.image.load('bg.png')
reset = pygame.image.load('gameover.png')
start = pygame.image.load('start.png')
quit = pygame.image.load("quit.png")
jumpSound = pygame.mixer.Sound("jump.wav")

def bg_music():
    if not pygame.mixer.music.get_busy():
        # Load audio file
        mixer.music.load("arcade_music.mp3")
        #play the music
        mixer.music.play(-1)
        #set bg_music volume
        pygame.mixer.music.set_volume(0.3)


class Button():
    def __init__(self,x,y,image):
        self.image = image
        self.image = pygame.transform.scale(self.image, (120, 80))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.clicked = False
    def draw(self):
        action = False

        screen.blit(self.image,self.rect)
        # mouse position
        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                action = True
                self.clicked = True
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
        return action




def draw_grid():
    for line in range(0, 20):
        pygame.draw.line(screen, (255, 255, 255), (0, line * tile_size), (screen_width, line * tile_size))
        pygame.draw.line(screen, (255, 255, 255), (line * tile_size, 0), (line * tile_size, screen_height))


# create player
class Player():
    def __init__(self, x, y):
        img = pygame.image.load('people.png')
        self.image = pygame.transform.scale(img, (40, 80))
        # obtain position of people
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.vel_y = 0
        self.jumped = False
        self.lives = 3

    # movement of people
    def update(self,game_over):
        dx = 0
        dy = 0

        if game_over == 0:
            # get keypresses
            key = pygame.key.get_pressed()
            if key[pygame.K_SPACE] and self.jumped == False:
                jumpSound.play()
                self.vel_y = -15
                self.jumped = True
            if key[pygame.K_SPACE] == False:
                self.jumped = False
            if key[pygame.K_LEFT]:
                dx -= 5
            if key[pygame.K_RIGHT]:
                dx += 5

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

                    # falling
                    elif self.vel_y >= 0:
                        dy = tile[1].top - self.rect.bottom
                        self.vel_y = 0

            # check collision with enemies
            if pygame.sprite.spritecollide(self,enemy_group , False):
                game_over = -1
                self.lives -= 1  # Decrease lives when colliding with enemies




            # update player coordinates
            self.rect.x += dx
            self.rect.y += dy

        elif game_over == -1:
            self.rect.x = 100
            self.rect.y = screen_height - 130
            game_over = 0
            if self.lives == 0:
                game_over = -1
                reset_button.draw()

        # draw player onto screen
        screen.blit(self.image, self.rect)
        pygame.draw.rect(screen, (255, 255, 255), self.rect, 2)
        return(game_over)

class World():
    def __init__(self, data):
        self.tile_list = []
        dirt_img = pygame.image.load('brick.png')
        coin_img = pygame.image.load('coin.png')
        block_img = pygame.image.load('block.png')
        door_img = pygame.image.load('door.png')
        row_count = 0
        for row in data:
            col_count = 0
            for tile in row:
                if tile == 1:  # tile_list[0] dirt
                    img = pygame.transform.scale(dirt_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = tile_size * col_count
                    img_rect.y = tile_size * row_count
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 2:  # tile_list[0] dirt
                    coin = Coin(col_count * tile_size, row_count * tile_size)
                    coin_group.add(coin)

                if tile == 3:  # tile_list[2] block
                    img = pygame.transform.scale(block_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = tile_size * col_count
                    img_rect.y = tile_size * row_count
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 4:  # tile_list[3] enemy
                    enemy = Enemy(col_count * tile_size, row_count * tile_size)
                    enemy_group.add(enemy)

                if tile == 5:  # tile_list[4] door
                    door = Door(col_count * tile_size, row_count * tile_size)
                    door_group.add(door)
                col_count += 1
            row_count += 1

    # draw world to screen
    def draw(self):
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])
            pygame.draw.rect(screen, (255, 255, 255), tile[1], 2)


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


# select positions for world
world_data = [
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

player = Player(100, screen_height - 130)

enemy_group = pygame.sprite.Group()

door_group = pygame.sprite.Group()

coin_group = pygame.sprite.Group()



world = World(world_data)

reset_button = Button(screen_width//2 - 75, screen_height//2,reset)
# if save_button.draw():
# pickle_out(world_data,pickle_out)
start_button = Button(screen_width//2-150, screen_height//2-40,start)
quit_button = Button(screen_width//2+75, screen_height//2-40,quit)



run = True
while run:
    bg_music()
    clock.tick(fps)
    screen.blit(bg, (0, 0))
    if main_menu == True:
        if start_button.draw():
            main_menu = False
        if quit_button.draw():
            run = False
    else:
        world.draw()

        # draw_grid()

        enemy_group.draw(screen)

        door_group.draw(screen)
        coin_group.draw(screen)

        game_over = player.update(game_over)


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()
