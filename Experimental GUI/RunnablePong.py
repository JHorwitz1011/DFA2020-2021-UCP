"""
Pong code transplated into a function so it can be called from a GUI script

"""

import turtle
import imutils
from cv2 import cv2
from imutils.video import VideoStream
import time
import sys
import numpy as np




def main():
    TAG_TYPE = "DICT_ARUCO_ORIGINAL"
    FRAME_WIDTH = 800
    FRAME_HEIGHT = 800
    UP_MARKER = 5
    DOWN_MARKER = 7
    FRAMES_NEEDED = 2
    frame_count_up = 0
    frame_count_down = 0

    BALL_SPEED = 5

    ARUCO_DICT = {
        "DICT_4X4_50": cv2.aruco.DICT_4X4_50,
        "DICT_4X4_100": cv2.aruco.DICT_4X4_100,
        "DICT_4X4_250": cv2.aruco.DICT_4X4_250,
        "DICT_4X4_1000": cv2.aruco.DICT_4X4_1000,
        "DICT_5X5_50": cv2.aruco.DICT_5X5_50,
        "DICT_5X5_100": cv2.aruco.DICT_5X5_100,
        "DICT_5X5_250": cv2.aruco.DICT_5X5_250,
        "DICT_5X5_1000": cv2.aruco.DICT_5X5_1000,
        "DICT_6X6_50": cv2.aruco.DICT_6X6_50,
        "DICT_6X6_100": cv2.aruco.DICT_6X6_100,
        "DICT_6X6_250": cv2.aruco.DICT_6X6_250,
        "DICT_6X6_1000": cv2.aruco.DICT_6X6_1000,
        "DICT_7X7_50": cv2.aruco.DICT_7X7_50,
        "DICT_7X7_100": cv2.aruco.DICT_7X7_100,
        "DICT_7X7_250": cv2.aruco.DICT_7X7_250,
        "DICT_7X7_1000": cv2.aruco.DICT_7X7_1000,
        "DICT_ARUCO_ORIGINAL": cv2.aruco.DICT_ARUCO_ORIGINAL,
        "DICT_APRILTAG_16h5": cv2.aruco.DICT_APRILTAG_16h5,
        "DICT_APRILTAG_25h9": cv2.aruco.DICT_APRILTAG_25h9,
        "DICT_APRILTAG_36h10": cv2.aruco.DICT_APRILTAG_36h10,
        "DICT_APRILTAG_36h11": cv2.aruco.DICT_APRILTAG_36h11
    }

    if ARUCO_DICT.get(TAG_TYPE, None) is None:
        print("[INFO] ArUCo tag of '{}' is not supported".format(
        TAG_TYPE))
        sys.exit(0)

    print("[INFO] detecting '{}' tags...".format(TAG_TYPE))
    arucoDict = cv2.aruco.Dictionary_get(ARUCO_DICT[TAG_TYPE])
    arucoParams = cv2.aruco.DetectorParameters_create()

    global camera 
    camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)

    if not camera.isOpened():
        print("Camera could not be referenced")
        exit(0)

    global wn
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
    ball1.dx = BALL_SPEED
    ball1.dy = -BALL_SPEED

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


    def paddle_a_up():
        y = paddle_a.ycor()
        y += 20
        paddle_a.sety(y)


    def paddle_a_down():
        y = paddle_a.ycor()
        y -= 20
        paddle_a.sety(y)


    def paddle_b_up():
        y = paddle_b.ycor()
        y += 20
        paddle_b.sety(y)


    def paddle_b_down():
        y = paddle_b.ycor()
        y -= 20
        paddle_b.sety(y)

    def readFrame(frame_count_up, frame_count_down):
        ret, frame = camera.read()

        if ret:
            frame = imutils.resize(frame, FRAME_WIDTH)
            #(H, W) = frame.shape[:2]

            (corners, ids, _rejected) = cv2.aruco.detectMarkers(frame, arucoDict, parameters = arucoParams)
            cv2.aruco.drawDetectedMarkers(frame,corners,ids,(0,255,0))

            if ids is not None:
                frame_count_up += detect(UP_MARKER, ids)
                frame_count_down += detect(DOWN_MARKER, ids)

                """
                for (markerCorner, _markerID) in zip(corners, ids):
                    corners = markerCorner.reshape((4,2))
                    (topLeft, _topRight, bottomRight, _bottomLeft) = corners
                    cX = int((topLeft[0] + bottomRight[0]) / 2.0)
                    cY = int((topLeft[1] + bottomRight[1]) / 2.0)

                    if cX < (W // 3) and cY < (H // 3):
                        paddle_a_up
                    if cX < (W // 3) and cY > (H // 3):
                        paddle_a_down
                """
            
            frame = cv2.flip(frame, 1)
            #cv2.rectangle(frame, (0, 0), (W // 3, H // 3), (255, 0, 0), 3)
            #cv2.rectangle(frame, (0, (H // 3) * 2), (W//3, H), (0, 0, 255), 3)
            cv2.imshow('Frame', frame)
        
        return frame_count_up, frame_count_down

    def detect(markerID, ids):
        return 1 if markerID in ids else 0

    # Keyboard binding
    wn.listen()
    wn.onkeypress(paddle_a_up, "w")
    wn.onkeypress(paddle_a_down, "s")
    wn.onkeypress(paddle_b_up, "Up")
    wn.onkeypress(paddle_b_down, "Down")


    # Main game loop
    while True:
        timeCheck = time.time()

        wn.update()
        (frame_count_up, frame_count_down) = readFrame(frame_count_up, frame_count_down)

        if frame_count_up > FRAMES_NEEDED:
            paddle_a_up()
            frame_count_up = 0

        if frame_count_down > FRAMES_NEEDED:
            paddle_a_down()
            frame_count_down = 0


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
        
        print('fps - ',1/(time.time()-timeCheck))


def quit():
    cv2.destroyAllWindows()
    camera.release()
    turtle.Screen().bye()