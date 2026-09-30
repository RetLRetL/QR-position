import cv2
import numpy
from position import *
from config import *
from kalman import *

if KALMAN:
    qr_kf = KalmanFilter()

def search_any(img, detector):
    data, bbox, _ = detector.detectAndDecode(img)
    if bbox is None:
        # if there is no qr found, get predicted data
        x_pred, y_pred = qr_kf.update(None, None) 
        return numpy.array([[x_pred, y_pred], [x_pred+10, y_pred], [x_pred+10, y_pred+10], [x_pred, y_pred+10]])
    
    points = bbox.reshape(-1, 2)
    # center of found qr
    center = numpy.mean(points, axis=0)
    # change Kalman filter 
    x_filtered, y_filtered = qr_kf.update(center[0], center[1])
    
    # change points with Kalman data
    offset = numpy.array([x_filtered, y_filtered]) - center
    return points + offset

"""
Gets:   "img" as an array  from numpy;
        "detector" as a QRCodeDetector object.

Provides: massive of points of corners of any qr.

"""

def search_and_print(img, GOAL_DATA, detector, mtx, dist):
    retval, decoded_info, points, _ = detector.detectAndDecodeMulti(img)
    if not retval or points is None:
        return 0, 0, 0

    for data, pts in zip(decoded_info, points):
        if data.strip() != GOAL_DATA.strip():
            continue  # only goal qr is operating

        # center of found qr
        center = numpy.mean(pts, axis=0)
        # change Kalman filter 
        x_kf, y_kf = qr_kf.update(center[0], center[1])  # Калман-фильтр

        # change points with Kalman data
        offset = numpy.array([x_kf, y_kf]) - center
        pts_filtered = pts + offset

        # visualization
        for j in range(len(pts_filtered)):
            pt1 = tuple(map(int, pts_filtered[j]))
            pt2 = tuple(map(int, pts_filtered[(j + 1) % len(pts_filtered)]))
            cv2.line(img, pt1, pt2, (100, 100, 100), 5)

        # position calculating
        distance = findDistance(img, pts_filtered, mtx, dist)
        polar_angle, azimuthal_angle = findAngles(img, pts_filtered, distance, mtx)
        pt_display = tuple(map(int, pts_filtered[2]))

        if COORDINATE_PRINT:
            drawPosition(img, distance, polar_angle, azimuthal_angle, pt_display[0], pt_display[1])
        if COORDINATE_DRAW:
            printPosition(distance, polar_angle, azimuthal_angle)

        return distance, polar_angle, azimuthal_angle

    return 0, 0, 0

"""
Gets:  "img" as an array  from numpy;
        "goal data" as a string;
        "detector" as a QRCodeDetector object.

Provides: tranformed image ("img" with outlined QR-code if found).

"""

