import cv2

cap=cv2.VideoCapture("C:/Users/tarin/thermocouple-reader/videos/5_per_Trehalose.MOV") #direct to path of the video

#establish fps
fps=cap.get(cv2.CAP_PROP_FPS)
print("FPS:", fps)

#cycle through each and all frames
while True: 
    success, frame = cap.read()
    if not success:
        break #end of the video
    print(frame.shape) #dimensions of array

cap.release()