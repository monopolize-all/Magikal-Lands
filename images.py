"""
Source:
https://pixel-boy.itch.io/ninja-adventure-asset-pack
"""

# REMOVE REDUNDANT TASK

import pygame, os
from PIL import Image
import numpy
from numpy import asarray, rot90, fliplr, where as numpy_where, all as numpy_all, array

# region Constants

IMAGES_PATH = "Images"

TILE_SIZE = numpy.array((64, 64), dtype=numpy.int)
TILE_HEIGHT, TILE_WIDTH = TILE_SIZE

# endregion

def get_keyed_tiles(TILESET_PATH, TILESET_KEYS):
    KEYED_TILESET = {}
    # TILESET = asarray(Image.open(TILESET_PATH).convert("RGB"))
    TILESET = array(asarray(Image.open(TILESET_PATH)))

    # handle alpha channel
    TILESET[numpy_all(TILESET == (1, 2, 3, 255), axis=-1)] = (1, 2, 3, 0)
    TILESET[numpy_where(TILESET[:, :, 3] == 0)] = (1, 2, 3, 0)
    
    for key, val in TILESET_KEYS.items():
        #postx, posty = val
        #posx, posy = postx * TILE_SIZE, posty * TILE_SIZE

        posx, posy = TILE_SIZE * val

        # REMOVE REDUNDANT TASK of rotating image via numpy.rot90 and numpy.fliplr
        numpy_image = rot90(fliplr(TILESET[posy:posy+TILE_HEIGHT, posx:posx+TILE_WIDTH]), 1)
        
        KEYED_TILESET[key] = pygame.surfarray.make_surface(numpy_image[:,:,:3])
        KEYED_TILESET[key].set_colorkey((1, 2, 3))
    return KEYED_TILESET

#pixels[np.all(pixels == (0, 255, 0), axis=-1)] = (255,255,255)

# region Player Tileset

PLAYER_TILESET_PATH = os.path.join(IMAGES_PATH, "character_spritesheet.png")
PLAYER_TILESET_KEYS = {
    "idle_down": (0, 0),
    "idle_up": (1, 0),
    "idle_left": (2, 0),
    "idle_right": (3, 0),
    "walk_down_0": (0, 0),
    "walk_up_0": (1, 0),
    "walk_left_0": (2, 0),
    "walk_right_0": (3, 0),
    "walk_down_1": (0, 1),
    "walk_up_1": (1, 1),
    "walk_left_1": (2, 1),
    "walk_right_1": (3, 1),
    "walk_down_2": (0, 2),
    "walk_up_2": (1, 2),
    "walk_left_2": (2, 2),
    "walk_right_2": (3, 2),
    "walk_down_3": (0, 3),
    "walk_up_3": (1, 3),
    "walk_left_3": (2, 3),
    "walk_right_3": (3, 3),
}
PLAYER = get_keyed_tiles(PLAYER_TILESET_PATH, PLAYER_TILESET_KEYS)

# endregion

# region Ground Tileset

GROUND_TILESET_PATH = os.path.join(IMAGES_PATH, "ground_spritesheet.png")
GROUND_TILESET_KEYS = {
    "desert_grass_0": (0, 5),
    "desert_grass_1": (1, 5),
    "desert_grass_2": (2, 5),
    "desert_grass_3": (3, 5),
    "desert_grass_4": (4, 5),

    "plains_grass_0": (0, 12),
    "plains_grass_1": (1, 12),
    "plains_grass_2": (2, 12),
    "plains_grass_3": (3, 12),
    "plains_grass_4": (4, 12),

    "snow_grass_0": (0, 19),
    "snow_grass_1": (1, 19),
    "snow_grass_2": (2, 19),
    "snow_grass_3": (3, 19),
    "snow_grass_4": (4, 19),

    "blessed_grass_0": (11, 5),
    "blessed_grass_1": (12, 5),
    "blessed_grass_2": (13, 5),
    "blessed_grass_3": (14, 5),
    "blessed_grass_4": (15, 5),

    "swampy_grass_0": (11, 12),
    "swampy_grass_1": (12, 12),
    "swampy_grass_2": (13, 12),
    "swampy_grass_3": (14, 12),
    "swampy_grass_4": (15, 12),

    "cursed_grass_0": (11, 19),
    "cursed_grass_1": (12, 19),
    "cursed_grass_2": (13, 19),
    "cursed_grass_3": (14, 19),
    "cursed_grass_4": (15, 19),
}
GROUNDS = get_keyed_tiles(GROUND_TILESET_PATH, GROUND_TILESET_KEYS)

# endregion

# region Entity Tileset

ENTITY_TILESET_PATH = os.path.join(IMAGES_PATH, "entities_spritesheet.png")
ENTITY_TILESET_KEYS = {
    "plains_tree": (0, 0),
    "desert_tree": (1, 0),
    "swampy_tree": (2, 0),
    "snow_tree": (3, 0),
    "blessed_tree": (4, 0),
    "cursed_tree": (1, 0),
    "humid_orb": (0, 1),
    "dry_orb": (1, 1),
    "frozen_orb": (2, 1),
    "desert_orb": (3, 1),
    "blessed_orb": (4, 1),
    "cursed_orb": (5, 1),
}
ENTITIES = get_keyed_tiles(ENTITY_TILESET_PATH, ENTITY_TILESET_KEYS)

# endregion

# region Final Grouping

sprites = {
    "player": PLAYER,
    "shadow": pygame.image.load(os.path.join(IMAGES_PATH, "Shadow.png")),
    "grounds": GROUNDS,
    "entities": ENTITIES,
}

# endregion
