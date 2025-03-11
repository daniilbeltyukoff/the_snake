from random import randint

import pygame as pg

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Инициализация шрифта:
pg.font.init()
font = pg.font.Font(None, 36)

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pg.display.set_caption('Змейка')

# Настройка времени:
clock = pg.time.Clock()

# Константы для центра экрана:
CENTER_X = SCREEN_WIDTH // 2
CENTER_Y = SCREEN_HEIGHT // 2


# Тут опишите все классы игры.
class GameObject:
    """Базовый класс для объекта игры."""

    def __init__(self) -> None:
        """Инициализация объекта игры."""
        self.position = [(CENTER_X, CENTER_Y)]
        self. body_color = None

    @staticmethod
    def draw_rect(position, color):
        """Отрисовка объекта на экране."""
        rect = pg.Rect(position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, color, rect)

    def draw(self):
        """Метод предназначен для переопределения в дочерних классах"""


class Apple(GameObject):
    """Класс для яблока, которое будет есть змейка."""

    def __init__(self):
        """Инициализация яблока"""
        super().__init__()
        self.body_color = APPLE_COLOR
        self.position = self.randomize_position([])

    def randomize_position(self, snake_positions):
        """Устанавливает случайную позицию яблока на игровом поле."""
        while True:
            self.position = (
                randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            )
            if self.position not in snake_positions:
                return self.position

    def draw(self):
        """Отрисовка яблока для экрана."""
        GameObject.draw_rect(
            self.position, APPLE_COLOR
        )


class Snake(GameObject):
    """Класс для змейки, которая перемещается на игровом поле."""

    def __init__(self):
        """Инициализация змейки, которая перемащается по игровому полю"""
        super().__init__()
        self.reset()

    def update_direction(self):
        """Обновляет направление змейки"""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Перемещает змейку в заданном направлении.
        При выходе змейки за пределы поля,
        она появится с противоположной стороны.
        Также происходит проверка на столкновение змейки с собой.
        """
        head_x, head_y = self.get_head_position()
        dir_x, dir_y = self.direction
        new_head = (head_x + dir_x * GRID_SIZE, head_y + dir_y * GRID_SIZE)
        new_head = (
            new_head[0] % SCREEN_WIDTH,
            new_head[1] % SCREEN_HEIGHT
        )

        self.positions.insert(0, new_head)
        self.last = self.positions[-1]

        if len(self.positions) > self.length:
            self.positions.pop()

    def draw(self):
        """Отрисовывает змейку на экране, затирая след."""
        for position in self.positions[:]:
            GameObject.draw_rect(position, self.body_color)

        head_rect = self.get_head_position()
        GameObject.draw_rect(head_rect, self.body_color)

        if self.last:
            last_rect = self.last
            GameObject.draw_rect(last_rect, BOARD_BACKGROUND_COLOR)

    def get_head_position(self):
        """Возвращает позицию головы змейки."""
        return self.positions[0]

    def reset(self):
        """Сбрасывает змейку в начальное положение."""
        self.length = 1
        self.positions = [(CENTER_X, CENTER_Y)]
        self.direction = RIGHT
        self.next_direction = None
        self.body_color = SNAKE_COLOR
        self.last = None


def handle_keys(game_object):
    """Обрабатывает нажатия клавиш,
    чтобы изменить направление движения змейки.
    """
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                pg.quit()
                exit
            elif event.key == pg.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pg.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pg.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pg.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def draw_text(text, x, y, font):
    """Отрисока текста на экране."""
    text_surface = font.render(text, True, (255, 255, 255))
    screen.blit(text_surface, (x, y))


def main():
    """Запуск основного цикла игры."""
    pg.init()
    pg.font.init()
    font = pg.font.Font(None, 36)

    apple = Apple()
    snake = Snake()
    running = True
    score = 0

    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.move()

        if snake.get_head_position() == apple.position:
            snake.length += 1
            score += 1
            apple.randomize_position(snake.positions)

        elif snake.get_head_position() in snake.positions[4:]:
            snake.reset()
            score = 0

        screen.fill(BOARD_BACKGROUND_COLOR)
        apple.draw()
        snake.draw()
        draw_text('Score: {}'.format(score), 10, 10, font)
        draw_text('Press ESC to exit', 10, 50, font)
        pg.display.update()


if __name__ == '__main__':
    main()
