import cv2
import mediapipe as mp
import pyautogui
import time 

# Initialize utilities
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

# State variable to track the last gesture
last_gesture = "NEUTRAL"

# Start webcam capture
cap = cv2.VideoCapture(0)

with mp_hands.Hands(
    min_detection_confidence=0.7,
    min_tracking_confidence=0.5) as hands:

    while cap.isOpened():
        success, image = cap.read()
        if not success:
            continue

        image_height, image_width, _ = image.shape
        image = cv2.flip(image, 1)
        image.flags.writeable = False
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = hands.process(image_rgb)
        image.flags.writeable = True

        current_action = "NEUTRAL"

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                index_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
                pixel_x = int(index_finger_tip.x * image_width)
                pixel_y = int(index_finger_tip.y * image_height)
                
                # Define zones
                left_zone = image_width / 3
                right_zone = image_width * 2 / 3
                top_zone = image_height / 3
                bottom_zone = image_height * 2 / 3

                # Check for gestures
                if pixel_x < left_zone:
                    current_action = "left"
                elif pixel_x > right_zone:
                    current_action = "right"
                elif pixel_y < top_zone:
                    current_action = "up"
                elif pixel_y > bottom_zone:
                    current_action = "down"

                mp_drawing.draw_landmarks(
                    image,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS)
        
        # --- FINAL CONTROL LOGIC ---
        if current_action != "NEUTRAL" and current_action != last_gesture:
            pyautogui.press(current_action)
            print(f"Action: Pressed '{current_action}' key")
            last_gesture = current_action
        
        if current_action == "NEUTRAL":
            last_gesture = "NEUTRAL"

        # --- NEW: RESIZE THE FRAME TO BE 20% LARGER ---
        scale_percent = 120 # percent of original size
        width = int(image.shape[1] * scale_percent / 100)
        height = int(image.shape[0] * scale_percent / 100)
        dim = (width, height)
        
        # Resize image
        resized_image = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)

        # Display the resized image
        cv2.imshow('Hand Gesture Controller', resized_image)

        if cv2.waitKey(5) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()