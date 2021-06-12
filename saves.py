import json
import numpy
import random

from images import TILE_HEIGHT, TILE_WIDTH

KEY_MAP = [
    "plains_grass_0",
    "plains_grass_1",
    "plains_grass_2",
    "plains_grass_3",
    "plains_grass_4",
]

KEY_ENTITIES_ORBS_START = 2
KEY_ENTITIES_ORBS_END = 5

KEY_ENTITIES = [
    None,  # Denotes no entity
    "tree",
    "humid_orb",
    "dry_orb",
    "frozen_orb",
    "desert_orb",
]

# Manipulate these values to change equilibrium condition
# below affects property values
HUMIDITY_COEFFICIENT = 100
DRY_COEFFICIENT = 0
SNOW_COEFFICIENT = 0
DESERT_COEFFICIENT = 100
# below affects tiles
HIGH_COEFFICIENT = 60
LOW_COEFFICIENT = 40
ORB_PROPERTY_EFFECT = {
    "humid_orb": ["humidity", HUMIDITY_COEFFICIENT ],
    "dry_orb": ["humidity", DRY_COEFFICIENT],
    "frozen_orb": ["temperature", SNOW_COEFFICIENT],
    "desert_orb": ["temperature", DESERT_COEFFICIENT],
}

MAP_SIZE = (1010, 1010)
CHUNK_SIZE = (10, 10)
CHUNK_SIZE_IN_WORLD_MAP = (6, 6)
CHUNKS_IN_MAP = MAP_SIZE[0] // CHUNK_SIZE[0], MAP_SIZE[1] // CHUNK_SIZE[1]
CHUNKS_IN_WIDTH_OF_MAP, CHUNKS_IN_HEIGHT_OF_MAP = CHUNKS_IN_MAP
CHUNK_SIZE_WIDTH, CHUNK_SIZE_HEIGHT = CHUNK_SIZE
CHUNK_SIZE_WIDTH_DIV_2, CHUNK_SIZE_HEIGHT_DIV_2 = CHUNK_SIZE_HEIGHT // 2, CHUNK_SIZE_HEIGHT // 2
CHUNK_ARRAY_DIMENSIONS = (MAP_SIZE[0] // CHUNK_SIZE[0], MAP_SIZE[1] // CHUNK_SIZE[1])
ENTITIES_PER_CHUNK = 10
# Entity: x, y, id
CHUNK_ENTITIES_ARRAY_DIMENSIONS = (MAP_SIZE[0] // CHUNK_SIZE[0], MAP_SIZE[1] // CHUNK_SIZE[1], ENTITIES_PER_CHUNK, 3)

save_data = {
    "player_tile_position": numpy.array([MAP_SIZE[0] // 2, MAP_SIZE[1] // 2]),
    "player_offset_position": numpy.array([TILE_WIDTH // 2, TILE_HEIGHT // 2]),
    "player_move_speed": 1,
    "map": numpy.zeros((MAP_SIZE[0], MAP_SIZE[1]), dtype=numpy.int), #numpy.random.randint(1, 7, (100, 100))
    "map_chunk_properties": {
        #"temperature": numpy.array(([[290, 310], [290, 290]])),  
        #"temperature": numpy.random.choice((260, 290, 330), CHUNK_ARRAY_DIMENSIONS),
        #"temperature": numpy.full(CHUNK_ARRAY_DIMENSIONS, 290, dtype=numpy.int),
        #"humidity": numpy.random.choice((10, 30, 60), CHUNK_ARRAY_DIMENSIONS),
        "temperature": numpy.full(CHUNK_ARRAY_DIMENSIONS, 50, dtype=numpy.int),
        "humidity": numpy.full(CHUNK_ARRAY_DIMENSIONS, 50, dtype=numpy.int),
    },
    "chunk_size_in_world_map": numpy.array(CHUNK_SIZE_IN_WORLD_MAP, dtype = numpy.int),
    "map_chunk_entities": numpy.zeros(CHUNK_ENTITIES_ARRAY_DIMENSIONS, dtype=numpy.int),
    "equilibrium_property_values": {
        "temperature": 50,
        "humidity": 50,
    },
}

# vanity tiles
for _ in range(0, 1000):

    save_data["map"][random.randint(0, 99), random.randint(0, 99)] = random.randint(1, 4)

# trees
NUMBER_OF_TREES = 10000
for _ in range(0, NUMBER_OF_TREES):

    x, y = random.randint(0, CHUNKS_IN_MAP[0] - 1), random.randint(0, CHUNKS_IN_MAP[1] - 1)
    for i in range(ENTITIES_PER_CHUNK):
        if save_data["map_chunk_entities"][x, y, i, 2] == 0:
            break
    else:
        continue

    entity = random.randint(0, CHUNK_SIZE[0] - 1), random.randint(0, CHUNK_SIZE[1] - 1), 1
    save_data["map_chunk_entities"][x, y, i] = numpy.array(entity, dtype=numpy.int)

# orbs
NUMBER_OF_ORBS = 4
ORBS_DETAILS = []
orbs_yet_to_place = list(ORB_PROPERTY_EFFECT.keys())
"""orb_positions = [
    [CHUNKS_IN_WIDTH_OF_MAP // 2, CHUNKS_IN_HEIGHT_OF_MAP // 6],
    [CHUNKS_IN_WIDTH_OF_MAP // 2, CHUNKS_IN_HEIGHT_OF_MAP // 6 * 5],
    [CHUNKS_IN_WIDTH_OF_MAP // 6, CHUNKS_IN_HEIGHT_OF_MAP // 2],
    [CHUNKS_IN_WIDTH_OF_MAP // 6 * 5, CHUNKS_IN_HEIGHT_OF_MAP // 2],
    [CHUNKS_IN_WIDTH_OF_MAP // 4, CHUNKS_IN_HEIGHT_OF_MAP // 4],
    [CHUNKS_IN_WIDTH_OF_MAP // 4 * 3, CHUNKS_IN_HEIGHT_OF_MAP // 4],
    [CHUNKS_IN_WIDTH_OF_MAP // 4, CHUNKS_IN_HEIGHT_OF_MAP // 4 * 3],
    [CHUNKS_IN_WIDTH_OF_MAP // 4 * 3, CHUNKS_IN_HEIGHT_OF_MAP // 4 * 3]
]"""
orb_positions = [
    [CHUNKS_IN_WIDTH_OF_MAP // 2, CHUNKS_IN_HEIGHT_OF_MAP // 8],
    [CHUNKS_IN_WIDTH_OF_MAP // 2, CHUNKS_IN_HEIGHT_OF_MAP // 8 * 7],
    [CHUNKS_IN_WIDTH_OF_MAP // 8, CHUNKS_IN_HEIGHT_OF_MAP // 2],
    [CHUNKS_IN_WIDTH_OF_MAP // 8 * 7, CHUNKS_IN_HEIGHT_OF_MAP // 2]
]
for _ in range(0, NUMBER_OF_ORBS):

    #x, y = random.randint(0, CHUNKS_IN_MAP[0] - 1), random.randint(0, CHUNKS_IN_MAP[1] - 1)
    x, y = orb_positions.pop(0)
    for i in range(ENTITIES_PER_CHUNK):
        if save_data["map_chunk_entities"][x, y, i, 2] == 0:
            break
    else:
        continue

    #entity = random.randint(0, CHUNK_SIZE[0] - 1), random.randint(0, CHUNK_SIZE[1] - 1), random.randint(2, 7)
    #entity = CHUNK_SIZE_WIDTH_DIV_2, CHUNK_SIZE_HEIGHT_DIV_2, random.randint(2, 7)
    if orbs_yet_to_place:
        # orb_being_placed = random.choice(orbs_yet_to_place)
        orb_being_placed = orbs_yet_to_place[0]
        orbs_yet_to_place.remove(orb_being_placed)
    else:
        orb_being_placed = random.choice(("humid_orb", "frozen_orb", "dry_orb", "desert_orb"))  # KEY_ENTITIES[random.randint(2, 7)]
    entity = CHUNK_SIZE_WIDTH_DIV_2, CHUNK_SIZE_HEIGHT_DIV_2, KEY_ENTITIES.index(orb_being_placed)
    save_data["map_chunk_entities"][x, y, i] = numpy.array(entity, dtype=numpy.int)
    ORBS_DETAILS.append(f"{KEY_ENTITIES[entity[2]]}: [{x}, {y}]")
    #print(x, y, entity)

#save_data["map"][50, 50] = 1
#save_data["map_chunk_entities"][6, 6, 0] = [0, 0, 1]
#save_data["map_chunk_properties"]["temperature"][5][5] = 330
