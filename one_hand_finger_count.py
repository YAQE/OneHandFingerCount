import cv2
import mediapipe as mp


cap = cv2.VideoCapture(0)

mpHand = mp.solutions.hands

hands = mpHand.Hands()

mpDraw = mp.solutions.drawing_utils

tipIds = [4, 8, 12, 16, 20]

while True:
    
    success, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    results = hands.process(imgRGB)
    print(results.multi_hand_landmarks)
    
    lmList = []
    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            mpDraw.draw_landmarks(img, handLms, mpHand.HAND_CONNECTIONS)
            
            for id, lm in enumerate(handLms.landmark):
                h , w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmList.append([id, cx, cy])
                
            if len(lmList) != 0:
                
                fingers = []
                
                if lmList[tipIds[0]][1] < lmList[tipIds[1]][1]:
                    #basparmak
                    if lmList[tipIds[0]][1] < lmList[tipIds[0] - 1][1]:
                        fingers.append(1)
                    else:
                        fingers.append(0)
                else:
                    #basparmak
                    if lmList[tipIds[0]][1] > lmList[tipIds[0] - 1][1]:
                        fingers.append(1)
                    else:
                        fingers.append(0)
                    
                
                #basparmak
                # if lmList[tipIds[0]][1] < lmList[tipIds[0] - 1][1]:
                #     fingers.append(1)
                # else:
                #     fingers.append(0)
                
                #basparmak harici 4 parmak
                for id in range(1, 5):
                    
                    if lmList[tipIds[id]][2] <  lmList[tipIds[id] - 2][2]:
                        fingers.append(1)
                    else:
                        fingers.append(0)
                
                print(fingers)
            totalF = fingers.count(1)
            cv2.putText(img, str(totalF), (30,125), cv2.FONT_HERSHEY_PLAIN, 10, (255,0,0), 8)
            
            
    cv2.imshow("Finger Counter", img)
    cv2.waitKey(1)