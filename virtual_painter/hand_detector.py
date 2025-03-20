import cv2
import mediapipe as mp

class HandDetector:
    def __init__(self, maxHands=1):
        self.hands = mp.solutions.hands.Hands(max_num_hands=maxHands)
        self.mpDraw = mp.solutions.drawing_utils

    def find_hand(self, frame):
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(rgb)
        lm_list = []
        if results.multi_hand_landmarks:
            for hand in results.multi_hand_landmarks:
                for id, lm in enumerate(hand.landmark):
                    h, w, c = frame.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    lm_list.append((id, cx, cy))
                self.mpDraw.draw_landmarks(frame, hand, mp.solutions.hands.HAND_CONNECTIONS)
        return lm_list
