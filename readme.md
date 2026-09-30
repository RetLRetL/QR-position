# OpenCV Project

# System Requirements
# - Windows 10/11, macOS 10.15+, or Linux (Ubuntu 20.04+ recommended)
# - Conda (Miniconda or Anaconda) installed
# - 4GB+ free disk space

# Installation Guide

# 1.Create and Activate Virtual Environment

# For Windows
conda env create -f environment-windows.yml

conda activate opencv-env

# For Linux
conda env create -f environment-linux.yml

conda activate opencv-env

sudo apt-get update
sudo apt-get install -y \
    libgl1-mesa-glx \
    libsm6 \
    libxext6 \
    libxrender1 \
    libgtk2.0-0 \
    libglib2.0-0

# 2.Verify Successful Activation
You should see (opencv-env) prefix in your terminal prompt. Confirm with:

conda info --envs

# 3.Using the Virtual Environment

conda activate opencv-env

# 4.Launching the program

python main.py

# Program Features

The program uses "config.py" for customizable settings.

# Optimization settings:

Operating images frequency: FRAME_INTERVAL.
Recommended value: 4<=FRAME_INTERVAL<=10.

Resolution: IMAGE_WIDTH, IMAGE_HEIGHT.
Recommended values: IMAGE_WIDTH=800, IMAGE_HEIGHT=600.

Rotating to roll angle: ROLL.

Censored (close, paint over) qr-codes during roll angle calculation: ROLL_CENSOR.

Use Kalman transformation: KALMAN.
Recommended value: KALMAN=1.

# Set up

# The program requires:
1.Calibration;
2.QR-codes.

# Calibration guide:
Make >10 photos of chessboard with user's camera;
photos should be made with different angles,
chessboard should fit the frame.
Place those images in "calib_images" folder
(or other folder, written down in CALIBTARION_IMAGES_PATH in config.py).
Size of crossboard should be filled in PATTERN_SIZE in cofig.py.

# QR-codes requirements:
QR-codes should be stored in "sourse" folder.
The size of real QR-code should be known and filled in REAL_WIDTH in config.py.
Program reads printed QR-codes better.

# Functional testing
"image_final" should display the image, leveled with horizon;
if qr-codes are in frame, goal qr-code should be framed,
program should print distance and angle in console.

# If there are doubts in correctness
there are images, which can display intermediate processes:
SHOW_IMAGE_ROW      - shows image from camera;
CALIBRATION_DISPLAY - shows calibration images with tagged crosses of chessboard;
ROLL_CENSOR_DISPLAY - shows images with censored (closed, painted over) qr-codes;
ROLL_DISPLAY - shows image with horizontal lines for roll angle calculations.

# Keyboard Shortcuts Reference
q - te close window "image"

# Notes
It's better to use printed QR-codes.
Horizon line (or lines close to it) required for roll angle calculations.
Kalman transformation requires a little time before acting properly.
Kalman transformation also increases the CPU load by 1.5 times.
Real size of the goal qr-code should be known.
