import time
import random
import turtle
import colorsys
from decorator import log_action
import possible_module
from exceptions import InactivityException, SnakeTooLongException, BoarderCollision

class Snake:
    """
    Класс для представления змейки
    """
    def __init__(self, head_color, controls, start_pos, snake_name):

        if not isinstance(head_color, str):
            raise TypeError("head_color must be a string")

        if not isinstance(controls, dict):
            raise TypeError("controls must be a dictionary")

        if not isinstance(start_pos, tuple) or len(start_pos) != 2:
            raise TypeError("start_pos must be a tuple of length 2")

        if not isinstance(snake_name, str):
            raise TypeError("snake_name must be a string")

        self.head = turtle.Turtle()
        self.head.shape("circle")
        self.head.color(head_color)
        self.head.penup()
        self.head.goto(*start_pos)
        self.head.direction = "Stop"

        self.body = []
        self.score = 0
        self.high_score = 0
        self.speed = 0.3
        self.controls = controls
        self.snake_name = snake_name
        self.position = start_pos

        self.scoreboard = possible_module.Scoreboard(self.snake_name, self.position)

    def move(self):
        """
        Прописали передвижение змейки в зависимости от текущего направления
        """
        if self.head.direction == "up":
            self.head.sety(self.head.ycor() + 20)
        elif self.head.direction == "down":
            self.head.sety(self.head.ycor() - 20)
        elif self.head.direction == "left":
            self.head.setx(self.head.xcor() - 20)
        elif self.head.direction == "right":
            self.head.setx(self.head.xcor() + 20)

    @log_action("Добавление сегмента тела")
    def add_body_segment(self, color):
        """
        Обеспечиваем добавление нового сегмента тела змейки
        """
        new_segment = turtle.Turtle()
        new_segment.shape("circle")
        new_segment.color(color)
        new_segment.penup()
        self.body.append(new_segment)

    def follow_head(self):
        """
        Обеспечиваем следование частей тела змейки за головой
        """
        for index in range(len(self.body) - 1, 0, -1):
            x = self.body[index - 1].xcor()
            y = self.body[index - 1].ycor()
            self.body[index].goto(x, y)
        if self.body:
            x = self.head.xcor()
            y = self.head.ycor()
            self.body[0].goto(x, y)

class Game:
    def __init__(self):
        self.screen = turtle.Screen()
        self.screen.bgcolor("black")
        self.screen.setup(width = 666, height = 666)
        self.screen.tracer(0)

        self.width = 666
        self.height = 666
        self.sleep = 0.3

        self.snake1 = Snake("blue", {"up": "w", "down": "s", "left": "a", "right": "d"}, (0, 100), "Snake 1")
        self.snake2 = Snake("purple", {"up": "Up", "down": "Down", "left": "Left", "right": "Right"}, (0, -100), "Snake 2")

        self.food = turtle.Turtle()
        self.food.shape("square")
        self.food.color("yellow")
        self.food.penup()
        self.food.goto(random.randint(-300, 300), random.randint(-300, 300))

        self.last_move_time = {"snake1": time.time(), "snake2": time.time()}

    def relocate_food(self):
        """
        Помещаем еды в случайное место
        """
        self.food.goto(random.randint(-self.width // 2 + 30, self.width // 2 - 30), random.randint(-self.height // 2 + 30, self.height // 2 - 30))

    def set_direction(self, snake, direction, snake_name):
        """
        Устанавливаем направления змейки
        """
        opposite = {"up": "down", "down": "up", "left": "right", "right": "left"}
        if snake.head.direction != opposite[direction]:
            snake.head.direction = direction
            self.last_move_time[snake_name] = time.time()

    def check_food_collision(self, snake):
        """
        Проверяем на столкновение змейки с едой
        """
        if snake.head.distance(self.food) < 17:
            new_color = colorsys.hsv_to_rgb(random.random(), 1, 0.5)
            snake.add_body_segment(new_color)

            if len(snake.body) % 2 == 1: # Уменьшаем поле слева/справа
                self.width -= 20
            else:
                self.height -= 20 # Уменьшаем поле сверху/снизу

            self.screen.setup(self.width, self.height) # Обновляем значения размеров доступного экрана
            self.relocate_food()

            for segment in snake.body:
                segment.color(new_color)

            snake.scoreboard.update_score()

    def check_snake_collision(self, snake1, snake2):
        """
        Проверка столкновения змей
        """
        for segment in snake2.body:
            if segment != snake2.head and snake1.head.distance(segment) < 15:
                return True
        return False

    def check_snake_size(self, snake):
        """
        Проверяем на возможность заполнения змейкой всего поля
        """
        if len(snake.body) + 1 >= (self.width * self.height) // (20 * 20):
            raise SnakeTooLongException("Змейка заполнила всё игровое поле.")

    def check_collision(self, snake):
        """
        Проверяем столкновение головы змейки с границей
        """
        if (snake.head.xcor() > self.width // 2 - 15 or snake.head.xcor() < -self.width // 2 + 15 or
            snake.head.ycor() > self.height // 2 - 15 or snake.head.ycor() < -self.height // 2 + 15):
            raise BoarderCollision("Змейка врезалась в границу поля!")

    def check_inactivity(self, snake_name):
        """
        Проверяем, бездействует ли один из игроков
        """
        if time.time() - self.last_move_time[snake_name] > 10:
            raise InactivityException("Игрок бездействовал слишком долго.")

    def play(self):
        self.screen.listen()

        self.screen.onkeypress(lambda: self.set_direction(self.snake1, "up", "snake1"), "w") # Блок, отвечающий за связку клавиш и направлений движения змейки 1
        self.screen.onkeypress(lambda: self.set_direction(self.snake1, "down", "snake1"), "s")
        self.screen.onkeypress(lambda: self.set_direction(self.snake1, "left", "snake1"), "a")
        self.screen.onkeypress(lambda: self.set_direction(self.snake1, "right", "snake1"), "d")

        self.screen.onkeypress(lambda: self.set_direction(self.snake2, "up", "snake2"), "Up") # Блок, отвечающий за связку клавиш и направлений движения змейки 2
        self.screen.onkeypress(lambda: self.set_direction(self.snake2, "down", "snake2"), "Down")
        self.screen.onkeypress(lambda: self.set_direction(self.snake2, "left", "snake2"), "Left")
        self.screen.onkeypress(lambda: self.set_direction(self.snake2, "right", "snake2"), "Right")

        while True:
            self.screen.update()

            self.snake1.move()
            self.snake2.move()

            self.snake1.follow_head()
            self.snake2.follow_head()

            self.check_food_collision(self.snake1)
            self.check_food_collision(self.snake2)

            self.check_collision(self.snake1)
            self.check_collision(self.snake2)

            self.check_inactivity("snake1")
            self.check_inactivity("snake2")

            if self.check_snake_collision(self.snake1, self.snake2) or self.check_snake_collision(self.snake2, self.snake1):
                break

            time.sleep(self.sleep)

if __name__ == "__main__":
    game = Game()
    game.play()
