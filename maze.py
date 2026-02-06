import sys

import pygame

from levels import LEVELS

TILE_SIZE = 32
FPS = 60

COLORS = {
    "wall": (30, 30, 30),
    "floor": (240, 240, 240),
    "player": (50, 120, 220),
    "start": (120, 200, 120),
    "exit": (220, 120, 120),
    "text": (20, 20, 20),
}


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Maze Adventure")
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        self.level_index = 0
        self.level = []
        self.player_pos = [0, 0]
        self.screen = None
        self.clock = pygame.time.Clock()
        self.load_level(self.level_index)

    def load_level(self, index: int) -> None:
        self.level = LEVELS[index]
        width = len(self.level[0])
        height = len(self.level)
        window_size = (width * TILE_SIZE, height * TILE_SIZE)
        if self.screen is None:
            self.screen = pygame.display.set_mode(window_size)
        else:
            self.screen = pygame.display.set_mode(window_size)
        self.player_pos = self.find_tile("S")

    def find_tile(self, tile: str) -> list[int]:
        for y, row in enumerate(self.level):
            for x, cell in enumerate(row):
                if cell == tile:
                    return [x, y]
        raise ValueError(f"Tile {tile!r} not found in level")

    def is_wall(self, x: int, y: int) -> bool:
        return self.level[y][x] == "#"

    def move_player(self, dx: int, dy: int) -> None:
        new_x = self.player_pos[0] + dx
        new_y = self.player_pos[1] + dy
        if self.is_wall(new_x, new_y):
            return
        self.player_pos = [new_x, new_y]
        if self.level[new_y][new_x] == "E":
            self.advance_level()

    def advance_level(self) -> None:
        self.level_index += 1
        if self.level_index >= len(LEVELS):
            self.show_completion()
            pygame.quit()
            sys.exit()
        self.load_level(self.level_index)

    def show_completion(self) -> None:
        self.screen.fill(COLORS["floor"])
        title = self.font.render("Поздравляю!", True, COLORS["text"])
        subtitle = self.small_font.render(
            "Ты прошел все уровни лабиринта!", True, COLORS["text"]
        )
        self.screen.blit(title, title.get_rect(center=(self.screen.get_width() // 2, 120)))
        self.screen.blit(
            subtitle,
            subtitle.get_rect(center=(self.screen.get_width() // 2, 180)),
        )
        pygame.display.flip()
        pygame.time.wait(2500)

    def handle_input(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_w, pygame.K_UP):
                    self.move_player(0, -1)
                if event.key in (pygame.K_s, pygame.K_DOWN):
                    self.move_player(0, 1)
                if event.key in (pygame.K_a, pygame.K_LEFT):
                    self.move_player(-1, 0)
                if event.key in (pygame.K_d, pygame.K_RIGHT):
                    self.move_player(1, 0)

    def draw(self) -> None:
        self.screen.fill(COLORS["floor"])
        for y, row in enumerate(self.level):
            for x, cell in enumerate(row):
                rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                if cell == "#":
                    pygame.draw.rect(self.screen, COLORS["wall"], rect)
                elif cell == "S":
                    pygame.draw.rect(self.screen, COLORS["start"], rect)
                elif cell == "E":
                    pygame.draw.rect(self.screen, COLORS["exit"], rect)
        player_rect = pygame.Rect(
            self.player_pos[0] * TILE_SIZE + 4,
            self.player_pos[1] * TILE_SIZE + 4,
            TILE_SIZE - 8,
            TILE_SIZE - 8,
        )
        pygame.draw.rect(self.screen, COLORS["player"], player_rect)
        level_text = self.small_font.render(
            f"Уровень {self.level_index + 1} из {len(LEVELS)}", True, COLORS["text"]
        )
        self.screen.blit(level_text, (10, 10))
        pygame.display.flip()

    def run(self) -> None:
        while True:
            self.handle_input()
            self.draw()
            self.clock.tick(FPS)


def main() -> None:
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
