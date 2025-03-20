import os
import cv2
import numpy as np
import mediapipe as mp

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=2, min_detection_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (0, 0, 0)]  # Blue, Green, Red, Eraser (Black)
color_index = 0
brush_thickness = 7
eraser_thickness = 50

cap = cv2.VideoCapture(0)
cv2.namedWindow('Virtual Painter', cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty('Virtual Painter', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

canvas = None
mode = 'Draw'
prev_x, prev_y = None, None  # For smooth drawing

def fingers_up(hand_landmarks):
    finger_tips = [8, 12, 16, 20]
    fingers = []

    # Thumb
    fingers.append(1 if hand_landmarks.landmark[4].x < hand_landmarks.landmark[3].x else 0)

    for tip in finger_tips:
        fingers.append(1 if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[tip - 2].y else 0)

    return fingers

while True:
    success, frame = cap.read()
    if not success:
        break
    frame = cv2.flip(frame, 1)

    # Initialize whiteboard if not done
    if canvas is None:
        canvas = np.ones_like(frame) * 255  # White background canvas

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks, handedness in zip(results.multi_hand_landmarks, results.multi_handedness):
            label = handedness.classification[0].label  # 'Left' or 'Right'
            if label != 'Right':
                continue  # Only Right hand controls

            lm_list = []
            for id, lm in enumerate(hand_landmarks.landmark):
                h, w, _ = frame.shape
                lm_list.append((int(lm.x * w), int(lm.y * h)))

            if not lm_list:
                continue

            fingers = fingers_up(hand_landmarks)

            # Drawing logic with smooth line
            if fingers[1] == 1 and fingers[2] == 0:  # Index finger up -> Draw
                mode = 'Draw'
                x, y = lm_list[8]
                if prev_x is None or prev_y is None:
                    prev_x, prev_y = x, y
                cv2.line(canvas, (prev_x, prev_y), (x, y), colors[color_index], brush_thickness)
                prev_x, prev_y = x, y

            # Color Change: Index and Middle finger up
            elif fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 0:
                mode = 'Color Change'
                color_index = (color_index + 1) % len(colors)
                prev_x, prev_y = None, None
                cv2.putText(frame, 'Color Changed', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, colors[color_index], 3)

            # Thick Brush Mode
            elif fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 1:
                mode = 'Thick Brush'
                x, y = lm_list[8]
                if prev_x is None or prev_y is None:
                    prev_x, prev_y = x, y
                cv2.line(canvas, (prev_x, prev_y), (x, y), colors[color_index], brush_thickness + 10)
                prev_x, prev_y = x, y

            # Eraser: All fingers down
            elif fingers.count(1) == 0:
                mode = 'Eraser'
                x, y = lm_list[8]
                if prev_x is None or prev_y is None:
                    prev_x, prev_y = x, y
                cv2.line(canvas, (prev_x, prev_y), (x, y), (255, 255, 255), eraser_thickness)
                prev_x, prev_y = x, y

            else:
                prev_x, prev_y = None, None

            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    else:
        prev_x, prev_y = None, None  # Reset if no hand detected

    # Combine Canvas on whiteboard
    output = cv2.addWeighted(frame, 0.3, canvas, 0.7, 0)
    cv2.putText(output, f'Mode: {mode}', (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 0), 3)
    cv2.imshow("Virtual Painter", output)

    key = cv2.waitKey(1)
    if key == ord('q'):
        break
    elif key == ord('c'):
        canvas = np.ones_like(frame) * 255  # Clear canvas
    elif key == ord('s'):  # Press 's' to save the drawing
        save_path = '../assets/saved_drawings'
        os.makedirs(save_path, exist_ok=True)
        import datetime
        filename = datetime.datetime.now().strftime("%Y%m%d_%H%M%S") + '.png'
        full_path = os.path.join(save_path, filename)
        cv2.imwrite(full_path, canvas)
        print(f"Drawing saved at: {full_path}")

cap.release()
cv2.destroyAllWindows()
