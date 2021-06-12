# region Initalisation and State variables

import numpy, time, pygame

from images import sprites, TILE_SIZE, TILE_HEIGHT, TILE_WIDTH
from saves import *

pygame.init()
TILES_IN_WIDTH = 15
TILES_IN_HEIGHT = 11
TILES_IN_SCREEN = numpy.array((TILES_IN_WIDTH, TILES_IN_HEIGHT), dtype=numpy.int)
SCREEN_WIDTH = TILE_WIDTH * TILES_IN_WIDTH
SCREEN_HEIGHT = TILE_HEIGHT * TILES_IN_HEIGHT
SCREEN_SIZE = numpy.array((SCREEN_WIDTH, SCREEN_HEIGHT), dtype=numpy.int)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Mage Wars")

FPS = 60 # frames per second setting
clock = pygame.time.Clock()

game_quit = False
screen_update_required = True

# endregion

# region Sprites

class Tile_Map(pygame.sprite.Sprite):
    
    def __init__(self):
        super().__init__()
        
        self.tile_images = sprites["grounds"]
        self.entity_images = sprites["entities"]
        width = TILE_WIDTH * (TILES_IN_WIDTH + 2)
        height = TILE_HEIGHT * (TILES_IN_HEIGHT + 2)

        self.image = pygame.Surface((width, height))

        self.map = save_data["map"]
        self.map_chunk_properties = save_data["map_chunk_properties"]

        self.player_tile_position_in_map = save_data["player_tile_position"]
        self.player_offset_position_in_map = save_data["player_offset_position"]
        #self.player_tile_position_in_map = numpy.array(save_data["player_tile_position"])
        #self.player_offset_position_in_map = numpy.array(save_data["player_offset_position"])

        player_tile_offset_x, player_tile_offset_y = self.player_offset_position_in_map
        self.position = - player_tile_offset_x - TILE_WIDTH // 2, player_tile_offset_y - TILE_HEIGHT
        #self.position = - self.player_tile_position_in_map - TILE_SIZE // 2

        self.rect = self.image.get_rect(topleft = self.position)

        self.map_chunk_entities = save_data["map_chunk_entities"]

        self.need_to_blit_everything = True

    def get_tile_property(self, x, y, tile_property):

        chunk_x, chunk_y = x // CHUNK_SIZE_WIDTH, y // CHUNK_SIZE_HEIGHT
        
        x_coord_in_chunk, y_coord_in_chunk = x % CHUNK_SIZE_WIDTH, y % CHUNK_SIZE_HEIGHT

        temperature = self.map_chunk_properties[tile_property][chunk_x, chunk_y]

        if x_coord_in_chunk < CHUNK_SIZE_WIDTH_DIV_2 and chunk_x - 1 >= 0:
            temperature_left_chunk = self.map_chunk_properties[tile_property][chunk_x-1][chunk_y]
            temperature = (temperature * (x_coord_in_chunk + CHUNK_SIZE_WIDTH_DIV_2) + temperature_left_chunk * (CHUNK_SIZE_WIDTH_DIV_2 - x_coord_in_chunk)) // CHUNK_SIZE_WIDTH
        
        elif x_coord_in_chunk > CHUNK_SIZE_WIDTH_DIV_2 and chunk_x + 1 < len(self.map_chunk_properties[tile_property]):
            temperature_right_chunk = self.map_chunk_properties[tile_property][chunk_x+1][chunk_y]
            temperature = (temperature * (CHUNK_SIZE_WIDTH + CHUNK_SIZE_WIDTH_DIV_2 - x_coord_in_chunk) + temperature_right_chunk * (x_coord_in_chunk - CHUNK_SIZE_WIDTH_DIV_2)) // CHUNK_SIZE_WIDTH

        if y_coord_in_chunk < CHUNK_SIZE_HEIGHT_DIV_2 and chunk_y - 1 >= 0:
            temperature_down_chunk = self.map_chunk_properties[tile_property][chunk_x][chunk_y-1]
            temperature = (temperature * (y_coord_in_chunk + CHUNK_SIZE_HEIGHT_DIV_2) + temperature_down_chunk * (CHUNK_SIZE_HEIGHT_DIV_2 - y_coord_in_chunk)) // CHUNK_SIZE_HEIGHT

        elif y_coord_in_chunk > CHUNK_SIZE_HEIGHT_DIV_2 and chunk_y + 1 < len(self.map_chunk_properties[tile_property][0]):
            temperature_up_chunk = self.map_chunk_properties[tile_property][chunk_x][chunk_y+1]
            temperature = (temperature * (CHUNK_SIZE_HEIGHT + CHUNK_SIZE_HEIGHT_DIV_2 - y_coord_in_chunk) + temperature_up_chunk * (y_coord_in_chunk - CHUNK_SIZE_HEIGHT_DIV_2)) // CHUNK_SIZE_HEIGHT

        return temperature

    def tile_type_based_on_properties(self, x, y):

        temperature = self.get_tile_property(x, y, "temperature")
        humidity = self.get_tile_property(x, y, "humidity")

        '''if temperature > 323 or humidity < 20:
            return "desert"'''

        if temperature > HIGH_COEFFICIENT:
            return "desert"

        if humidity < LOW_COEFFICIENT:
            return "cursed"

        if temperature < LOW_COEFFICIENT:
            return "snow"

        if humidity > HIGH_COEFFICIENT:
            return "swampy"

        else:
            return "plains"
        
    def get_tile_name(self, x, y):

        # return KEY_MAP[self.map[x][y]]

        tile_name = ""

        tile_modifiers = []
        tile_type = ""
        tile_id = self.map[x][y]
        
        if 0 <= tile_id <= 4:
            tile_type = "grass"

            tile_modifiers.append(self.tile_type_based_on_properties(x, y))
        
        tile_name = tile_type + "_" + str(tile_id)

        if tile_modifiers:
            tile_name = "_".join(tile_modifiers) + "_" + tile_name
        
        return tile_name

    def blit_everything(self):
        self.blit_tiles()
        self.blit_entities()

    def blit_tiles(self):
        x_mid, y_mid = self.player_tile_position_in_map
        #x_start, y_start = x_mid - TILES_IN_WIDTH // 2 - 1, y_mid - TILES_IN_HEIGHT // 2 - 1
        #x_stop, y_stop = x_mid + TILES_IN_WIDTH // 2 + 1, y_mid + TILES_IN_HEIGHT // 2 + 1

        x_start, y_start = self.player_tile_position_in_map - TILES_IN_SCREEN // 2 - 1
        x_stop, y_stop = self.player_tile_position_in_map + TILES_IN_SCREEN // 2 + 1

        blit_pos_x = 0
        for x in range(x_start, x_stop + 1):
            blit_pos_y = (TILES_IN_HEIGHT + 1) * TILE_HEIGHT
            for y in range(y_start, y_stop + 1):
                tile_name = self.get_tile_name(x, y)  # KEY_MAP[self.map[x][y]]
                self.image.blit(self.tile_images[tile_name], (blit_pos_x, blit_pos_y))
                blit_pos_y -= TILE_HEIGHT
            blit_pos_x += TILE_WIDTH

        global screen_update_required
        screen_update_required = True

    def blit_entities(self):
        x_mid, y_mid = self.player_tile_position_in_map
        x_start, y_start = x_mid - TILES_IN_WIDTH // 2 - 1, y_mid - TILES_IN_HEIGHT // 2 - 1
        x_stop, y_stop = x_mid + TILES_IN_WIDTH // 2 + 1, y_mid + TILES_IN_HEIGHT // 2 + 1

        chunk_x_start, chunk_y_start = x_start // CHUNK_SIZE_WIDTH, y_start // CHUNK_SIZE_HEIGHT
        chunk_x_stop, chunk_y_stop = x_stop // CHUNK_SIZE_WIDTH, y_stop // CHUNK_SIZE_HEIGHT
        blit_pos_chunk_x = - TILE_WIDTH * (x_start % CHUNK_SIZE_WIDTH)

        for chunk_x in range(chunk_x_start, chunk_x_stop+1):
            blit_pos_chunk_y = TILE_HEIGHT * (y_start % CHUNK_SIZE_HEIGHT + TILES_IN_HEIGHT + 1)
            for chunk_y in range(chunk_y_start, chunk_y_stop+1):
                for i in range(ENTITIES_PER_CHUNK):
                    offset_x, offset_y, entity_id = self.map_chunk_entities[chunk_x, chunk_y][i]
                    if entity_id == 0:
                        break
                    blit_pos_x = blit_pos_chunk_x + TILE_WIDTH * offset_x
                    blit_pos_y = blit_pos_chunk_y - TILE_WIDTH * offset_y

                    entity_name = KEY_ENTITIES[entity_id]
                    x, y = chunk_x * CHUNK_SIZE_WIDTH + offset_x, chunk_y * CHUNK_SIZE_HEIGHT + offset_y
                    if entity_name == "tree":
                        entity_modifier = self.tile_type_based_on_properties(x, y)
                        entity_name = entity_modifier + "_" + entity_name
                    self.image.blit(self.entity_images[entity_name], (blit_pos_x, blit_pos_y))

                blit_pos_chunk_y -= TILE_HEIGHT * CHUNK_SIZE_HEIGHT
            blit_pos_chunk_x += TILE_WIDTH * CHUNK_SIZE_WIDTH

        global screen_update_required
        screen_update_required = True

    def on_player_move(self):
        player_tile_offset_x, player_tile_offset_y = self.player_offset_position_in_map
        self.position = - player_tile_offset_x - TILE_WIDTH // 2, player_tile_offset_y - TILE_WIDTH
        self.rect = self.image.get_rect(topleft = self.position)

    def check_collision(self, x, y):
        chunk_x, chunk_y = x // CHUNK_SIZE_WIDTH, y // CHUNK_SIZE_HEIGHT
        chunk_pos_x, chunk_pos_y = x % CHUNK_SIZE_WIDTH, y % CHUNK_SIZE_HEIGHT

        chunk_entities = self.map_chunk_entities[chunk_x, chunk_y]

        for entity in chunk_entities:
            x, y, id = entity

            if id == 0:
                return False

            else:
                if chunk_pos_x == x and chunk_pos_y == y:
                    return True

    def shift(self, direction):
        """Direction can take values 'up', 'down', "left', 'right'"""
        if direction not in ("up", "down", "left", "right"): 
            raise Exception("unknown direction: " + direction)        

        elif direction == "up":
            self.image.blit(self.image, (0, TILE_HEIGHT))
            x_mid, y_mid = self.player_tile_position_in_map
            y = y_mid + TILES_IN_HEIGHT // 2 + 1
            x_start = x_mid - TILES_IN_WIDTH // 2 - 1
            x_stop = x_mid + TILES_IN_WIDTH // 2 + 1

            blit_pos_x = 0
            blit_pos_y = 0 #SCREEN_HEIGHT + TILE_SIZE

            for x in range(x_start, x_stop + 1):
                tile_name = self.get_tile_name(x, y)  # KEY_MAP[self.map[x][y]]
                self.image.blit(self.tile_images[tile_name], (blit_pos_x, blit_pos_y))
                blit_pos_x += TILE_WIDTH

            self.blit_entities()

        elif direction == "right":
            self.image.blit(self.image, (-TILE_WIDTH, 0))
            
            x_mid, y_mid = self.player_tile_position_in_map
            x = x_mid + TILES_IN_WIDTH // 2 + 1
            y_start = y_mid - TILES_IN_HEIGHT // 2 - 1
            y_stop = y_mid + TILES_IN_HEIGHT // 2 + 1

            blit_pos_y = (TILES_IN_HEIGHT + 1) * TILE_HEIGHT
            blit_pos_x = SCREEN_WIDTH + TILE_WIDTH

            for y in range(y_start, y_stop + 1):
                tile_name = self.get_tile_name(x, y)  # KEY_MAP[self.map[x][y]]
                self.image.blit(self.tile_images[tile_name], (blit_pos_x, blit_pos_y))
                blit_pos_y -= TILE_HEIGHT

            self.blit_entities()

        elif direction == "down":
            self.image.blit(self.image, (0, -TILE_HEIGHT))

            x_mid, y_mid = self.player_tile_position_in_map
            y = y_mid - TILES_IN_HEIGHT // 2 - 1
            x_start = x_mid - TILES_IN_WIDTH // 2 - 1
            x_stop = x_mid + TILES_IN_WIDTH // 2 + 1

            blit_pos_x = 0
            blit_pos_y = SCREEN_HEIGHT + TILE_HEIGHT

            for x in range(x_start, x_stop + 1):
                tile_name = self.get_tile_name(x, y)  # KEY_MAP[self.map[x][y]]
                self.image.blit(self.tile_images[tile_name], (blit_pos_x, blit_pos_y))
                blit_pos_x += TILE_WIDTH

            self.blit_entities()

        elif direction == "left":
            self.image.blit(self.image, (TILE_WIDTH, 0))

            x_mid, y_mid = self.player_tile_position_in_map
            x = x_mid - TILES_IN_WIDTH // 2 - 1
            y_start = y_mid - TILES_IN_HEIGHT // 2 - 1
            y_stop = y_mid + TILES_IN_HEIGHT // 2 + 1

            blit_pos_y = (TILES_IN_HEIGHT + 1) * TILE_HEIGHT
            blit_pos_x = 0

            for y in range(y_start, y_stop + 1):
                tile_name = self.get_tile_name(x, y)  # KEY_MAP[self.map[x][y]]
                self.image.blit(self.tile_images[tile_name], (blit_pos_x, blit_pos_y))
                blit_pos_y -= TILE_HEIGHT

            self.blit_entities()
            
        world_map.need_to_blit_world_map = True

    def update(self):
        if self.need_to_blit_everything:
            self.blit_everything()
            self.need_to_blit_everything = False

class World_Map(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()

        # Screen size - size of two tiles
        self.max_map_size = SCREEN_SIZE - TILE_SIZE * 2
        
        self.chunk_size_in_map = save_data["chunk_size_in_world_map"]

        self.chunks_in_map = self.max_map_size // self.chunk_size_in_map

        # Adjust map size
        self.max_map_size = self.chunks_in_map * self.chunk_size_in_map

        self.tiles = {
            "blessed": pygame.Surface(self.chunk_size_in_map),
            "cursed": pygame.Surface(self.chunk_size_in_map),
            "desert": pygame.Surface(self.chunk_size_in_map),
            "plains": pygame.Surface(self.chunk_size_in_map),
            "snow": pygame.Surface(self.chunk_size_in_map),
            "swampy": pygame.Surface(self.chunk_size_in_map)
        }
        self.tiles["blessed"].fill((240, 187, 222))
        self.tiles["cursed"].fill((147, 71, 66))
        self.tiles["desert"].fill((232, 179, 109))
        self.tiles["plains"].fill((137, 209, 82))
        self.tiles["snow"].fill((218, 224, 215))
        self.tiles["swampy"].fill((65, 156, 80))

        self.player_position = tile_map.player_tile_position_in_map

        self.need_to_blit_world_map = True

    def blit_world_map(self):
        get_tile_type = tile_map.tile_type_based_on_properties
        map_height = self.max_map_size[1]
        chunk_width, chunk_height = self.chunk_size_in_map
        chunks_in_width_of_map, chunks_in_height_of_map = self.chunks_in_map
        chunks_in_width_of_map_div_2 = chunks_in_width_of_map // 2
        chunks_in_height_of_map_div_2 = chunks_in_height_of_map // 2

        player_chunk_x, player_chunk_y = self.player_position // CHUNK_SIZE

        chunk_x_start = max(player_chunk_x-chunks_in_width_of_map_div_2, 0)
        chunk_x_end = min(player_chunk_x+chunks_in_width_of_map_div_2, CHUNKS_IN_WIDTH_OF_MAP - 1)

        chunk_y_start = max(player_chunk_y-chunks_in_height_of_map_div_2, 0)
        chunk_y_end = min(player_chunk_y+chunks_in_height_of_map_div_2, CHUNKS_IN_HEIGHT_OF_MAP - 1)

        self.current_chunks_in_map = numpy.array((chunk_x_end-chunk_x_start, chunk_y_end-chunk_y_start), dtype=numpy.int)

        self.current_map_size = self.chunks_in_map * self.chunk_size_in_map

        self.image = pygame.Surface(self.current_map_size)

        self.position = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
        self.rect = self.image.get_rect(center = self.position)

        # Offset
        blit_start_x = 0
        blit_start_y = map_height - chunk_height

        blit_x = blit_start_x
        for chunk_x in range(chunk_x_start, chunk_x_end + 1):
            blit_y = blit_start_y
            for chunk_y in range(chunk_y_start, chunk_y_end + 1):
                x = chunk_x * CHUNK_SIZE_WIDTH + CHUNK_SIZE_WIDTH_DIV_2
                y = chunk_y * CHUNK_SIZE_HEIGHT + CHUNK_SIZE_HEIGHT_DIV_2
                tile_type = get_tile_type(x, y)
                self.image.blit(self.tiles[tile_type], (blit_x, blit_y))
                blit_y -= chunk_height
            blit_x += chunk_width
    
    def update(self):
        if self.need_to_blit_world_map:
            self.blit_world_map()
            self.need_to_blit_world_map = False

class Player(pygame.sprite.Sprite):
    
    def __init__(self):
        super().__init__()
        
        self.images = sprites["player"]
        self.direction = "up"
        self.image = self.images["idle_up"]
        
        # pos_x = TILE_WIDTH * (TILES_IN_WIDTH//2)
        # pos_y = TILE_HEIGHT * (TILES_IN_HEIGHT//2)
        pos_x = SCREEN_WIDTH // 2
        pos_y = SCREEN_HEIGHT // 2
        self.position = pos_x, pos_y
        self.rect = self.image.get_rect(center = self.position)

        self.player_move_speed = save_data["player_move_speed"]
        #self.player_tile_position_in_map = save_data["player_tile_position"]
        #self.player_offset_position_in_map = save_data["player_offset_position"]
        self.player_tile_position_in_map = tile_map.player_tile_position_in_map
        self.player_offset_position_in_map = tile_map.player_offset_position_in_map
        

        self.last_key_pressed = None

        self.animation_stage = 0
        self.animation_step_max_duration = 15
        self.animation_step_duration = 0

    def for_keys_pressed(self, keys_pressed):
        if self.last_key_pressed:
            if keys_pressed[self.last_key_pressed]:
                self.move()
                return

        if keys_pressed[pygame.K_UP]:
            self.direction = "up"
            self.last_key_pressed = pygame.K_UP

        elif keys_pressed[pygame.K_RIGHT]:
            self.direction = "right"
            self.last_key_pressed = pygame.K_RIGHT

        elif keys_pressed[pygame.K_DOWN]:
            self.direction = "down"
            self.last_key_pressed = pygame.K_DOWN

        elif keys_pressed[pygame.K_LEFT]:
            self.direction = "left"
            self.last_key_pressed = pygame.K_LEFT

        else:
            self.last_key_pressed = None
            return

        self.move()

    def move(self):

        if self.direction == "up":
            self.player_offset_position_in_map[1] += self.player_move_speed

            if self.player_offset_position_in_map[1] > TILE_HEIGHT:
                self.player_tile_position_in_map[1] += 1
                if tile_map.check_collision(*self.player_tile_position_in_map):
                    self.player_tile_position_in_map[1] -= 1
                    self.player_offset_position_in_map[1] = TILE_HEIGHT
                    return
                tile_map.shift(self.direction)
                self.player_offset_position_in_map[1] = 0

        elif self.direction == "right":
            self.player_offset_position_in_map[0] += self.player_move_speed
            
            if self.player_offset_position_in_map[0] > TILE_WIDTH:
                self.player_tile_position_in_map[0] += 1
                if tile_map.check_collision(*self.player_tile_position_in_map):
                    self.player_tile_position_in_map[0] -= 1
                    self.player_offset_position_in_map[0] = TILE_WIDTH
                    return
                self.player_offset_position_in_map[0] = 0
                tile_map.shift(self.direction)

        elif self.direction == "down":
            self.player_offset_position_in_map[1] -= self.player_move_speed

            if self.player_offset_position_in_map[1] < 0:
                self.player_tile_position_in_map[1] -= 1
                if self.player_tile_position_in_map[1] < 0:
                    self.player_tile_position_in_map[1] = 0
                else:
                    if tile_map.check_collision(*self.player_tile_position_in_map):
                        self.player_tile_position_in_map[1] += 1
                        self.player_offset_position_in_map[1] = 0
                        return
                    self.player_offset_position_in_map[1] = TILE_HEIGHT
                    tile_map.shift(self.direction)
            
        elif self.direction == "left":
            self.player_offset_position_in_map[0] -= self.player_move_speed

            if self.player_offset_position_in_map[0] < 0:
                self.player_tile_position_in_map[0] -= 1
                if self.player_tile_position_in_map[0] < 0:
                    self.player_tile_position_in_map[0] = 0
                else:
                    if tile_map.check_collision(*self.player_tile_position_in_map):
                        self.player_tile_position_in_map[0] += 1
                        self.player_offset_position_in_map[0] = 0
                        return
                    self.player_offset_position_in_map[0] = TILE_WIDTH
                    tile_map.shift(self.direction)

        tile_map.on_player_move()

        self.animation_step_duration += 1
        if self.animation_step_duration == self.animation_step_max_duration:
            if self.animation_stage == 3:
                self.animation_stage = 0
            else:
                self.animation_stage += 1
            
            self.animation_step_duration = 0

        self.image = self.images["walk_" + self.direction + "_" + str(self.animation_stage)]

        global screen_update_required
        screen_update_required = True

    def stop_moving(self):
        self.image = self.images["idle_" + self.direction]
        self.is_moving = False  

class Character_Shadow(pygame.sprite.Sprite):
    
    def __init__(self, position):
        super().__init__()

        self.image = sprites["shadow"]
        self.position = position
        self.rect = self.image.get_rect(center = self.position)

class UI(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()

        self.fonts = {
            "normal": pygame.font.SysFont(None, 20),
        }

        self.details_to_print = []

    def entities_description_in_chunk(self):
        entities = []

        x, y = tile_map.player_tile_position_in_map

        chunk_x, chunk_y = x // CHUNK_SIZE_WIDTH, y // CHUNK_SIZE_HEIGHT
        # chunk_pos_x, chunk_pos_y = x % CHUNK_SIZE_WIDTH, y % CHUNK_SIZE_HEIGHT

        chunk_entities = tile_map.map_chunk_entities[chunk_x, chunk_y]

        for entity_x, entity_y, entity_id in chunk_entities:
            if entity_id != 0:
                entities.append(f"{KEY_ENTITIES[entity_id]} at ({entity_x + chunk_x * CHUNK_SIZE_WIDTH}, {entity_y + chunk_y * CHUNK_SIZE_HEIGHT})")

        return entities

    def label(self, content, font_key = "normal", color = (0, 0, 0)):
        label_surface = self.fonts[font_key].render(str(content), True, color)
        return label_surface

    def draw(self, screen):
        tile_position = tile_map.player_tile_position_in_map
        tile_offset = tile_map.player_offset_position_in_map
        position = numpy.round(tile_position + tile_offset / TILE_SIZE, decimals=1)

        chunk_position = tile_position // CHUNK_SIZE
        chunk_offset = tile_position % CHUNK_SIZE
        #chunk = numpy.round(chunk_position + chunk_offset / CHUNK_SIZE, decimals=1)

        chunk_properties_description = []
        for chunk_property_name in world_manager.map_chunk_properties:
            chunk_property_value = round(tile_map.map_chunk_properties[chunk_property_name][chunk_position[0]][chunk_position[1]], 2)
            chunk_properties_description.append(f"{chunk_property_name.capitalize()}: {chunk_property_value}")

        tile_properties_description = []
        for tile_property_name in world_manager.map_chunk_properties:
            tile_property_value = round(tile_map.get_tile_property(*tile_position, tile_property_name), 2)
            tile_properties_description.append(f"{tile_property_name.capitalize()}: {tile_property_value}")

        chunk_entities_description = self.entities_description_in_chunk()

        fps = round(clock.get_fps())

        to_display_top_left = ["Position: " + str(position), *tile_properties_description]
        to_display_top_right = ["Chunk: " + str(chunk_position), *chunk_properties_description, *ORBS_DETAILS]
        to_display_bottom_left = [*chunk_entities_description]
        to_display_bottom_right = ["FPS: " + str(fps)]

        to_display_top_left_max_width = 0
        current_blit_position = numpy.array((10, 10), dtype=numpy.int)
        for content in to_display_top_left:
            content_label = self.label(content)
            content_label_rect = content_label.get_rect(topleft=current_blit_position)
            screen.blit(content_label, current_blit_position)
            current_blit_position += [0, content_label_rect.height]
            to_display_top_left_max_width = max(to_display_top_left_max_width, content_label_rect.width)

        current_blit_position = numpy.array((SCREEN_WIDTH - 10, 10), dtype=numpy.int)
        for content in to_display_top_right:
            content_label = self.label(content)
            content_label_rect = content_label.get_rect(topright=current_blit_position)
            screen.blit(content_label, content_label_rect)
            current_blit_position += [0, content_label_rect.height]

        current_blit_position = numpy.array((10, SCREEN_HEIGHT - 10), dtype=numpy.int)
        for content in to_display_bottom_left:
            content_label = self.label(content)
            content_label_rect = content_label.get_rect(bottomleft=current_blit_position)
            screen.blit(content_label, content_label_rect)
            current_blit_position -= [0, content_label_rect.height]

        current_blit_position = numpy.array((SCREEN_WIDTH - 10, SCREEN_HEIGHT - 10), dtype=numpy.int)
        for content in to_display_bottom_right:
            content_label = self.label(content)
            content_label_rect = content_label.get_rect(bottomright=current_blit_position)
            screen.blit(content_label, content_label_rect)
            current_blit_position -= [0, content_label_rect.height]

# endregion

# region miscellaneous classes

class World_Manager():

    def __init__(self):
        self.map_chunk_properties = save_data["map_chunk_properties"]

        self.properties = self.map_chunk_properties.keys()

        self.equilibrium_property_values = save_data["equilibrium_property_values"]

        self.map_chunk_entities = save_data["map_chunk_entities"]

        self.chunks_having_orbs = []
        self.update_chunks_having_orbs()

    def update_chunks_having_orbs(self):
        self.chunks_having_orbs = []

        for chunk_x in range(0, CHUNKS_IN_WIDTH_OF_MAP):
            for chunk_y in range(0, CHUNKS_IN_HEIGHT_OF_MAP):
                entities = self.map_chunk_entities[chunk_x, chunk_y]
                for i, (offset_x, offset_y, entity_id) in enumerate(entities):
                    if entity_id == 0:
                        break

                    elif KEY_ENTITIES_ORBS_START <= entity_id <= KEY_ENTITIES_ORBS_END:
                        self.chunks_having_orbs.append((chunk_x, chunk_y, i))
                    
                    else:
                        pass

    def get_chunk_property(self, x, y, chunk_property_name):
        chunk_x, chunk_y = x // CHUNK_SIZE_WIDTH, y // CHUNK_SIZE_HEIGHT

        chunk_property_value = self.map_chunk_properties[chunk_property_name][chunk_x, chunk_y]

        return chunk_property_value

    def set_chunk_property(self, x, y, chunk_property_name, chunk_property_value):
        chunk_x, chunk_y = x // CHUNK_SIZE_WIDTH, y // CHUNK_SIZE_HEIGHT

        self.map_chunk_properties[chunk_property_name][chunk_x, chunk_y] = chunk_property_value

    def diffuse_property(self, chunk_property):
        self.map_chunk_properties[chunk_property] = (self.map_chunk_properties[chunk_property] + numpy.roll(self.map_chunk_properties[chunk_property], 1) + numpy.roll(self.map_chunk_properties[chunk_property], -1) + numpy.roll(self.map_chunk_properties[chunk_property], 1, axis=0) + numpy.roll(self.map_chunk_properties[chunk_property], -1, axis=0) )/5

        # below code prevents wrapping of the array (kinda)
        self.map_chunk_properties[chunk_property][0] = self.map_chunk_properties[chunk_property][1]
        self.map_chunk_properties[chunk_property][-1] = self.map_chunk_properties[chunk_property][-2]
        self.map_chunk_properties[chunk_property][:, 0] = self.map_chunk_properties[chunk_property][:, 1]
        self.map_chunk_properties[chunk_property][:, -1] = self.map_chunk_properties[chunk_property][:, -2]

        tile_map.need_to_blit_everything = True
        world_map.need_to_blit_world_map = True

    def orbs_effect_on_chunks(self):
        for chunk_x, chunk_y, i in self.chunks_having_orbs:
            offset_x, offset_y, entity_id = self.map_chunk_entities[chunk_x, chunk_y, i]
            if not KEY_ENTITIES_ORBS_START <= entity_id <= KEY_ENTITIES_ORBS_END:
                print("ORBS POSITIONS CHANGED BUT NOT UPDATED")
                raise Exception

            property_affected, new_propery_value = ORB_PROPERTY_EFFECT[KEY_ENTITIES[entity_id]]
            self.map_chunk_properties[property_affected][chunk_x, chunk_y] = new_propery_value
                        
        tile_map.need_to_blit_everything = True
        world_map.need_to_blit_world_map = True

    """def entity_effect_on_chunks(self):
        chunk_properties_difference_from_equilibrium = {}
        for chunk_property in self.properties:
            chunk_properties_difference_from_equilibrium[chunk_property] = self.equilibrium_property_values[chunk_property] - self.map_chunk_properties[chunk_property]        
        for chunk_x in range(0, CHUNKS_IN_WIDTH_OF_MAP):
            for chunk_y in range(0, CHUNKS_IN_HEIGHT_OF_MAP):
                entities = self.map_chunk_entities[chunk_x, chunk_y]

                for offset_x, offset_y, entity_id in entities:
                    if entity_id == None:
                        break
                    
                    # entity-tree's effect
                    elif entity_id == 1:
                        for chunk_property in self.properties:
                            self.map_chunk_properties[chunk_property][chunk_x, chunk_y] += int(chunk_properties_difference_from_equilibrium[chunk_property][chunk_x, chunk_y] * 0.1)

                    elif 2 <= entity_id <= 7:
                        self.orb_effect_on_chunk(chunk_x, chunk_y, entity_id)
                        
        tile_map.need_to_blit_everything = True
        world_map.need_to_blit_world_map = True"""

# endregion

# region Sprites and Sprite Groups Initialisation

sprites_to_render = pygame.sprite.Group()

tile_map = Tile_Map()
sprites_to_render.add(tile_map)

world_map = World_Map()

player_shadow = Character_Shadow((SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 28))
sprites_to_render.add(player_shadow)

player = Player()
sprites_to_render.add(player)

world_manager = World_Manager()

ui = UI()

# endregion

# region Miscellaneous

start = time.time()
world_manager.orbs_effect_on_chunks()
print("Entities effect time:", time.time() - start)

start = time.time()
world_manager.diffuse_property("temperature")
print("Propeties spread time: ", time.time() - start)

def run_entities():
    world_manager.orbs_effect_on_chunks()
    
def run_chunk_properties_diffusion():
    for chunk_property in save_data["map_chunk_properties"]:
        world_manager.diffuse_property(chunk_property)

def time_warp():
    for i in range(500):
        run_entities()
        run_chunk_properties_diffusion()
    print("TIME WARPED.")

for i in range(0):
    time_warp()

USER_EVENTS = {
    pygame.USEREVENT + 1: {"delay": 500, "function": run_entities},
    pygame.USEREVENT + 2: {"delay": 500, "function": run_chunk_properties_diffusion},
    #pygame.USEREVENT + 3: {"delay": 2000, "function": time_warp}
}

for event_key, event_values in USER_EVENTS.items():
    pygame.time.set_timer(event_key, event_values["delay"])

# endregion

# region Game Loop

while not game_quit:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_quit = True

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_q:
                game_quit = True

            if event.key == pygame.K_1:
                for chunk_property in world_manager.properties:
                    world_manager.diffuse_property(chunk_property)

            if event.key == pygame.K_2:
                world_manager.orbs_effect_on_chunks()

            if event.key == pygame.K_3:
                time_warp()

            if event.key == pygame.K_m:
                if world_map in sprites_to_render:
                    sprites_to_render.remove(world_map)
                else:
                    sprites_to_render.add(world_map)
                screen_update_required = True

        elif event.type in USER_EVENTS:
            USER_EVENTS[event.type]["function"]()

    keys_pressed = pygame.key.get_pressed()
    player.for_keys_pressed(keys_pressed)

    sprites_to_render.update()

    if screen_update_required:
        sprites_to_render.draw(screen)
        ui.draw(screen)
        pygame.display.update()
        screen_update_required = False

    clock.tick(FPS)

# endregion
