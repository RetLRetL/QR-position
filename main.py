import cv2
from search import *
from setup import *
from roll import *
from config import *

processing_counter = 0

resulutionSetup(cap) 
ret=0
while(ret==0):
    ret, mtx, dist=calibration(CALIBRATION_DISPLAY)

while True:
           
    ret, img = cap.read()
    processing_counter += 1

    # To break the programm
    if cv2.waitKey(1) == ord('q'):
            break

    if processing_counter % FRAME_INTERVAL == 0:
        
        # Show original image
        if SHOW_IMAGE_ROW:
            cv2.imshow('image_row', img)
        
        # Rotate image to roll angle
        if ROLL:
            img=roll(img, detector)

        # Find qr
        search_and_print(img, GOAL_DATA, detector, mtx, dist)

        cv2.imshow('image_final', img)
        
