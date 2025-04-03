import cv2
import numpy as np

def detect_vertical_lines(section_img, section_name="Section"):
    """
    Process the section image to detect vertical lines.
    Returns the output image (with drawn lines), a list of filtered x-coordinates,
    and a list of column ranges (each as a tuple: (start_x, end_x)).
    """
    # Convert to grayscale
    gray = cv2.cvtColor(section_img, cv2.COLOR_BGR2GRAY)
    
    # Invert to make lines white
    gray = cv2.bitwise_not(gray)
    
    # Binarize image
    _, binary = cv2.threshold(gray, 0, 255,
                              cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    
    # Morphology to isolate vertical lines using a tall, narrow kernel
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 15))
    vertical_lines = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel)
    
    # Hough Transform to detect vertical line segments 
    # pls dont fucking touch this
    lines = cv2.HoughLinesP(vertical_lines, 1, np.pi / 180,
                            threshold=6, minLineLength=20, maxLineGap=300)
    
    # Copy the section image to draw the lines on
    output = section_img.copy()
    x_coords_raw = []
    
    # If any lines are detected, process them
    if lines is not None:
        for x1, y1, x2, y2 in lines[:, 0]:
            angle = abs(np.degrees(np.arctan2(y2 - y1, x2 - x1)))
            if angle > 85:  # near vertical
                cv2.line(output, (x1, y1), (x2, y2), (0, 255, 0), 2)
                x_avg = (x1 + x2) // 2
                x_coords_raw.append(x_avg)
    
    # Sort the x-coordinates and filter duplicates (close ones)
    x_coords_raw.sort()
    x_coords_filtered = []
    duplicate_threshold = 10  # pixel gap between unique lines
    columns = []
    
    for x in x_coords_raw:
        if not x_coords_filtered or abs(x - x_coords_filtered[-1]) > duplicate_threshold:
            x_coords_filtered.append(x)
    
    # Optionally, draw the filtered vertical lines on the image and print their positions
    for x in x_coords_filtered:
        cv2.line(output, (x, 0), (x, output.shape[0]), (0, 255, 0), 2)
        print(f"{section_name} - Vertical line at x = {x}")
        
        
    
    # Calculate column ranges (the space between consecutive vertical lines)
    # For example, if there are 6 vertical lines, there will be 5 columns.
    
    for i in range(len(x_coords_filtered) - 1):
        col_range = (x_coords_filtered[i], x_coords_filtered[i+1])
        columns.append(col_range)
        print(f"{section_name} - Column {i+1}: x range = {col_range}")
    
    return output, x_coords_filtered, columns

# Example usage:
if __name__ == "__main__":
    img = cv2.imread("scan2.jpg")
    resized = cv2.resize(img, (800, 1000))
    # Example section, adjust the slice as needed
    section = resized[222:352, 530:750]
    
    output_img, x_coords, columns = detect_vertical_lines(section, section_name="Section 1")
    
    cv2.imshow("Detected Vertical Lines", output_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
