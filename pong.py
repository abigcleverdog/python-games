import turtle

BALL_SPEED = .1

wn = turtle.Screen()
wn.title("Pong Game")
wn.bgcolor("black")
wn.setup(800, 600)
wn.tracer(0)

# Scores
score_a = 0
score_b = 0

# Paddle A
paddle_a = turtle.Turtle()
paddle_a.speed(0)
paddle_a.shape("square")
paddle_a.color("white")
paddle_a.shapesize(stretch_wid=5, stretch_len=1)
paddle_a.penup()
paddle_a.goto(-350, 0)

# Paddle B
paddle_b = turtle.Turtle()
paddle_b.speed(0)
paddle_b.shape("square")
paddle_b.color("white")
paddle_b.shapesize(stretch_wid=5, stretch_len=1)
paddle_b.penup()
paddle_b.goto(350, 0)

# Ball
ball = turtle.Turtle()
ball.speed(0)
ball.shape("square")
ball.color("white")
ball.penup()
ball.goto(0, 0)
ball.dx = BALL_SPEED
ball.dy = BALL_SPEED


# Functions
def paddle_a_up():
    y = paddle_a.ycor()
    if abs(y) > 250:
        y = 250 * y / abs(y)
    paddle_a.sety(y + 20)


def paddle_a_down():
    y = paddle_a.ycor()
    if abs(y) > 250:
        y = 250 * y / abs(y)
    paddle_a.sety(y - 20)


def paddle_b_up():
    y = paddle_b.ycor()
    if abs(y) > 250:
        y = 250 * y / abs(y)
    paddle_b.sety(y + 20)


def paddle_b_down():
    y = paddle_b.ycor()
    if abs(y) > 250:
        y = 250 * y / abs(y)
    paddle_b.sety(y - 20)


# Pen
pen = turtle.Turtle()
pen.speed(0)
pen.color("white")
pen.penup()
pen.hideturtle()
pen.goto(0, 260)
pen.write(f"Player A: {score_a}  Player B: {score_b}", align="center", font=("Courier", 24, "normal"))

wn.listen()
wn.onkeypress(paddle_a_up, "w")
wn.onkeypress(paddle_a_down, "r")
wn.onkeypress(paddle_b_up, "Up")
wn.onkeypress(paddle_b_down, "Down")

while True:
    wn.update()

    # Move the ball
    ball.setx(ball.xcor() + ball.dx)
    ball.sety(ball.ycor() + ball.dy)

    # Border checking
    if abs(ball.ycor()) > 290:
        ball.sety(ball.ycor())
        ball.dy *= -1

    if abs(ball.xcor()) > 390:
        if ball.xcor() > 0:
            score_a += 1
        else:
            score_b += 1
        pen.clear()
        pen.write(f"Player A: {score_a}  Player B: {score_b}", align="center", font=("Courier", 24, "normal"))
        ball.goto(0, 0)
        ball.dx *= -1

    # paddle hits ball
    if (paddle_b.xcor() - 20 <= ball.xcor() <= paddle_b.xcor() - 10 and
            paddle_b.ycor() - 50 <= ball.ycor() <= paddle_b.ycor() + 50
    ) or (paddle_a.xcor() + 10 <= ball.xcor() <= paddle_a.xcor() + 20 and (
            paddle_a.ycor() - 50 <= ball.ycor() <= paddle_a.ycor() + 50)):
        ball.dx *= -1
