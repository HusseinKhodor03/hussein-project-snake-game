import pygame
import random
from enum import Enum
from collections import namedtuple

pygame.font.init()

SCORE_FONT = pygame.font.SysFont("arial", 25)

WHITE = (255, 255, 255)
RED = (200, 0, 0)
BLUE_1 = (0, 0, 255)
BLUE_2 = (0, 100, 255)
BLACK = (0, 0, 0)

BLOCK_SIZE = 20
FPS = 15


class Direction(Enum):
    INITIAL = 0
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4


Point = namedtuple("Point", "x, y")


class SnakeGame:
    def __init__(self, width=640, height=480):
        self.width = width
        self.height = height
        self.window = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()
        self.direction = Direction.INITIAL

        self.head = Point(self.width / 2, self.height / 2)
        self.snake = [
            self.head,
            Point(self.head.x - BLOCK_SIZE, self.head.y),
            Point(self.head.x - (2 * BLOCK_SIZE), self.head.y),
        ]

        self.score = 0
        self.food = None
        self._place_food()

        pygame.display.set_caption("Snake Game")

    def _place_food(self):
        x = (
            random.randint(0, (self.width - BLOCK_SIZE) // BLOCK_SIZE)
            * BLOCK_SIZE
        )
        y = (
            random.randint(0, (self.height - BLOCK_SIZE) // BLOCK_SIZE)
            * BLOCK_SIZE
        )
        self.food = Point(x, y)

        if self.food in self.snake:
            self._place_food()

    def _update_ui(self):
        self.window.fill(BLACK)

        for point in self.snake:
            pygame.draw.rect(
                self.window,
                BLUE_1,
                pygame.Rect(point.x, point.y, BLOCK_SIZE, BLOCK_SIZE),
            )
            pygame.draw.rect(
                self.window,
                BLUE_2,
                pygame.Rect(point.x + 4, point.y + 4, 12, 12),
            )

        pygame.draw.rect(
            self.window,
            RED,
            pygame.Rect(self.food.x, self.food.y, BLOCK_SIZE, BLOCK_SIZE),
        )

        score_text = SCORE_FONT.render(f"Score: {self.score}", True, WHITE)
        self.window.blit(score_text, (0, 0))

        pygame.display.update()

    def _move(self, direction):
        x = self.head.x
        y = self.head.y

        if direction == Direction.RIGHT:
            x += BLOCK_SIZE
        elif direction == Direction.LEFT:
            x -= BLOCK_SIZE
        elif direction == Direction.DOWN:
            y += BLOCK_SIZE
        elif direction == Direction.UP:
            y -= BLOCK_SIZE

        self.head = Point(x, y)

    def _is_collision(self):
        if (
            self.head.x > self.width - BLOCK_SIZE
            or self.head.x < 0
            or self.head.y > self.height - BLOCK_SIZE
            or self.head.y < 0
        ):
            return True

        if self.head in self.snake[1:]:
            return True

        return False

    def play_step(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if (
                    event.key == pygame.K_LEFT
                    and self.direction != Direction.RIGHT
                ):
                    if self.direction != Direction.INITIAL:
                        self.direction = Direction.LEFT
                elif (
                    event.key == pygame.K_RIGHT
                    and self.direction != Direction.LEFT
                ):
                    self.direction = Direction.RIGHT
                elif (
                    event.key == pygame.K_UP
                    and self.direction != Direction.DOWN
                ):
                    self.direction = Direction.UP
                elif (
                    event.key == pygame.K_DOWN
                    and self.direction != Direction.UP
                ):
                    self.direction = Direction.DOWN

        if self.direction != Direction.INITIAL:
            self._move(self.direction)
            self.snake.insert(0, self.head)

        game_over = False

        if self._is_collision():
            game_over = True
            return game_over, self.score

        if self.head == self.food:
            self.score += 1
            self._place_food()
        else:
            if len(self.snake) > 3:
                self.snake.pop()

        self._update_ui()
        self.clock.tick(FPS)

        return game_over, self.score


if __name__ == "__main__":
    game = SnakeGame()

    while True:
        game_over, score = game.play_step()

        if game_over == True:
            break
