GOAL_DATA = "ПутинВВ002"  # the string, expected to be read from QR-code
REAL_WIDTH = 0.063  # Physical QR-code size, meter

IMAGE_WIDTH=900 # 1<=int camera resolution: width
IMAGE_HEIGHT=600 # 1<=int camera resolution: height

FRAME_INTERVAL=10 # 1<=int - ratio of all images to operating ones

SHOW_IMAGE_ROW=0 # 1/0 - show image before any operations

COORDINATE_PRINT=0 # 1/0 - print coordinate of found QR-code in console
COORDINATE_DRAW=1 # 1/0 - draw coordinate of found QR-code on camera display

ROLL=1 # 1/0 - calculate roll angle and rotate image
ROLL_PRINT=0 # 1/0 print coordinate of found QR-code in console
ROLL_DRAW=0 # 1/0 draw coordinate of found QR-code on camera display
ROLL_DISPLAY=0 # 1/0 - show the roll calculating procces
ROLL_CENSOR=1 # 1/0 - censor qr-codes during roll calculating
ROLL_CENSOR_DISPLAY=0 # 1/0 - show the censorship procces
ROLL_MAX_ANGLE=10  # 0<=float<=90  - maximum roll angle

KALMAN=1 # 1/0 - use kalman transformation

CALIBRATION_DISPLAY=0 # 1/0 - show the colibration procces
CALIBTARION_IMAGES_PATH='calib_images/*.jpg'
PATTERN_SIZE = (9, 7)  # 9x7 crosses calibration chess board