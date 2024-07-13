import pygame as pg
import theme

pg.init()

screen_size_x = 1024
screen_size_y = 1024
screen = pg.display.set_mode((screen_size_x, screen_size_y))

pg.display.set_caption('"<färm::sîm>"')

clock = pg.time.Clock()

# variables
tile_size = 128
tile_gap = 10

running = True

while running:
    clock.tick(60)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                running = False

    # logic stuff

    # get mouse position
    mouse_pos = pg.mouse.get_pos()

    

    # graphics stuff
    screen.fill(theme.bg_colour)

    # colour every 64x64 square differently
    for x in range(int(screen_size_x / tile_size)):
        for y in range(int(screen_size_y / tile_size)):
            pg.draw.rect(screen, theme.crop, (
                x * tile_size + tile_gap,
                y * tile_size + tile_gap,
                tile_size - tile_gap * 2, tile_size - tile_gap * 2
                ))

    pg.display.update()


pg.quit()