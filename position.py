import cv2
import numpy
from config import *


def findDistance(img, points, mtx, dist):

    pixel_width = numpy.linalg.norm(points[0] - points[1])

    focal_length = mtx[0, 0]

    distance = (REAL_WIDTH * focal_length) / pixel_width
    return distance

"""
Gets:   img     - image to search on;
        points  - array with found QR-code corners coordinates;
        mtx     - camera matrix;
        dist    - distortion coefficients.
Provides:   distance - physical distance to the object, meter.  
"""



def findAngles(img, points, distance, mtx):
    focal_length = mtx[0, 0]
    
    img_center = numpy.array([img.shape[1] / 2, img.shape[0] / 2])

    qr_center = numpy.mean(points, axis=0)

    vector = qr_center - img_center
    vector[0]=(vector[0] * distance) / focal_length # px -> meter
    vector[1]=(vector[1] * distance) / focal_length
    

    polar_angle = - numpy.arctan2(vector[1], distance) * 180 / numpy.pi

    azimuthal_angle = numpy.arctan2(vector[0], distance) * 180 / numpy.pi
    
    return polar_angle, azimuthal_angle

"""
Gets:   img     - image to search on;
        points  - array with found QR-code corners coordinates;
        distance- physical distance to the object, meter;
        mtx     - camera matrix;
Provides:   polar_angle - polar angular, up from horizon (center), degrees;
            azimuthal_angle - right from meridian(center), degrees;
"""

def drawPosition(img, distance, polar_angle, azimuthal_angle, x, y):
    cv2.putText(img,f"distance: {distance:.3f} meter",\
                (x, y+30),\
                cv2.FONT_HERSHEY_SIMPLEX,\
                1, (0, 0, 0), 6, cv2.LINE_AA)
    cv2.putText(img,f"distance: {distance:.3f} meter",\
                (x, y+30),\
                cv2.FONT_HERSHEY_SIMPLEX,\
                1, (255, 0, 0), 2, cv2.LINE_AA)
    
    cv2.putText(img, f"Polar angle: {polar_angle:.3f} degree",\
                (x, y+60),\
                cv2.FONT_HERSHEY_SIMPLEX,\
                1, (0, 0, 0), 6, cv2.LINE_AA)
    cv2.putText(img, f"Polar angle: {polar_angle:.3f} degree",\
                (x, y+60),\
                cv2.FONT_HERSHEY_SIMPLEX,\
                1, (0, 255, 0), 2, cv2.LINE_AA)
    
    
    cv2.putText(img, f"Azimutal angle: {azimuthal_angle:.3f} degree",\
                (x, y+90),\
                cv2.FONT_HERSHEY_SIMPLEX,\
                1, (0, 0, 0), 6, cv2.LINE_AA)
    cv2.putText(img, f"Azimutal angle: {azimuthal_angle:.3f} degree",\
                (x, y+90),\
                cv2.FONT_HERSHEY_SIMPLEX,\
                1, (0, 0, 255), 2, cv2.LINE_AA)
    
"""
Function transform image by adding given parametrs around given coordinates;
Gets:   img             - image to search on;
        distance        - parametr 1;
        polar_angle     - parametr 2;
        azimuthal_angle - parametr 3;
        x, y            - coordinates.

"""

def printPosition(distance, polar_angle, azimuthal_angle):
    print(f"distance={distance:0^4.4f}m polar_angle={polar_angle:0^4.4f}° azimuthal_angle={azimuthal_angle:0^4.4f}°") 

"""
Function prints given parametrs in console;
"""

