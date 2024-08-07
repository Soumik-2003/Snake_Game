import time
from turtle import *
import random


screen = Screen()
screen.setup(width=700, height=500)
screen.title('Snake Game')
screen.bgcolor('black')
screen.tracer(0)


class Snake:
    def __init__(self):
        self.side = None
        self.X = None
        self.Y = None
        self.list1 = []
        self.pos = 0
        self.snake_body()
        self.head = self.list1[0]

    def snake_body(self):
        for go in range(3):
            pet = Turtle('square')
            pet.up()
            pet.shapesize(stretch_wid=0.50, stretch_len=0.50)
            pet.color('white')
            pet.goto(self.pos, 0)
            self.list1.append(pet)
            self.pos -= 15

    def reset(self):
        for block in self.list1:
            block.hideturtle()
        self.list1.clear()
        self.snake_body()
        self.head = self.list1[0]

    def add_body(self):
        pet = Turtle('square')
        pet.up()
        pet.shapesize(stretch_wid=0.50, stretch_len=0.50)
        pet.color('white')
        pet.goto(self.list1[-1].position())
        self.list1.append(pet)

    def move(self):
        for sett in range(len(self.list1) - 1, 0, -1):
            self.X = self.list1[sett - 1].xcor()
            self.Y = self.list1[sett - 1].ycor()
            self.list1[sett].goto(self.X, self.Y)
        self.list1[0].forward(15)

    def up(self):
        if self.head.heading() != 270:
            self.head.setheading(90)

    def down(self):
        if self.head.heading() != 90:
            self.head.setheading(270)

    def left(self):
        if self.head.heading() != 0:
            self.head.setheading(180)

    def right(self):
        if self.head.heading() != 180:
            self.head.setheading(0)

    def wall(self):
        x = self.head.xcor()
        y = self.head.ycor()

        if self.head.distance(350, y) < 10:
            self.head.goto(-340, y)

        elif self.head.distance(-350, y) < 10:
            self.head.goto(340, y)

        elif self.head.distance(x, 250) < 10:
            self.head.goto(x, -240)

        elif self.head.distance(x, -250) < 10:
            self.head.goto(x, 240)


Alignment = "center"
Font = ("calibre", 13, "normal")


class Score(Turtle):
    score = 0

    def __init__(self):
        super().__init__()
        self.pencolor('white')
        with open('data.txt', mode='r') as High_Score:
            self.highscore = int(High_Score.read())
        self.hideturtle()
        self.up()
        self.goto(x=-10, y=230)
        self.down()
        self.write(f"Score = {self.score}, High Score = {self.highscore}", False, Alignment, Font)

    def high_score(self):
        if self.score > self.highscore:
            with open('data.txt', mode='w') as self.highscore2:
                self.highscore2.write(str(self.score))
        self.score = 0
        self.update_score()

    def update_score(self):
        self.clear()
        self.write(f"Score = {self.score}, High Score = {self.highscore}", False, Alignment, Font)

    def game_over(self):
        super().__init__()
        self.hideturtle()
        self.pencolor('blue')
        self.write(f"Game Over!", False, 'center', ("calibre", 20, "normal"))

    def add_score(self):
        self.score += 1
        self.update_score()


class Food(Turtle):

    def __init__(self):
        super().__init__()
        self.shape('circle')
        self.shapesize(stretch_len=0.5, stretch_wid=0.5)
        self.penup()
        self.color('red')
        X_axis = random.randint(-340, 341)
        Y_axis = random.randint(-240, 241)
        self.speed(20)
        self.goto(X_axis, Y_axis)

    def refresh(self):
        X_axis = random.randint(-340, 341)
        Y_axis = random.randint(-240, 241)
        self.speed(20)
        self.goto(X_axis, Y_axis)


snake = Snake()
food = Food()
score = Score()

screen.listen()
screen.onkey(snake.up, 'Up')
screen.onkey(snake.down, 'Down')
screen.onkey(snake.left, 'Left')
screen.onkey(snake.right, 'Right')

while True:
    try:
        screen.update()
        time.sleep(0.15)
        snake.move()

        # Detect Collision
        for blocks in snake.list1[1:]:
            if snake.head.distance(blocks) < 10:
                score.high_score()
                replay = screen.textinput(title='Replay or Quit', prompt="Replay = 'y', Quit = 'n' ")
                if replay == 'y':
                    snake.reset()
                    screen.listen()
                    score.clear()
                    score.__init__()
                elif replay == 'n':
                    exit()

        # Food Collision Check
        if snake.head.distance(food) < 10:
            food.refresh()
            snake.add_body()
            score.add_score()

        # Detect Side Collision
        A = snake.head.xcor()
        B = snake.head.ycor()
        if ((snake.head.distance(350, B) < 10) or (snake.head.distance(-350, B) < 10) or
                (snake.head.distance(A, 250) < 10) or (snake.head.distance(A, -250) < 10)):
            snake.wall()
    except:
        break

