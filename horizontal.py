import cv2
import numpy as np

def detect_horizontal_lines(section_img, section_name="Section"):
    """
    Detect horizontal lines in the given section image.
    Returns:
      - output: the section image with drawn horizontal lines,
      - y_coords_filtered: a list of the filtered y-coordinates for the detected lines.
    """
    # Convert image to grayscale
    gray = cv2.cvtColor(section_img, cv2.COLOR_BGR2GRAY)
    
    # Optional: smooth the image
    gray = cv2.GaussianBlur(gray, (3, 3), 0)
    
    # Invert so lines become white
    gray = cv2.bitwise_not(gray)
    
    # Binarize the image
    _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    
    # Morphology to isolate horizontal lines:
    # Use a wide kernel to connect across bubbles
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (40, 1))
    horizontal_lines = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel)
    horizontal_lines = cv2.morphologyEx(horizontal_lines, cv2.MORPH_CLOSE, kernel)
    
    # Additional bridging to further connect broken parts
    bridge_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (10, 1))
    horizontal_lines = cv2.dilate(horizontal_lines, bridge_kernel, iterations=1)
    
    # Hough Transform to detect horizontal line segments
    lines = cv2.HoughLinesP(horizontal_lines, 1.5, np.pi / 180,
                            threshold=30, minLineLength=8, maxLineGap=1000)
    
    # Create a copy to draw lines on
    output = section_img.copy()
    y_coords_raw = []
    
    # Loop over detected lines and keep those that are near-horizontal
    if lines is not None:
        for x1, y1, x2, y2 in lines[:, 0]:
            length = np.sqrt((x2 - x1)**2 + (y2 - y1)**2)
            angle = abs(np.degrees(np.arctan2(y2 - y1, x2 - x1)))
            if angle < 5:  # near horizontal
                # Draw the detected line
                cv2.line(output, (x1, y1), (x2, y2), (0, 255, 0), 2)
                # Get the average y coordinate of the line
                y_avg = (y1 + y2) // 2
                y_coords_raw.append(y_avg)
    
    # Filter duplicate/close y-coordinates
    y_coords_raw.sort()
    y_coords_filtered = []
    duplicate_threshold = 10  # pixels
    
    for y in y_coords_raw:
        if not y_coords_filtered or abs(y - y_coords_filtered[-1]) > duplicate_threshold:
            y_coords_filtered.append(y)
    
    # Optionally, draw the filtered horizontal lines (full width) and print their y positions
    for y in y_coords_filtered:
        cv2.line(output, (0, y), (output.shape[1], y), (0, 255, 0), 2)
        print(f"{section_name} - Horizontal line at y = {y}")
    
    return output, y_coords_filtered

# Example usage:


