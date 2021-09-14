import cv2

from HandTrackingModule import DetectHand

cap = cv2.VideoCapture(0)
dh = DetectHand(detectionCon=0.8)

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    dh.detect_hand(img)
    handslist = dh.hand_position(img, draw=False)
    total_fingers = []
    if len(handslist) != 0:
        for lmlist in handslist:
            # Index finger
            if lmlist[8][2] < lmlist[6][2]:
                total_fingers.append(1)
            else:
                total_fingers.append(0)
            # Middle finger
            if lmlist[12][2] < lmlist[10][2]:
                total_fingers.append(1)
            else:
                total_fingers.append(0)
            # Ring finger
            if lmlist[16][2] < lmlist[14][2]:
                total_fingers.append(1)
            else:
                total_fingers.append(0)
            # Pinky finger
            if lmlist[20][2] < lmlist[18][2]:
                total_fingers.append(1)
            else:
                total_fingers.append(0)
            # thumb
            if (lmlist[3][1] < lmlist[4][1] and lmlist[17][1] < lmlist[4][1]) or (lmlist[3][1] > lmlist[4][1] and lmlist[17][1] > lmlist[4][1]):
                total_fingers.append(1)
            else:
                total_fingers.append(0)
            cv2.rectangle(img, (2, 2), (160, 100), (0, 255, 0), cv2.FILLED)
            cv2.putText(img, str(sum(total_fingers)), (2, 95), cv2.FONT_HERSHEY_PLAIN, 8, (255, 0, 0), 7)
    # print(sum(total_fingers))
    cv2.imshow('Capturing', img)
    cv2.waitKey(1)
