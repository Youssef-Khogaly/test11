import cv2
import numpy as np
def process_LaneDetection(img):
    """
    Processes the given image to detect lanes and draw the center.
    
    Args:
    - img: Input image.
    """
    cv2.imshow("org",img)
    # Apply Gaussian blur to smooth the image and reduce noise
    blurred = cv2.GaussianBlur(img, (5, 5), 0)
    
    # Convert the image to grayscale for easier edge detection
    gray = cv2.cvtColor(blurred, cv2.COLOR_BGR2GRAY)
    
    # Perform edge detection using the Canny algorithm
    edges = cv2.Canny(gray, 75, 150)
    cv2.imshow("EdgeDetections",edges)
    # Get the dimensions of the edge-detected image
    height, width = edges.shape
    
    # Create an empty mask to apply the region of interest (ROI)
    mask = np.zeros_like(edges)
    
    # Define the region of interest (ROI) as a polygon (trapezoid) for lane detection
    roi_corners = np.array([[
        (int(0), 380),  # bottom left
        (int(0), int(270)),  # top left
        (int(520), int(270)),  # top right
        (int(633), 380)  # bottom right
    ]], dtype=np.int32)
    
    # Fill the ROI polygon with white color on the mask to isolate the region of interest
    cv2.fillPoly(mask, roi_corners, 255)
    
    # Apply the mask to the edges to keep only the edges inside the ROI
    masked_edges = cv2.bitwise_and(edges, mask)
    cv2.imshow("maskedEdges2",masked_edges)
    # Detect lines using the Hough Line Transform on the masked edges
    lines = cv2.HoughLinesP(masked_edges, 1, np.pi / 180, 50, maxLineGap=200)
    
    # Create a copy of the original image to draw the lane lines
    output_img = img.copy()

    # Lists to store left and right lane lines
    left_lines = []
    right_lines = []

    # If lines are detected, process each line
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line.reshape(4)

            # Skip vertical lines
            if x2 == x1:
                continue
            
            # Calculate the slope and y-intercept of the line
            parameters = np.polyfit((x1, x2), (y1, y2), 1)
            slope = parameters[0]
            y_int = parameters[1]

            # Skip nearly horizontal lines
            if abs(slope) < 0.3:
                continue
            
            # Classify lines as left or right based on slope
            if slope < 0:
                left_lines.append((slope, y_int))
            elif slope > 0:
                right_lines.append((slope, y_int))

        # Function to make lane points based on the average slope and intercept
        def make_points(image, average): 
            slope, y_int = average 
            y1 = image.shape[0]
            y2 = int(y1 * (4/5))  
            x1 = int((y1 - y_int) / slope)
            x2 = int((y2 - y_int) / slope)
            return np.array([x1, y1, x2, y2])
        
        # Calculate the average slope and y-intercept for left and right lanes
        if left_lines:
            left_avg = np.average(left_lines, axis=0)
            left_lane = make_points(masked_edges, left_avg)
            x1, y1, x2, y2 = left_lane
            cv2.line(output_img, (x1, y1), (x2, y2), (255, 0, 0), 10)

        if right_lines:
            right_avg = np.average(right_lines, axis=0)
            right_lane = make_points(masked_edges, right_avg)
            x1, y1, x2, y2 = right_lane
            cv2.line(output_img, (x1, y1), (x2, y2), (255, 0, 0), 10)

        # Find the center point between the bottom of the left and right lanes
        if left_lines and right_lines:
            left_x = left_lane[0]
            left_y = left_lane[1]
            right_x = right_lane[0]
            right_y = right_lane[1]
            center_x = (left_x + right_x) // 2
            center_y = (left_y + right_y) // 2  # Center at the bottom
            cv2.circle(output_img, (center_x, center_y), 6, (0, 0, 255), -1)

    return output_img, masked_edges  # Return both the output image and edges after masking



def process_video(video_path, show=True):
    """
    Process an entire video frame by frame.
    
    Args:
    - video_path (str): Path to the input video.
    - show (bool): If True, display the processed frames.
    """
    # Open the video
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print(f"Error: Unable to open video file {video_path}")
        return
    
    while True:
        ret, frame = cap.read()
        
        # If no frame is returned, end of video
        if not ret:
            break
        # Process the current frame
        frame,roi = process_LaneDetection(frame)
        if show:
            cv2.imshow("Camera Feed", frame)
            cv2.imshow("ROI Display", roi)  # Display the ROI in a separate window
        if cv2.waitKey(30) == 27:  # Wait for 30 ms and check if 'Esc' is pressed (key code 27)
            break  # Exit the loop if 'Esc' is pressed

    # Release the video capture object
    cap.release()


def main():
    
    process_video("/home/khogaly/graduation/test_images/Lane_Detection_test.mp4" ,show=True)
main()
