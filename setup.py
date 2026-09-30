import sys
import cv2
import numpy 
import glob
from config import *
from roll import *

cap = cv2.VideoCapture(0)       #initialise camera and detector from opencv
detector = cv2.QRCodeDetector()



def resulutionSetup(cap):
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, IMAGE_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, IMAGE_HEIGHT)
    actual_width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    actual_height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    print(f"Resolution: {actual_width}x{actual_height}")
    return 1


def calibration(bit): # bit = 1/0 - show the procces

    # Preparing arrays for 3D points
    objp = numpy.zeros((PATTERN_SIZE[0] * PATTERN_SIZE[1], 3), numpy.float32)
    objp[:, :2] = numpy.mgrid[0:PATTERN_SIZE[0], 0:PATTERN_SIZE[1]].T.reshape(-1, 2)

    objpoints = []  # 3D points in space
    imgpoints = []  # 2D points ob flat

    images = glob.glob(CALIBTARION_IMAGES_PATH)

    for fname in images:
        img = cv2.imread(fname)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Crosses searching
        ret, corners = cv2.findChessboardCorners(gray, PATTERN_SIZE, None)

        if ret:
            objpoints.append(objp)
            imgpoints.append(corners)

            # show the procces
            if bit:
                cv2.drawChessboardCorners\
                    (img, PATTERN_SIZE, corners, ret)
                cv2.imshow('Chessboard', img)
                cv2.waitKey(500)

    cv2.destroyAllWindows()

    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera\
        (objpoints, imgpoints, gray.shape[::-1], None, None)

    if ret:
        #check for projection errors
        mean_error = 0
        for i in range(len(objpoints)):

            # 3D points projects on 2D points
            imgpoints2, _ = cv2.projectPoints\
                (objpoints[i], rvecs[i], tvecs[i], mtx, dist)

            # Calculatintg the differences between real and projected points
            error = cv2.norm(imgpoints[i], imgpoints2, cv2.NORM_L2)\
                  / len(imgpoints2)
            mean_error += error

        mean_error /= len(objpoints)
        if mean_error>1:
            print("Calibration error: mean_error={mean_error:.3f} > 1.000")
            sys.exit(1)
        return 1, mtx, dist
    else:
        return 0, None, None
    
""""
Function fulfill the calibration of video camera.

Set of images ('calib_images/*.jpg') incorporates many photos, made with
    calibrating video camera.

Returns:    success marker;
            mtx - camera matrix;
            dist - camera distortion coefficients.
"""

