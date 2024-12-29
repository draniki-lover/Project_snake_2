import turtle
import time

class Scoreboard:
    def __init__(self, snake_name, position):
        self.score = 0
        self.snake_name = snake_name
        self.position = position
        self.pen = turtle.Turtle()
        self.pen.speed(0)
        self.pen.shape("square")
        self.pen.color("white")
        self.pen.penup()
        self.pen.hideturtle()
        self.pen.goto(self.position[0] - 100, self.position[1] + 100)
        self.pen.write(f"{self.snake_name}: {self.score}", align="center", font=("Arial", 15, "normal"))

    def update_score(self):
        """
        Обновляет счет во время игры
        """
        self.score += 10
        self.pen.clear()
        self.pen.write(f"{self.snake_name}: {self.score}", align="center", font=("Arial", 15, "normal"))

    def game_over(self):
        """
        Выводит сообщение о завершении игры
        """
        self.pen.goto(0, 0)
        self.pen.clear()
        self.pen.pendown()
        self.pen.write(f"Game Over! {self.snake_name}  Score: {self.score}", align="center", font=("Arial", 24, "normal"))
        time.sleep(2)