import cv2
import mediapipe as mp
import pyautogui
import time

# --- Parameters you can tune ---
SWIPE_THRESHOLD = 40  # How far your hand must move to trigger a swipe. Lower for more sensitivity.
ACTION_COOLDOWN = 0.3   # The minimum delay (in seconds) between repeatable actions.

# --- Global variables for gesture logic ---
last_action_time = 0
gesture_in_progress = False # A "lock" to prevent multiple actions from one swipe.
prev_x, prev_y = 0, 0     # Stores the previous position of the wrist.

def is_fist_closed(hand_landmarks):
    """
    A simple check to see if the fist is closed by comparing the vertical position
    of fingertips to the middle knuckles (PIP joints).
    """
    # Get y-coordinates for key landmarks of index and middle fingers
    tip_of_index = hand_landmarks.landmark[mp.solutions.hands.HandLandmark.INDEX_FINGER_TIP].y
    pip_of_index = hand_landmarks.landmark[mp.solutions.hands.HandLandmark.INDEX_FINGER_PIP].y

    tip_of_middle = hand_landmarks.landmark[mp.solutions.hands.HandLandmark.MIDDLE_FINGER_TIP].y
    pip_of_middle = hand_landmarks.landmark[mp.solutions.hands.HandLandmark.MIDDLE_FINGER_PIP].y

    # If the fingertip is lower on the screen (higher y-value) than the knuckle, the finger is curled.
    if tip_of_index > pip_of_index and tip_of_middle > pip_of_middle:
        return True
    return False

# --- Main Program ---
print("Starting in 3 seconds... Click on your game window now!")
time.sleep(3)

# Initialize MediaPipe and OpenCV
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
cap = cv2.VideoCapture(0)

with mp_hands.Hands(
    max_num_hands=1,  # Focus on one hand for stable control
    min_detection_confidence=0.7,
    min_tracking_confidence=0.5) as hands:

    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print("Ignoring empty camera frame.")
            continue

        # Get image dimensions and flip the image for a mirror view
        image_height, image_width, _ = image.shape
        image = cv2.flip(image, 1)

        # Process the image to find hands
        image.flags.writeable = False
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = hands.process(image_rgb)
        image.flags.writeable = True

        if results.multi_hand_landmarks:
            hand_landmarks = results.multi_hand_landmarks[0]
            action = None

            # --- GESTURE RECOGNITION LOGIC ---

            # 1. Check for a closed fist. This has the highest priority.
            if is_fist_closed(hand_landmarks):
                # Apply a cooldown for the fist gesture since it can be held
                if time.time() - last_action_time > ACTION_COOLDOWN:
                    pyautogui.press("down")
                    print("Action: Performed 'down' (Fist)")
                    last_action_time = time.time()
            else:
                # 2. If it's not a fist, check for swipes (up, left, right).
                wrist_landmark = hand_landmarks.landmark[mp.solutions.hands.HandLandmark.WRIST]
                current_x = int(wrist_landmark.x * image_width)
                current_y = int(wrist_landmark.y * image_height)

                # Calculate the change in position from the last frame
                delta_x = current_x - prev_x
                delta_y = current_y - prev_y

                # Check if the hand is moving fast enough to be a swipe
                if abs(delta_x) > SWIPE_THRESHOLD or abs(delta_y) > SWIPE_THRESHOLD:
                    # Only perform an action if a gesture is not already "in progress"
                    if not gesture_in_progress:
                        # Determine if the swipe is primarily horizontal or vertical
                        if abs(delta_x) > abs(delta_y):
                            action = "right" if delta_x > 0 else "left"
                        else:
                            # We only care about up-swipes for jumping
                            action = "up" if delta_y < 0 else None
                        
                        if action:
                            pyautogui.press(action)
                            print(f"Action: Performed '{action}' (Swipe)")
                            gesture_in_progress = True # Lock the gesture to prevent spam
                            last_action_time = time.time() # Start cooldown for the next gesture
                else:
                    # If the hand slows down, release the lock for the next gesture
                    gesture_in_progress = False

                # Update the previous position for the next frame
                prev_x, prev_y = current_x, current_y

            # Draw the hand landmarks on the image
            mp_drawing.draw_landmarks(
                image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
        
        # Resize the window to be larger
        scale_percent = 120
        width = int(image.shape[1] * scale_percent / 100)
        height = int(image.shape[0] * scale_percent / 100)
        dim = (width, height)
        resized_image = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)

        # Display the final image
        cv2.imshow('Hand Gesture Controller', resized_image)

        # Allow quitting by pressing 'q'
        if cv2.waitKey(5) & 0xFF == ord('q'):
            break

# Clean up
cap.release()
cv2.destroyAllWindows()