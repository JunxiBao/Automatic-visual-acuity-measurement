import cv2
import mediapipe as mp
import numpy as np

def get_finger_direction(landmarks, image_shape):
    """计算食指指向的方向"""
    h, w, _ = image_shape
    index_finger_tip = np.array([landmarks[8].x * w, landmarks[8].y * h])
    index_finger_mcp = np.array([landmarks[5].x * w, landmarks[5].y * h])

    direction = index_finger_tip - index_finger_mcp
    angle = np.arctan2(-direction[1], direction[0]) * 180 / np.pi

    if -45 <= angle < 45:
        return "Right"
    elif 45 <= angle < 135:
        return "Up"
    elif -135 <= angle < -45:
        return "Down"
    else:
        return "Left"

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5)
mp_draw = mp.solutions.drawing_utils

# 替换成你自己的图片路径
image_path = '../data/hand.png'
image = cv2.imread(image_path)
image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
results = hands.process(image_rgb)

if results.multi_hand_landmarks:
    for hand_landmarks in results.multi_hand_landmarks:
        direction = get_finger_direction(hand_landmarks.landmark, image.shape)
        cv2.putText(image, f"Direction: {direction}", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        mp_draw.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

# 显示处理后的图片
cv2.imwrite('../data/hand_result.png', image)
