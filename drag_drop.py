from HandTrackingModule import DetectHand
import cv2
import numpy as np


class DragRect:
    def __init__(self, rectCenter, size=[200, 200], color=(255, 0, 255)):
        self.rectCenter = rectCenter
        self.size = size
        self.color = color

    def drag(self, cursor1, cursor2):
        self.color = (0, 255, 0)
        self.distance, _ = ht.findDistance(cursor1, cursor2)
        if self.distance < 50:
            self.rectCenter = cursor1


rectlist = []
for i in range(5):
    rectlist.append(DragRect([250 * i + 150, 150]))

ht = DetectHand(detectionCon=0.85)
cap = cv2.VideoCapture(0)
while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    blk = np.zeros(img.shape, np.uint8)
    ht.detect_hand(img)
    handslist = ht.hand_position(img, draw=False)
    for rect in rectlist:
        cx, cy = rect.rectCenter
        w, h = rect.size
        top_left, bottom_right = (cx - w // 2, cy - h // 2), (cx + w // 2, cy + h // 2)
        if len(handslist) != 0:
            if len(handslist) == 1:
                hand1_cursor1 = handslist[0][8][1:]
                hand1_cursor2 = handslist[0][12][1:]
                if top_left[0] < hand1_cursor1[0] < bottom_right[0] and top_left[1] < hand1_cursor1[1] < bottom_right[1]:
                    rect.drag(hand1_cursor1, hand1_cursor2)
                else:
                    rect.color = (255, 0, 255)
            if len(handslist) == 2:
                hand1_cursor1, hand1_cursor2 = handslist[0][8][1:], handslist[0][12][1:]
                hand2_cursor1, hand2_cursor2 = handslist[1][8][1:], handslist[1][12][1:]
                if (top_left[0] < hand1_cursor1[0] < bottom_right[0] and top_left[1] < hand1_cursor1[1] < bottom_right[1]) or (top_left[0] < hand2_cursor1[0] < bottom_right[0] and top_left[1] < hand2_cursor1[1] < bottom_right[1]):
                    if top_left[0] < hand1_cursor1[0] < bottom_right[0] and top_left[1] < hand1_cursor1[1] <bottom_right[1]:
                        rect.drag(hand1_cursor1, hand1_cursor2)
                    if top_left[0] < hand2_cursor1[0] < bottom_right[0] and top_left[1] < hand2_cursor1[1] < bottom_right[1]:
                        rect.drag(hand2_cursor1, hand2_cursor2)
                else:
                    rect.color = (255, 0, 255)

        cv2.rectangle(blk, top_left, bottom_right, rect.color, cv2.FILLED)
    out = cv2.addWeighted(img, 1.0, blk, 0.5, 1)
    cv2.imshow('Capturing...', out)
    cv2.waitKey(1)
    
