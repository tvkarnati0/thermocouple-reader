import cv2

cap = cv2.VideoCapture("C:/Users/tarin/thermocouple-reader/videos/5_per_Trehalose.MOV")

# establish fps
fps = cap.get(cv2.CAP_PROP_FPS)
print("FPS:", fps)

# read first frame
success, frame = cap.read()
cap.release()

if not success:
    print("Couldn't read a frame")
else:
    print(frame.shape)  # dimensions and color of image

    # Use selectROI to pick the box interactively
    x, y, w, h = cv2.selectROI("Select region", frame)
    cv2.destroyWindow("Select region") #press any button
    print(x, y, w, h)

    # Now crop using those coordinates
    crop = frame[y:y+h, x:x+w]
    cv2.imwrite("crop_test.png", crop)