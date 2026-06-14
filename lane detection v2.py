import cv2
import numpy as np

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

print("--- STARTING HIGH-PRECISION STREAM (Press 'q' to stop) ---")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    height, width, _ = frame.shape
    camera_center = width // 2

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lower_white = np.array([0, 0, 195])
    upper_white = np.array([180, 45, 255])
    white_mask = cv2.inRange(hsv, lower_white, upper_white)

    kernel_clean = np.ones((3, 3), np.uint8)
    kernel_glue = np.ones((11, 11), np.uint8)

    opened_mask = cv2.morphologyEx(white_mask, cv2.MORPH_OPEN, kernel_clean)
    closed_mask = cv2.morphologyEx(opened_mask, cv2.MORPH_CLOSE, kernel_glue)
    final_mask = cv2.dilate(closed_mask, kernel_clean, iterations=1)

    contours, _ = cv2.findContours(
        final_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )

    left_line_x = []
    right_line_x = []

    for contour in contours:
        area = cv2.contourArea(contour)
        if 4000 < area < 250000:
            perimeter = cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, 0.02 * perimeter, True)

            rect = cv2.minAreaRect(approx)
            box = cv2.boxPoints(rect)
            box = np.int32(box)

            M = cv2.moments(box)
            if M["m00"] != 0:
                cx = int(M["m10"] / M["m00"])

                cv2.drawContours(frame, [box], 0, (0, 255, 0), 3)

                if cx < camera_center:
                    left_line_x.append(cx)
                else:
                    right_line_x.append(cx)

    pid_error = 0
    target_x = camera_center

    if left_line_x and right_line_x:
        avg_left = int(np.mean(left_line_x))
        avg_right = int(np.mean(right_line_x))
        target_x = (avg_left + avg_right) // 2
        pid_error = target_x - camera_center

    elif left_line_x and not right_line_x:
        avg_left = int(np.mean(left_line_x))
        target_x = avg_left + int(width * 0.23)
        pid_error = target_x - camera_center

    elif right_line_x and not left_line_x:
        avg_right = int(np.mean(right_line_x))
        target_x = avg_right - int(width * 0.23)
        pid_error = target_x - camera_center

    print(f"Current PID Error: {pid_error}")

    danger_zone_pixels = int(width * 0.20)
    max_safe_deviation = camera_center - danger_zone_pixels

    cv2.line(
        frame, (camera_center, 0), (camera_center, height), (255, 0, 0), 2
    )
    cv2.circle(frame, (target_x, int(height * 0.7)), 8, (255, 255, 0), -1)

    if abs(pid_error) > max_safe_deviation:
        status_text = f"PID_ERROR:{pid_error} [CRITICAL]"
        text_color = (0, 0, 255)
    else:
        status_text = f"PID_ERROR:{pid_error}"
        text_color = (0, 255, 255)

    cv2.putText(
        frame,
        status_text,
        (20, 50),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        text_color,
        2,
    )

    cv2.imshow("Object Tracker", frame)
    cv2.imshow("Mask Diagnostic Feed", final_mask)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
print("--- STREAM TERMINATED ---")