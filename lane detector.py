import cv2
import numpy as np
import math

def canny_edge(image):
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blur, 50, 150)
    return edges

def region_of_interest(image):
    height = image.shape[0]
    polygons = np.array([
        [(100, height), (1180, height), (600, 400)]
    ])
    mask = np.zeros_like(image)
    cv2.fillPoly(mask, polygons, 255)
    masked_image = cv2.bitwise_and(image, mask)
    return masked_image

def display_lines(image, lines):
    line_image = np.zeros_like(image)
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line.reshape(4)
            cv2.line(line_image, (x1, y1), (x2, y2), (0, 255, 0), 10)
    return line_image

def main():
    SOURCE = 1
    cap = cv2.VideoCapture(SOURCE)

    if not cap.isOpened():
        return

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        edges = canny_edge(frame)
        cropped_edges = region_of_interest(edges)

        lines = cv2.HoughLinesP(
            cropped_edges,
            rho=2,
            theta=np.pi / 180,
            threshold=100,
            minLineLength=40,
            maxLineGap=5
        )

        line_image = display_lines(frame, lines)
        combo = cv2.addWeighted(frame, 0.8, line_image, 1, 1)

        cv2.imshow("Lane Detection", combo)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
