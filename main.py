import pickle

import pygame
import pygame.display
import pygame.draw
import pygame.event
import pygame.font
import pygame.image
import pygame.key
import pygame.time
import pygame.transform

from settings import (
    CARGO,
    CARGO_TARGET,
    COLS,
    FLOOR,
    HEIGHT,
    ROWS,
    SQ_H,
    SQ_W,
    TARGET,
    WALL,
    WIDTH,
    cargo_img,
    cargo_on_target_img,
    floor_img,
    level_map,
    player_img,
    player_index,
    player_on_target_img,
    target_img,
    wall_img,
)

pygame.init()
pygame.font.init()


class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self, win, level_map):
        if level_map[self.y][self.x] == TARGET:
            win.blit(player_on_target_img, (self.x * SQ_W, self.y * SQ_H))
        else:
            win.blit(player_img, (self.x * SQ_W, self.y * SQ_H))


class Cargo:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self, win, level_map):
        if level_map[self.y][self.x] in [TARGET, CARGO_TARGET]:
            win.blit(cargo_on_target_img, (self.x * SQ_W, self.y * SQ_H))
        else:
            win.blit(cargo_img, (self.x * SQ_W, self.y * SQ_H))


class Level:
    def __init__(self, level=1):
        self.level = level
        with open(f"levels/level-{level}.pkl", "rb") as f:
            self.map, player_pos = pickle.load(f)
        self.player = Player(*player_pos)
        self.cargos = []
        for i, row in enumerate(self.map):
            for j, cell in enumerate(row):
                if cell in (CARGO, CARGO_TARGET):
                    self.cargos.append(Cargo(j, i))

    def draw(self, win):
        for i, row in enumerate(self.map):
            for j, cell in enumerate(row):
                if cell == WALL:
                    win.blit(wall_img, (j * SQ_W, i * SQ_H))
                elif cell in (TARGET, CARGO_TARGET):
                    win.blit(target_img, (j * SQ_W, i * SQ_H))
                elif cell == FLOOR:
                    win.blit(floor_img, (j * SQ_W, i * SQ_H))

        for cargo in self.cargos:
            cargo.draw(win, self.map)
        self.player.draw(win, self.map)

    def move_player(self, key):
        try:
            up = self.map[self.player.y - 1][self.player.x]
        except IndexError:
            up = self.map[self.player.y][self.player.x]

        try:
            down = self.map[self.player.y + 1][self.player.x]
        except IndexError:
            down = self.map[self.player.y][self.player.x]

        try:
            left = self.map[self.player.y][self.player.x - 1]
        except IndexError:
            left = self.map[self.player.y][self.player.x]

        try:
            right = self.map[self.player.y][self.player.x + 1]
        except IndexError:
            right = self.map[self.player.y][self.player.x]

        cargo_vec = [0, 0]
        player_old_pos = (self.player.x, self.player.y)

        if key == pygame.K_UP and up != WALL:
            self.player.y -= 1
            cargo_vec[1] -= 1
        elif key == pygame.K_DOWN and down != WALL:
            self.player.y += 1
            cargo_vec[1] += 1
        elif key == pygame.K_LEFT and left != WALL:
            self.player.x -= 1
            cargo_vec[0] -= 1
        elif key == pygame.K_RIGHT and right != WALL:
            self.player.x += 1
            cargo_vec[0] += 1

        cargo_pos = [(cargo.x, cargo.y) for cargo in self.cargos]
        for i, cargo in enumerate(self.cargos):
            if cargo.x == self.player.x and cargo.y == self.player.y:
                # Horizontal Movement of cargo
                if (
                    cargo_vec[1] == 0
                    and 0 <= cargo.x + cargo_vec[0] < COLS
                    and (cargo.x + cargo_vec[0], cargo.y) not in cargo_pos
                    and self.map[cargo.y][cargo.x + cargo_vec[0]] != WALL
                ):
                    cargo.x += cargo_vec[0]

                # Vertical Movement of cargo
                elif (
                    cargo_vec[0] == 0
                    and 0 <= cargo.y + cargo_vec[1] < ROWS
                    and (cargo.x, cargo.y + cargo_vec[1]) not in cargo_pos
                    and self.map[cargo.y + cargo_vec[1]][cargo.x] != WALL
                ):
                    cargo.y += cargo_vec[1]
                # There is something blocking the cargo
                else:
                    self.player.x = player_old_pos[0]
                    self.player.y = player_old_pos[1]

        if self.check_win():
            self.__init__(self.level + 1)

    def check_win(self):
        for cargo in self.cargos:
            if self.map[cargo.y][cargo.x] not in [TARGET, CARGO_TARGET]:
                return False
        return True


def level_from_string(map_str: str):
    map_ = []
    map_str: str = map_str.strip()
    for line in map_str.splitlines():
        map_.append([char for char in line])

    return Level(map_, _1d_to_2d(20))


level = Level()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

while True:
    clock.tick(60)
    screen.fill("#ded6ad")

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.KEYDOWN:
            if 1073741903 <= event.key <= 1073741906:
                level.move_player(event.key)
            elif event.key == pygame.K_SPACE:
                level = Level(level.level)

    level.draw(screen)

    pygame.display.flip()
