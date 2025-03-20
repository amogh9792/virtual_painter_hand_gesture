import cv2
import numpy as np
from utils import fingers_up

class VirtualPainter:
    def __init__(self):
        self.colors = [(0, 0, 255), (255, 0, 0), (0, 255, 0)]  # Red, Blue, Green
        self.color_index = 0
        self.brush_color = self.colors[self.color_index]
        self.brush_thickness = 7
        self.eraser_thickness = 50
        self.canvas = None
        self.prev_point = None

    def draw(self, frame, lm_list):
        if not lm_list:
            self.prev_point = None
            return

        finger_state = fingers_up(lm_list)
        index_finger = lm_list[8][1], lm_list[8][2]  # Tip of index finger

        # Change color gesture: Index + Middle fingers up
        if finger_state == [0, 1, 1, 0, 0]:
            self.color_index = (self.color_index + 1) % len(self.colors)
            self.brush_color = self.colors[self.color_index]
            cv2.putText(frame, f"Color Changed", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, self.brush_color, 3)
            self.prev_point = None
            return

        # Eraser Mode: All fingers up
        if finger_state == [1, 1, 1, 1, 1]:
            cv2.putText(frame, "Eraser Mode", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 3)
            if self.prev_point:
                cv2.line(self.canvas, self.prev_point, index_finger, (255, 255, 255), self.eraser_thickness)
            self.prev_point = index_finger
            return

        # Brush Mode: Only Index or Index+Middle+Ring
        if finger_state == [0, 1, 0, 0, 0] or finger_state == [0, 1, 1, 1, 0]:
            cv2.circle(frame, index_finger, 15, self.brush_color, cv2.FILLED)
            if self.prev_point:
                cv2.line(self.canvas, self.prev_point, index_finger, self.brush_color, self.brush_thickness)
            self.prev_point = index_finger
        else:
            self.prev_point = None

    def prepare_canvas(self, frame):
        if self.canvas is None:
            self.canvas = np.ones_like(frame) * 255  # White background
        return self.canvas
