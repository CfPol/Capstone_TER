import cv2

# Load your image
img = cv2.imread("scan2.jpg")  # replace with your image name
resized = cv2.resize(img, (800, 1000))
if img is None:
    print("Image not found.")
    exit()

# Clone for drawing coordinates
display_img = resized.copy()

# Mouse callback function
def show_xy(event, x, y, flags, param):
    if event == cv2.EVENT_MOUSEMOVE:
        temp = display_img.copy()
        # Draw crosshair
        cv2.line(temp, (x, 0), (x, img.shape[0]), (0, 255, 0), 1)
        cv2.line(temp, (0, y), (img.shape[1], y), (0, 255, 0), 1)
        # Draw coordinates
        cv2.putText(temp, f"X: {x}, Y: {y}", (x+10, y-10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
        cv2.imshow("XY Tracker", temp)

cv2.imshow("XY Tracker", display_img)
cv2.setMouseCallback("XY Tracker", show_xy)

cv2.waitKey(0)
cv2.destroyAllWindows()
