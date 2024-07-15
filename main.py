import pygame as pg
import pygame_gui as pgui
import theme
from dataclasses import dataclass

pg.init()
pg.font.init()

screen_width = 900
screen_height = 900
screen = pg.display.set_mode((screen_width, screen_height))

pg.display.set_caption('"<färm::sîm>"')

font = pg.font.SysFont('Arial Black', 30)
debug_font = pg.font.SysFont('Monospace', 16)

clock = pg.time.Clock()

# variables
tile_size = 128
tile_gap = 10
tiles_x = 6
tiles_y = 6
tile_offset_x = (screen_width - tile_size * tiles_x) / 2
tile_offset_y = (screen_height - tile_size * tiles_y) / 2

farm_tiles = []

@dataclass
class FarmTile:
    x: int
    y: int
    grow_time: int
    grow_time_max: int = 120

# stats
wheat = 0

# add farm tiles to farm_tiles set
for x in range(tiles_x):
    for y in range(tiles_y):
        farm_tiles.append(FarmTile(x, y, 0))

# ui
class UI:
    def __init__(self):
        self.manager = pgui.UIManager((screen_width, screen_height))

        self.ui_window_shop = pgui.elements.UIWindow((0, 0, 0, 0), manager=self.manager, visible=False)
        self.ui_window_shop.is_enabled = False

        rect_button_shop = pg.Rect(0, 0, 100, 50)
        self.button_shop = pgui.elements.UIButton(
            relative_rect=rect_button_shop,
            text='Shop',
            manager=self.manager,
            anchors={"bottom":"bottom","right":"right"}
            )
    
    def draw_menu(self):
        button_width = 200
        button_height = 100
        button_amount = 4
        ui_window_menu_shop = (button_width + 10 + 100, button_amount * button_height + 40 + 120)
        ui_window_menu_shop = (screen_width / 2 - ui_window_menu_shop[0] / 2,
                              screen_height / 2 - ui_window_menu_shop[1] / 2)
        rect_ui_window_shop = pg.Rect(ui_window_menu_shop, ui_window_menu_shop)
        self.ui_window_shop = pgui.elements.UIWindow(rect=rect_ui_window_shop, manager=self.manager, window_display_title="Shop")

    def kill_menu(self):
        self.ui_window_shop.kill()


running = True

while running:
    clock.tick(60)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                running = False
        if event.type == pg.MOUSEBUTTONDOWN:
            click_pos = pg.mouse.get_pos()
            for tile in farm_tiles:
                if tile.grow_time == tile.grow_time_max and\
                (((tile.x) * tile_size + tile_gap + tile_offset_x) < click_pos[0] < ((tile.x+1) * tile_size - tile_gap + tile_offset_x)) and\
                (((tile.y) * tile_size + tile_gap + tile_offset_y) < click_pos[1] < ((tile.y+1) * tile_size - tile_gap + tile_offset_y)):
                    tile.grow_time = 0
                    wheat += 1

    # logic stuff

    # farm tiles

    for tile in farm_tiles:
        if tile.grow_time < tile.grow_time_max:
            tile.grow_time += 1

    # graphics stuff
    screen.fill(theme.bg_colour)

    # colour every 64x64 square differently
    for x in range(tiles_x):
        for y in range(tiles_y):
            pg.draw.rect(screen, theme.crop, (
                x * tile_size + tile_gap + tile_offset_x,
                y * tile_size + tile_gap + tile_offset_y,
                tile_size - tile_gap * 2, tile_size - tile_gap * 2
                ))

    # write tile.grow_time to every 64x64 square
    for tile in farm_tiles:
        text_surface = debug_font.render(str(tile.grow_time), False, theme.text, theme.black)
        screen.blit(text_surface, (
            tile.x * tile_size + tile_gap + tile_offset_x,
            tile.y * tile_size + tile_gap + tile_offset_y
            ))

    # stats
    stats_wheat_surface = font.render("Wheat: " + str(wheat), True, theme.black)
    screen.blit(stats_wheat_surface, (20, 20))

    pg.display.update()


pg.quit()