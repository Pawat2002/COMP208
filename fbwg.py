import pygame
from pygame import mixer

# Initialize pygame
pygame.init()

# set game window
screen_width = 1000
screen_height = 1000
screen = pygame.display.set_mode((screen_width, screen_height))

# set game title name and fonts
pygame.display.set_caption("Fire boy and Water girl")
tile_size = 100

sky_img = pygame.image.load('sky.jpg')

def bg_music():
    if not pygame.mixer.music.get_busy():
        # Load audio file
        mixer.music.load("arcade_music.mp3")
        #play the music
        mixer.music.play(-1)
        #set bg_music volume
        pygame.mixer.music.set_volume(0.3)


def draw_grid():
    for line in range(0, 12):
        pygame.draw.line(screen, (255, 255, 255), (0, line * tile_size), (screen_width, line * tile_size))
        pygame.draw.line(screen, (255, 255, 255), (line * tile_size, 0), (line * tile_size, screen_height))

class World():
    def __init__(self,data):
        self.tile_list = []
        dirt_img = pygame.image.load('brick.png')
        grass_img = pygame.image.load('grass.webp')
        row_count = 0
        for row in data:
            col_count = 0
            for tile in row:
                if tile == 1:
                    img = pygame.transform.scale(dirt_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = tile_size * col_count
                    img_rect.y = tile_size * row_count
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 2:
                    img = pygame.transform.scale(grass_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = tile_size * col_count
                    img_rect.y = tile_size * row_count
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                col_count += 1
            row_count += 1

    def draw(self):
        for tile in self.tile_list:
            screen.blit(tile[0],tile[1])

world_data = [
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 2, 2, 2, 2, 2, 2, 2, 2, 1],
]

world = World(world_data)
# if save_button.draw():
     #pickle_out(world_data,pickle_out)

run = True
while run:
    bg_music()
    screen.blit(sky_img, (0, 0))
    world.draw()
    draw_grid()




    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()
