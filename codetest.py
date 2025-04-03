import cv2
import numpy as np
import utils  

# Load and resize image
img = cv2.imread("scan2.jpg")
resized = cv2.resize(img, (800, 1000))
cropped = resized[222:881, 535:743] 
sections = {
    "Section 1": resized[222:352, 530:750],
    "Section 2": resized[365:513, 535:743],
    "Section 3": resized[525:688, 535:743],
    "Section 4": resized[703:870, 535:743],
}
copy = cropped.copy()



# Preprocessing
def detect_circles(section_img, section_name="Section"):
    gray = cv2.cvtColor(section_img, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (3, 3), 1)

    circles = cv2.HoughCircles(
        blurred, 
        cv2.HOUGH_GRADIENT, 
        dp=1.5, 
        param1=50,
        minDist=10,
        param2=30,
        minRadius=5,
        maxRadius=14
    )

    detected = []

    print(f"\n{section_name}:")
    if circles is not None:
        circles = np.uint16(np.around(circles))
        for x, y, r in circles[0, :]:
            cv2.circle(section_img, (x, y), r, (0, 255, 0), 2)
            cv2.circle(section_img, (x, y), 2, (0, 255, 0), 3)
            print(f"Circle - Center: ({x}, {y}), Radius: {r}")
            detected.append((x, y, r))
    else:
        print("No circles detected.")

    return section_img, detected

            



