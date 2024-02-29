import cv2
import mediapipe as mp
import numpy as np
import poseDetector as pm

cap = cv2.VideoCapture('./demo.mp4')
ret, img = cap.read()
H, W, _ = img.shape
out = cv2.VideoWriter('./out.mp4', cv2.VideoWriter_fourcc(*'mpv4'), int(cap.get(cv2.CAP_PROP_FPS)), (W, H))

detector = pm.poseDetector()
count = 0
direction = 0
form = 0


while cap.isOpened():
    #ret, img = cap.read() #640 x 480
    
    img = detector.findPose(img, False)
    lmList = detector.findPosition(img, False)
    # print(lmList)
    if len(lmList) != 0:
        elbow = detector.findAngle(img, 12, 14, 16)
        
        #Percentage of success of pushup
        per = np.interp(elbow, (90, 160), (0, 100))
        
        #Bar to show Pushup progress
        bar = np.interp(elbow, (90, 160), (380, 50))

        #Check to ensure right form before starting the program
        if elbow > 160:
            form = 1
    
        #Check for full range of motion for the pushup
        if form == 1:
            if per == 0:
                if elbow <= 90:
                    feedback = "Up"
                    if direction == 0:
                        count += 0.5
                        direction = 1
                    
            if per == 100:
                if elbow > 160:
                    feedback = "Down"
                    if direction == 1:
                        count += 0.5
                        direction = 0

        #Pushup counter
        cv2.rectangle(img, (70, 40), (250, 90), (0, 255, 0), cv2.FILLED)
        cv2.putText(img, 'Rep: '+ str(int(count)), (80, 80), cv2.FONT_HERSHEY_PLAIN, 3,
                    (0, 0, 0), 3)

        
    cv2.imshow('Pushup counter', img)
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break
        
    out.write(img)
    ret, img = cap.read()

cap.release()
out.release()
cv2.destroyAllWindows()