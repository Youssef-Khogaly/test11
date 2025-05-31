import cv2 as cv
import numpy as np
import os
import glob
import csv

# === Configuration ===
CHESS_BOARD_DIM = (8, 5)
SQUARE_SIZE = 2.5  # Set this to actual size of your square (e.g., in cm or mm)
images_path = "images/*.png"
output_csv = "camera_parameters.csv"

# === Prepare object points ===
objp = np.zeros((CHESS_BOARD_DIM[0] * CHESS_BOARD_DIM[1], 3), np.float32)
objp[:, :2] = np.mgrid[0:CHESS_BOARD_DIM[0], 0:CHESS_BOARD_DIM[1]].T.reshape(-1, 2)
objp *= SQUARE_SIZE  # scale to actual square size

# === Arrays to store object points and image points ===
objpoints = []  # 3d points in real world
imgpoints = []  # 2d points in image plane

# === Read calibration images ===
images = glob.glob(images_path)
if not images:
    print("❌ No calibration images found!")
    exit()

print(f"📷 Found {len(images)} images. Starting calibration...")

for fname in images:
    img = cv.imread(fname)
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    ret, corners = cv.findChessboardCorners(gray, CHESS_BOARD_DIM, None)

    if ret:
        objpoints.append(objp)
        corners2 = cv.cornerSubPix(gray, corners, (11, 11), (-1, -1),
                                   (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001))
        imgpoints.append(corners2)
    else:
        print(f"⚠️ Chessboard not found in {fname}")

# === Calibration ===
ret, cameraMatrix, distCoeffs, rvecs, tvecs = cv.calibrateCamera(
    objpoints, imgpoints, gray.shape[::-1], None, None)

if ret:
    print("✅ Calibration successful!")
    print("Camera matrix:\n", cameraMatrix)
    print("Distortion coefficients:\n", distCoeffs.ravel())

    # === Save to CSV ===
    with open(output_csv, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Camera Matrix'])
        writer.writerows(cameraMatrix)
        writer.writerow(['Distortion Coefficients'])
        writer.writerow(distCoeffs.ravel())
    print(f"💾 Calibration parameters saved to: {output_csv}")
else:
    print("❌ Calibration failed!")
