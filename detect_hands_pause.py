__author__      = "Vinay Verma"
__copyright__   = "Copyright 2021, Vinay Verma"
__credits__     = ["Vinay Verma"]
__license__     = "MIT"
__version__     = "0.1.0"
__maintainer__  = "Vinay Verma"
__email__       = "vermavinay982@gmail.com"
__module_name__ = "[Note Maker]"

import cv2
import mediapipe as mp
import pyautogui 

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands
prev_hand=False

cap = cv2.VideoCapture(0)
with mp_hands.Hands(
    model_complexity=0,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as hands:
  while cap.isOpened():
    success, image = cap.read()
    if not success:
      print("Ignoring empty camera frame.")
      # If loading a video, use 'break' instead of 'continue'.
      continue

    # To improve performance, optionally mark the image as not writeable to
    # pass by reference.
    image.flags.writeable = False
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(image)

    # Draw the hand annotations on the image.
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    
    hand = False
    if results.multi_hand_landmarks:
      # TO HIDE THE DRAWINGS MADE ON HAND 
      for hand_landmarks in results.multi_hand_landmarks:
        mp_drawing.draw_landmarks(
            image,
            hand_landmarks,
            mp_hands.HAND_CONNECTIONS,
            mp_drawing_styles.get_default_hand_landmarks_style(),
            mp_drawing_styles.get_default_hand_connections_style())
      
      hand = True
      # print("Hands Visible")
      # print(hand_landmarks)
    else:
      # print("Not Visible")
      pass

    # TO DETECT THE CHANGE
    if prev_hand != hand:
      print("Pressed Space - Change")
      pyautogui.press('space')

    prev_hand = hand

    # Flip the image horizontally for a selfie-view display.
    # COMMENT 3 LINES BELOW TO HIDE WINDOW SHOWING YOUR FACE
    cv2.imshow('MediaPipe Hands', cv2.flip(image, 1))
    if cv2.waitKey(5) & 0xFF == 27:
      break

cap.release()
