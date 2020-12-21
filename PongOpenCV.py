# Simple Pong in Python 3 for Beginners
# By @TokyoEdTech
# Part 10: Simplifying Your Code (One Year and a Half Later!)

import turtle
import imutils
from cv2 import cv2 as cv


FRAME_WIDTH = 800
FRAME_HEIGHT = 800
RADIUS = 25
FRAMES_NEEDED = 5
frame_count_up = 0
frame_count_down = 0

#Currently set to a green object for up and blue for down
#(36, 202, 59, 71, 255, 255)    # Green
#(18, 0, 196, 36, 255, 255)  # Yellow
#(89, 0, 0, 125, 255, 255)  # Blue
#(0, 100, 80, 10, 255, 255)   # Red
colorUpLower = (36,202,59)
colorUpUpper = (71,255,255)
colorDownLower = (0,100,80)
colorDownUpper = (10,255,255)

camera = cv.VideoCapture(0)
camera.set(cv.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
camera.set(cv.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)

if not camera.isOpened():
    print("Camera could not be referenced")
    exit(0)


wn = turtle.Screen()
wn.title("Pong by @TokyoEdTech")
wn.bgcolor("black")
wn.setup(width=800, height=600)
wn.tracer(0)

# Score
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
ball1 = turtle.Turtle()
ball1.speed(0)
ball1.shape("square")
ball1.color("green")
ball1.penup()
ball1.goto(0, 0)
ball1.dx = 3
ball1.dy = -3

balls = [ball1]  # balls = [ball1, ball2, ball3, ball4]

# Pen
pen = turtle.Turtle()
pen.speed(0)
pen.color("white")
pen.penup()
pen.hideturtle()
pen.goto(0, 260)
pen.write("Player A: 0  Player B: 0", align="center",
          font=("Courier", 24, "normal"))

# Function


def paddle_a_up():
    y = paddle_a.ycor()
    y += 20
    if y > 305:
        paddle_a.sety(-300)
    paddle_a.sety(y)


def paddle_a_down():
    y = paddle_a.ycor()
    y -= 20
    if y < -305:
        paddle_a.sety(300)
    paddle_a.sety(y)


def paddle_b_up():
    y = paddle_b.ycor()
    y += 20
    paddle_b.sety(y)


def paddle_b_down():
    y = paddle_b.ycor()
    y -= 20
    paddle_b.sety(y)


def detectColor(colorLow, colorUpper):
    ret, frame = camera.read()

    if ret:
        # Process frame @ lower quality level
        frame = imutils.resize(frame, width=600)
        blurred = cv.GaussianBlur(frame, (11, 11), 0)
        hsv = cv.cvtColor(blurred, cv.COLOR_BGR2HSV)

        mask = cv.inRange(hsv, colorLow, colorUpper)
        mask = cv.erode(mask, None, iterations=2)
        mask = cv.dilate(mask, None, iterations=2)

        cv.imshow('Mask', mask)

        # Pull contours to draw
        contours = cv.findContours(
            mask.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        contours = imutils.grab_contours(contours)
        center = None

        if len(contours) > 0:
            maxC = max(contours, key=cv.contourArea)
            ((x, y), radius) = cv.minEnclosingCircle(maxC)
            M = cv.moments(maxC)
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

            if radius > RADIUS:
                cv.circle(frame, (int(x), int(y)),
                          int(radius), (0, 255, 255), 2)
                cv.circle(frame, center, 5, (0, 0, 255), -1)
                return 1

        frame = cv.flip(frame, 1)
        cv.imshow('Frame', frame)
        return 0

def readFrame():
    ret, frame = camera.read()

    if ret:
        # Process frame @ lower quality level
        frame = imutils.resize(frame, width=600)
        blurred = cv.GaussianBlur(frame, (11, 11), 0)
        hsv = cv.cvtColor(blurred, cv.COLOR_BGR2HSV)

        mask = cv.inRange(hsv, colorUpLower, colorUpUpper)
        mask = cv.erode(mask, None, iterations=2)
        mask = cv.dilate(mask, None, iterations=2)

        cv.imshow('Mask', mask)

        # Pull contours to draw
        contours = cv.findContours(
            mask.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        contours = imutils.grab_contours(contours)
        center = None

        if len(contours) > 0:
            maxC = max(contours, key=cv.contourArea)
            ((x, y), radius) = cv.minEnclosingCircle(maxC)
            M = cv.moments(maxC)
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

            if radius > RADIUS:
                cv.circle(frame, (int(x), int(y)),
                          int(radius), (0, 255, 255), 2)
                cv.circle(frame, center, 5, (0, 0, 255), -1)
                global frame_count_up
                frame_count_up = frame_count_up + 1

        frame = cv.flip(frame, 1)
        cv.imshow('Frame', frame)


# Keyboard binding
wn.listen()
wn.onkeypress(paddle_a_up, "w")
wn.onkeypress(paddle_a_down, "s")
wn.onkeypress(paddle_b_up, "Up")
wn.onkeypress(paddle_b_down, "Down")


# Main game loop
while True:
    wn.update()
    readFrame()
    frame_count_up = frame_count_up + detectColor(colorUpLower,colorUpUpper)
    #frame_count_down = frame_count_down + detectColor(colorDownLower,colorDownUpper)

    if frame_count_up > FRAMES_NEEDED:
        paddle_a_up()
        frame_count_up = 0


    wn.update()

    for ball in balls:
        # Move the ball
        ball.setx(ball.xcor() + ball.dx)
        ball.sety(ball.ycor() + ball.dy)

        # Border checking
        if ball.ycor() > 290:
            ball.sety(290)
            ball.dy *= -1
            #os.system("afplay bounce.wav&")

        if ball.ycor() < -290:
            ball.sety(-290)
            ball.dy *= -1
            #os.system("afplay bounce.wav&")

        if ball.xcor() > 390:
            ball.goto(0, 0)
            ball.dx *= -1
            score_a += 1
            pen.clear()
            pen.write("Player A: {}  Player B: {}".format(
                score_a, score_b), align="center", font=("Courier", 24, "normal"))

        if ball.xcor() < -390:
            ball.goto(0, 0)
            ball.dx *= -1
            score_b += 1
            pen.clear()
            pen.write("Player A: {}  Player B: {}".format(
                score_a, score_b), align="center", font=("Courier", 24, "normal"))

        # Paddle and ball collisions
        if (ball.xcor() > 340 and ball.xcor() < 350) and (ball.ycor() < paddle_b.ycor() + 40 and ball.ycor() > paddle_b.ycor() - 40):
            ball.setx(340)
            ball.dx *= -1
            #os.system("afplay bounce.wav&")

        if (ball.xcor() < -340 and ball.xcor() > -350) and (ball.ycor() < paddle_a.ycor() + 40 and ball.ycor() > paddle_a.ycor() - 40):
            ball.setx(-340)
            ball.dx *= -1
            #os.system("afplay bounce.wav&")



cv.destroyAllWindows()
camera.release()
