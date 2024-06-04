import numpy as np
import cv2

# 定义颜色阈值
lower_red = np.array([200, 150, 250])  # 红色阈值下界
higher_red = np.array([255, 200, 200])  # 红色阈值上界

lower_green = np.array([150, 200, 150])  # 绿色阈值下界
higher_green = np.array([200, 255, 200])  # 绿色阈值上界

lower_blue = np.array([150, 150, 200])  # 绿色阈值下界
higher_blue = np.array([200, 200, 255])  # 绿色阈值上界

lower_black = np.array([0, 0, 0])  # 黑色阈值下界
higher_black = np.array([70, 70, 70])  # 黑色阈值上界

# 定义字体
font = cv2.FONT_HERSHEY_SIMPLEX

def process_color(frame, lower_color, higher_color, color_name):
    img_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(img_hsv, lower_color, higher_color)
    mask = cv2.medianBlur(mask, 7)

    cnts, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    for cnt in cnts:
        x, y, w, h = cv2.boundingRect(cnt)
        cv2.rectangle(frame, (x, y - 20), (x + w, y + h), (0, 0, 255), 2)
        cv2.putText(frame, color_name, (x, y - 20), font, 0.7, (0, 0, 255), 2)

try:
    cap = cv2.VideoCapture(0)  # 打开电脑内置摄像头

    if cap.isOpened():
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            process_color(frame, lower_red, higher_red, 'Red')
            process_color(frame, lower_green, higher_green, 'Green')
            process_color(frame, lower_black, higher_black, 'Black')

            cv2.imshow('frame', frame)
            key = cv2.waitKey(20) & 0xFF

            if key == 27:  # 按Esc键退出
                break

except Exception as e:
    print(f"Error occurred: {e}")

finally:
    if cap.isOpened():
        cap.release()
    cv2.destroyAllWindows()
