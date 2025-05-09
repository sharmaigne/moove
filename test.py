import cv2
import requests
import numpy as np
import time
from datetime import datetime

url = "http://192.168.1.20:8080/shot.jpg"
save_interval = 6  # seconds
last_saved = time.time()

while True:
    try:
        img_resp = requests.get(url, timeout=5)
        img_arr = np.array(bytearray(img_resp.content), dtype=np.uint8)
        frame = cv2.imdecode(img_arr, -1)

        # cv2.imshow("Live Feed", frame)

        current_time = time.time()
        if current_time - last_saved > save_interval:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"images/birdcam_{timestamp}.jpg"
            cv2.imwrite(filename, frame)
            print(f"Saved {filename}")
            last_saved = current_time
        # if cv2.waitKey(1) & 0xFF == ord("q"):
        #     break
    except Exception as e:
        print(f"Error: {e}")
        time.sleep(1) # wait before retrying

# TEST WITH WEBCAM FIRST
# cap = cv2.VideoCapture(0)
# while True:
#     ret, frame = cap.read()
#     if not ret:
#         break
#     cv2.imshow('Webcam Feed', frame)
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# cap.release()
cv2.destroyAllWindows()
