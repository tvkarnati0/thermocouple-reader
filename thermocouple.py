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
    x1, y1, w1, h1 = cv2.selectROI("Select region", frame)
    cv2.destroyWindow("Select region") #press any button
    print("Box1 Coordinates: ", x1, y1, w1, h1)

    # Now crop using those coordinates
    crop = frame[y1:y1+h1, x1:x1+w1]
    cv2.imwrite("Box1.png", crop)

    x2, y2, w2, h2 = cv2.selectROI("Select region", frame)
    cv2.destroyWindow("Select region") #press any button
    print("Box2 Coordinates: ", x2, y2, w2, h2)
    
    # Now crop using those coordinates
    crop = frame[y2:y2+h2, x2:x2+w2]
    cv2.imwrite("Box2.png", crop)