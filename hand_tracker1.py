import cv2
import mediapipe as mp
import pyautogui
import time

# --- NEW FUNCTION TO DETECT A CLOSED FIST ---
def is_fist_closed(hand_landmarks):
    """
    Checks if the fingertips are curled down past their middle knuckles.
    This is a simple but effective way to detect a fist.
    """
    # Get y-coordinates for the tips and primary knuckles of index and middle fingers
    tip_of_index = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y
    pip_of_index = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_PIP].y

    tip_of_middle = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y
    pip_of_middle = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_PIP].y

    # If the tip's y-coordinate is greater (lower on screen) than the knuckle's, the finger is curled.
    if tip_of_index > pip_of_index and tip_of_middle > pip_of_middle:
        return True
    return False

# --- SCRIPT SETUP ---
print("Starting in 3 seconds... Click on your game window now!")
time.sleep(3)

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

last_gesture = "NEUTRAL"
cap = cv2.VideoCapture(0)

# --- MAIN LOGIC ---
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
                
                # --- UPDATED GESTURE RECOGNITION LOGIC ---
                # First, check for a closed fist for the 'roll' action
                if is_fist_closed(hand_landmarks):
                    current_action = "down"
                else:
                    # If not a fist, use the index finger position for other actions
                    index_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
                    pixel_x = int(index_finger_tip.x * image_width)
                    pixel_y = int(index_finger_tip.y * image_height)

                    left_zone = image_width / 3
                    right_zone = image_width * 2 / 3
                    top_zone = image_height / 3

                    if pixel_x < left_zone:
                        current_action = "left"
                    elif pixel_x > right_zone:
                        current_action = "right"
                    elif pixel_y < top_zone:
                        current_action = "up"
                
                mp_drawing.draw_landmarks(
                    image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
        
        # --- CONTROL LOGIC (No changes here) ---
        if current_action != "NEUTRAL" and current_action != last_gesture:
            pyautogui.press(current_action)
            print(f"Action: Performed '{current_action}'")
            last_gesture = current_action
        
        if current_action == "NEUTRAL":
            last_gesture = "NEUTRAL"

        scale_percent = 120
        width = int(image.shape[1] * scale_percent / 100)
        height = int(image.shape[0] * scale_percent / 100)
        dim = (width, height)
        resized_image = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)

        cv2.imshow('Hand Gesture Controller', resized_image)

        if cv2.waitKey(5) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()