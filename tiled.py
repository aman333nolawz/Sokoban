import pickle

import pygame
import pygame.display
import pygame.font
import pygame.mouse

from settings import (
    CARGO,
    CARGO_TARGET,
    COLS,
    FLOOR,
    HEIGHT,
    PLAYER,
    ROWS,
    SQ_H,
    SQ_W,
    TARGET,
    WALL,
    WIDTH,
    cargo_img,
    cargo_on_target_img,
    floor_img,
    player_img,
    target_img,
    wall_img,
)

pygame.init()


win = pygame.display.set_mode((WIDTH + 300, HEIGHT))
screen = pygame.Surface((WIDTH, HEIGHT))
font = pygame.font.SysFont("Arial", 20)

current_tile = CARGO

tile_types = {
    "Cargo": [1, CARGO],
    "Cargo on target": [2, CARGO_TARGET],
    "Target": [3, TARGET],
    "Wall": [4, WALL],
    "Floor": [5, FLOOR],
    "Player": [6, PLAYER],
}

grid = [[FLOOR for _ in range(COLS)] for _ in range(ROWS)]
player_index = (0, 0)
prev_tile = None
level = 1

while True:
    win.fill("#282A36")
    screen.fill("#282A36")
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                current_tile = CARGO
            elif event.key == pygame.K_2:
                current_tile = CARGO_TARGET
            elif event.key == pygame.K_3:
                current_tile = TARGET
            elif event.key == pygame.K_4:
                current_tile = WALL
            elif event.key == pygame.K_5:
                current_tile = FLOOR
            elif event.key == pygame.K_6:
                prev_tile = current_tile
                current_tile = PLAYER
            elif event.key == pygame.K_s:
                with open(f"levels/level-{level}.pkl", "wb") as f:
                    pickle.dump([grid, player_index], f)
            elif event.key == pygame.K_l:
                with open(f"levels/level-{level}.pkl", "rb") as f:
                    grid, player_index = pickle.load(f)
            elif pygame.key.get_mods() & pygame.KMOD_SHIFT:
                if event.key == pygame.K_UP:
                    level += 1
                elif event.key == pygame.K_DOWN:
                    level = max(1, level - 1)

    for i, tile_type in enumerate(tile_types):
        if tile_types[tile_type][1] == current_tile:
            text = font.render(
                f"*{tile_type} = {tile_types[tile_type][0]}", 1, "#E3E4E0"
            )
        else:
            text = font.render(
                f"{tile_type} = {tile_types[tile_type][0]}", 1, "#E3E4E0"
            )
        win.blit(text, (WIDTH + 50, i * 30 + HEIGHT // 4))

    text = font.render(f"level = {level}", 1, "#E3E4E0")
    win.blit(text, (WIDTH + 50, 10))

    if pygame.mouse.get_pressed()[0]:
        x, y = pygame.mouse.get_pos()
        x, y = x // SQ_W, y // SQ_H
        if 0 <= x < COLS and 0 <= y < ROWS:
            if current_tile == PLAYER:
                if grid[y][x] in [FLOOR, TARGET]:
                    player_index = (x, y)
                else:
                    print(prev_tile)
                    grid[y][x] = prev_tile
            else:
                grid[y][x] = current_tile
    elif pygame.mouse.get_pressed()[2]:
        x, y = pygame.mouse.get_pos()
        x, y = x // SQ_W, y // SQ_H
        if 0 <= x < COLS and 0 <= y < ROWS:
            grid[y][x] = FLOOR

    for i, row in enumerate(grid):
        for j, tile in enumerate(row):
            if tile == CARGO:
                screen.blit(cargo_img, (j * SQ_W, i * SQ_H, SQ_W, SQ_H))
            elif tile == CARGO_TARGET:
                screen.blit(cargo_on_target_img, (j * SQ_W, i * SQ_H, SQ_W, SQ_H))
            elif tile == TARGET:
                screen.blit(target_img, (j * SQ_W, i * SQ_H, SQ_W, SQ_H))
            elif tile == WALL:
                screen.blit(wall_img, (j * SQ_W, i * SQ_H, SQ_W, SQ_H))
            else:
                screen.blit(floor_img, (j * SQ_W, i * SQ_H, SQ_W, SQ_H))

    screen.blit(player_img, (player_index[0] * SQ_W, player_index[1] * SQ_H))

    for i in range(COLS):
        pygame.draw.line(screen, "#000000", (i * SQ_W, 0), (i * SQ_W, HEIGHT))
    for i in range(ROWS):
        pygame.draw.line(screen, "#000000", (0, i * SQ_H), (WIDTH, i * SQ_H))

    win.blit(screen, (0, 0))

    pygame.display.flip()
