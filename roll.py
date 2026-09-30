import cv2
import numpy
from config import *
from setup import *
from search import *
from censore import *
from kalman import *
import math

if KALMAN:
    kf = KalmanFilter()

def rotate_image(image, angle):
    
    h, w = image.shape[:2]
    center = (w // 2, h // 2)
    
    # Rotating matrix
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    M[0, 2] += (w / 2) - center[0]
    M[1, 2] += (h / 2) - center[1]
    
    # Transformation
    rotated = cv2.warpAffine(image, M, (w, h), 
                           flags=cv2.INTER_LINEAR,
                           borderMode=cv2.BORDER_CONSTANT,
                            borderValue=(0, 0, 0))
    return rotated

"""
Gets:  "img" as an array  from numpy;
        "angle" as a float;

Provides: tranformed image (rotated to angle).

"""

def roll_angle(image, height, width, img_display):
    # Conver image into gray one
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Blur image
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    # detect edges using Canny algorithm
    edges = cv2.Canny(blurred, 50, 150)

    # Detect lines using Probabilistic Hough Transform
    lines = cv2.HoughLinesP(
        edges,
        rho=1,              
        theta=numpy.pi/180,
        threshold=100,       
        minLineLength=100,   
        maxLineGap=10        
    )

    if lines is None:
        return 0
    
    angles = []
    for line in lines:
        x1, y1, x2, y2 = line[0]
        
        # Calculate roll angle
        angle = math.degrees(math.atan2(y2 - y1, x2 - x1))
        
        # Filter of angles
        if abs(angle) < ROLL_MAX_ANGLE:  # допуск ±15 градусов
            angles.append(angle)
            # Visualization
            if ROLL_DISPLAY:
                cv2.line(img_display, (x1, y1), (x2, y2), (0, 0, 255), 2)

    if ROLL_DISPLAY:
        if ROLL_DRAW:
            roll_draw(img_display, angle)
        if ROLL_PRINT:
            roll_print(img_display, angle)    
        cv2.imshow('roll display', img_display)
    
    if not angles:
        return 0

    # Mean angle
    median_angle = numpy.median(angles)
    # Kalman transformation
    if KALMAN:
        return kf.update(median_angle, 0.0)[0]
    else:
        return median_angle

"""
Gets:   "image" as an array  from numpy;
        "height" as a float;
        "width" as a float; 
        "img_display" as an array  from numpy

Provides: float; dislayed iamge.

"""

def roll_print(img, median_angle):
    print(f"Угол крена камеры: {median_angle:.2f}°")

def roll_draw(img, median_angle):
    cv2.putText(
        img,
        f"Roll: {median_angle:.2f}°",
        (10, 30),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 0, 255),
        2
    )

def roll(img, detector):
    img_display = img.copy() 
    img_censored = img.copy() 
    # Censorship of image for angle calculations
    if ROLL_CENSOR==1: img_censored=censor_search(img_censored, detector)
    if img_censored is None:
        img_censored = img.copy()
    # Roll angle calculation
    angle=roll_angle(img_censored, IMAGE_HEIGHT, IMAGE_WIDTH, img_display)
    # Rotates image
    return rotate_image(img, angle)

"""
Gets:   "image" as an array  from numpy;
        "detector" as a QRCodeDetector object.

Provides: rotated array from numpy; dislayed image.

"""
