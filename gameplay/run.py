import time
import random
import turtle
import colorsys
from decorator import log_action
import possible_module

class Snake:
    """
    Класс для представления змейки
    """
    def __init__(self, head_color, controls, start_pos, snake_name):
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
        Передвижение змейки в зависимости от текущего направления
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
        Добавление нового сегмента тела змейки
        """
        new_segment = turtle.Turtle()
        new_segment.shape("circle")
        new_segment.color(color)
        new_segment.penup()
        self.body.append(new_segment)

    def follow_head(self):
        """
        Обеспечивает следования частей тела змейки за головой
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
        self.screen.title("Snake Game Multiplayer")
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

    def relocate_food(self):
        """
        Перемещение еды
        """
        self.food.goto(random.randint(-self.width // 2 + 30, self.width // 2 - 30), random.randint(-self.height // 2 + 30, self.height // 2 - 30))

    def check_food_collision(self, snake):
        """
        Проверка на столкновение змейки с едой
        """
        if (snake.head.distance(self.food) < 17):
            new_color = colorsys.hsv_to_rgb(random.random(), 1, 0.7)
            snake.add_body_segment(new_color)

            for segment in snake.body:
                segment.color(new_color)
            if (len(snake.body) % 2 == 1):
                self.width -= 20
            else:
                self.height -= 20

            self.screen.setup(self.width, self.height)
            self.relocate_food()
            snake.scoreboard.update_score()

    def check_collision(self, snake):
        """
        Проверка столкновений головы змейки с границами поля
        """
        if (snake.head.xcor() > self.width // 2 - 15 or snake.head.xcor() < -self.width // 2 + 15 or
                snake.head.ycor() > self.height // 2 - 15 or snake.head.ycor() < -self.height // 2 + 15):
            # print(f"Игра окончена! Змейка {snake.head.color()[0]} врезалась в границу.")
            snake.scoreboard.game_over()
            self.screen.bye()

    def set_direction(self, snake, direction):
        """
        Установка направления змейки
        """
        opposite = {"up": "down", "down": "up", "left": "right", "right": "left"}
        if (snake.head.direction != opposite[direction]):
            snake.head.direction = direction

    def check_snake_collision(self, snake1, snake2):
        """
        Проверка столкновения змей
        """
        for segment in snake2.body:
            if (segment != snake2.head and snake1.head.distance(segment) < 15):
                snake1.scoreboard.game_over()
                snake2.scoreboard.game_over()
                self.screen.bye()
                return True
        return False

    def play(self):
        self.screen.listen()

        # Управление для змейки 1
        self.screen.onkeypress(lambda: self.set_direction(self.snake1, "up"), "w")
        self.screen.onkeypress(lambda: self.set_direction(self.snake1, "down"), "s")
        self.screen.onkeypress(lambda: self.set_direction(self.snake1, "left"), "a")
        self.screen.onkeypress(lambda: self.set_direction(self.snake1, "right"), "d")

        # Управление для змейки 2
        self.screen.onkeypress(lambda: self.set_direction(self.snake2, "up"), "Up")
        self.screen.onkeypress(lambda: self.set_direction(self.snake2, "down"), "Down")
        self.screen.onkeypress(lambda: self.set_direction(self.snake2, "left"), "Left")
        self.screen.onkeypress(lambda: self.set_direction(self.snake2, "right"), "Right")

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

            if self.check_snake_collision(self.snake1, self.snake2) or self.check_snake_collision(self.snake2, self.snake1):
                break

            time.sleep(self.sleep)

if __name__ == "__main__":
    game = Game()
    game.play()
