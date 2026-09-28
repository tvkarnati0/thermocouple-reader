import cv2

points = []  # will store all the (x, y) coordinates you click

def click_event(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:  # left mouse button clicked
        points.append((x, y))
        print(f"Point added: {x}, {y}")

frame = cv2.imread("Box1.png")

cv2.imshow("Click points, then press any key when done", frame)
cv2.setMouseCallback("Click points, then press any key when done", click_event)
cv2.waitKey(0)
cv2.destroyAllWindows()

print("All points:", points)

import numpy as np

img = cv2.imread("Box1.png")
mask = np.zeros(img.shape[:2], dtype=np.uint8)   # all-black image, same height/width as the crop

pts = np.array(points, dtype=np.int32)          # convert the list of clicks into a numpy array
cv2.fillPoly(mask, [pts], 255)                  # fill the inside of the polygon with white

cv2.imwrite("Box1_mask.png", mask)

mask = cv2.imread("Box1_mask.png", 0)   # the 0 means "load as grayscale"
_, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
thresh[mask == 0] = 255                 # anywhere the mask is black, paint white
cv2.imwrite("Box1_masked.png", thresh)