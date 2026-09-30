import cv2
import numpy
from config import *
from search import *
import math

def censor_search(img, detector):
    points=search_any(img, detector)
    if points is None:
        return None
    for j in range(len(points)):
        pt1 = tuple(map(int, points[j]))
        pt2 = tuple(map(int, points[(j + 1) % len(points)]))
    center = numpy.mean(points, axis=0).astype(int)
    radius = int(numpy.linalg.norm(points[0] - center))
    cv2.circle(img, tuple(center), radius, (0, 0, 0), -1)
    if ROLL_CENSOR_DISPLAY==1:
        cv2.imshow('cosnsor', img)
    return img

def censor_point(img, detector, points):
    for j in range(len(points)):
        pt1 = tuple(map(int, points[j]))
        pt2 = tuple(map(int, points[(j + 1) % len(points)]))
    center = numpy.mean(points, axis=0).astype(int)
    radius = int(numpy.linalg.norm(points[0] - center))
    cv2.circle(img, tuple(center), radius, (0, 0, 0), -1)
    if ROLL_CENSOR_DISPLAY==1:
        cv2.imshow('cosnsor', img)
    return img