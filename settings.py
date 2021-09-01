import pygame

from level import level_map, player_index

WALL = "#"
PLAYER = "P"
CARGO = "X"
TARGET = "T"
FLOOR = "."
CARGO_TARGET = "S"

SCALE = 50

ROWS = len(level_map)  # level_map.count("\n") + 1
COLS = len(level_map[0])  # len(level_map.split("\n")[0])

SQ_W = SCALE
SQ_H = SCALE

WIDTH, HEIGHT = COLS * SCALE, ROWS * SCALE

wall_img = pygame.transform.scale(pygame.image.load("img/wall.png"), (SQ_W, SQ_H))
cargo_img = pygame.transform.scale(pygame.image.load("img/cargo.png"), (SQ_W, SQ_H))
cargo_on_target_img = pygame.transform.scale(
    pygame.image.load("img/cargo_on_target.png"), (SQ_W, SQ_H)
)
floor_img = pygame.transform.scale(pygame.image.load("img/floor.png"), (SQ_W, SQ_H))
target_img = pygame.transform.scale(pygame.image.load("img/target.png"), (SQ_W, SQ_H))
player_img = pygame.transform.scale(pygame.image.load("img/player.png"), (SQ_W, SQ_H))
player_on_target_img = pygame.transform.scale(
    pygame.image.load("img/player_on_target.png"), (SQ_W, SQ_H)
)
