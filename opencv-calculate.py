import cv2
import mediapipe as mp
import random
import time 


mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

TIP_IDS = [4, 8, 12, 16, 20]  


cap = cv2.VideoCapture(0)


num1 = random.randint(0, 2)
num2 = random.randint(0, 2)
equation = f"{num1} + {num2} = ?"  
correct_answer = num1 + num2  


with mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5) as hands:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("Failed to capture image. Exiting.")
            break

        
        height, width, _ = frame.shape
        
     
        roi_x1, roi_y1 = int(width * 0.2), int(height * 0.2)
        roi_x2, roi_y2 = int(width * 0.8), int(height * 0.8)
        
        
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False 
        results = hands.process(image) 
        
  
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        
        total_fingers = 0
        
       
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                
                wrist = hand_landmarks.landmark[0] 
                hand_x = int(wrist.x * width)
                hand_y = int(wrist.y * height)
                
              
                if roi_x1 < hand_x < roi_x2 and roi_y1 < hand_y < roi_y2:
                    
                    mp_drawing.draw_landmarks(
                        image, hand_landmarks, mp_hands.HAND_CONNECTIONS,
                        mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=4),
                        mp_drawing.DrawingSpec(color=(255, 0, 0), thickness=2))

                 
                    finger_states = [] 
                    for tip_id in TIP_IDS:
                        finger_tip = hand_landmarks.landmark[tip_id]
                        if tip_id == 4:  
                            finger_mcp = hand_landmarks.landmark[tip_id - 1]  
                            finger_states.append(finger_tip.x < finger_mcp.x)
                        else:  
                            finger_pip = hand_landmarks.landmark[tip_id - 2]  
                            finger_states.append(finger_tip.y < finger_pip.y)
                    
                    
                    total_fingers = sum(finger_states)
                    
                  
                   
        
        
        cv2.rectangle(image, (roi_x1, roi_y1), (roi_x2, roi_y2), (0, 255, 0), 2)
        
        
        cv2.putText(image, equation, (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        
        
        if total_fingers >= 0:
            cv2.putText(image, f"Fingers: {total_fingers}", (20, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            if total_fingers == 0:
                total_fingers = 0
                
            if total_fingers == correct_answer:
                
                equation = f"{num1} + {num2} = {correct_answer}"
                
                
                cv2.putText(image, "Correct!", (roi_x1, roi_y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)
                
              
                num1 = random.randint(0, 2)
                num2 = random.randint(0, 2)
                correct_answer = num1 + num2
                equation = f"{num1} + {num2} = ?"
            

        
        cv2.imshow("Hand Tracking and Finger Counting", image)
        
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


cap.release()
cv2.destroyAllWindows()
