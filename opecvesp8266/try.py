import cv2
import mediapipe as mp
import random
import time
from co import send 

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

TIP_IDS = [4, 8, 12, 16, 20]

cap = cv2.VideoCapture(0)


num1 = random.randint(0, 2)
num2 = random.randint(0, 2)
equation = f"{num1} + {num2} = ?"
correct_answer = num1 + num2


button_x, button_y = 50, 200
button_width, button_height = 200, 100
button_pressed = False

with mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5) as hands:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("Failed to capture")
            break

        height, width, _ = frame.shape

        roi_x1, roi_y1 = int(width * 0.5), int(height * 0.5)
        roi_x2, roi_y2 = int(width), int(height)

        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        results = hands.process(image)

        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        total_fingers = 0

        # Draw button
        button_color = (0, 255, 0) if button_pressed else (255, 0, 0)
        cv2.rectangle(image, (button_x, button_y),
                      (button_x + button_width, button_y + button_height), button_color, -1)
        cv2.putText(image, "choose Eq", (button_x + 20, button_y + 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(
                    image, hand_landmarks, mp_hands.HAND_CONNECTIONS,
                    mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=4),
                    mp_drawing.DrawingSpec(color=(255, 0, 0), thickness=2))

                hand_x = hand_landmarks.landmark[0].x * width
                hand_y = hand_landmarks.landmark[0].y * height
                if roi_x1 < hand_x < roi_x2 and roi_y1 < hand_y < roi_y2:
                    finger_states = []
                    for tip_id in TIP_IDS:
                        finger_tip = hand_landmarks.landmark[tip_id]
                        if tip_id == 4:  # Thumb
                            finger_mcp = hand_landmarks.landmark[tip_id - 1]
                            finger_states.append(finger_tip.x < finger_mcp.x)
                        else:  # Other fingers
                            finger_pip = hand_landmarks.landmark[tip_id - 2]
                            finger_states.append(finger_tip.y < finger_pip.y)

                    total_fingers = sum(finger_states)

                fingertip_x = int(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x * width)
                fingertip_y = int(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y * height)

                cv2.circle(image, (fingertip_x, fingertip_y), 10, (255, 0, 0), -1)
                if (button_x <= fingertip_x <= button_x + button_width and
                        button_y <= fingertip_y <= button_y + button_height):
                    button_pressed = True

        if button_pressed:
            send('0')
            while True:
                num1 = random.randint(0, 2)
                num2 = random.randint(0, 2)
                if not (num1 == 0 and num2 == 0):  # Avoid 0 + 0
                    break
            correct_answer = num1 + num2
            equation = f"{num1} + {num2} = ?"
            button_pressed = False

        # Draw the ROI and equation
        cv2.rectangle(image, (roi_x1, roi_y1), (roi_x2, roi_y2), (0, 255, 0), 2)
        cv2.putText(image, equation, (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        if total_fingers >= 0:
            cv2.putText(image, f"Fingers: {total_fingers}", (20, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            if total_fingers == correct_answer:
                cv2.putText(image, "Correct!", (20, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)
                send('1')

        # Show the image
        cv2.imshow("Hand Tracking and Finger Counting", image)

        # Break loop on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()

