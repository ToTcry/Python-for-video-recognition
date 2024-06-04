import numpy as np
import cv2

# 定义颜色阈值
# 红色区间优化，尝试减少误识别其他颜色的情况
lower_red = np.array([0, 100, 90])  # 减少饱和度和亮度的下限，以排除浅红或粉色调
higher_red = np.array([10, 255, 255])

# 绿色区间优化，确保在不同光照下都能准确识别
lower_green = np.array([35, 70, 70])  # 调整以适应更多绿色变体，特别是暗绿
higher_green = np.array([80, 255, 255])

# 黑色区间显著扩大
lower_black = np.array([0, 0, 0])  # 保持不变，因为已经是最低值
higher_black = np.array([100, 100, 50])  # 大幅增加，以识别更广泛的深色区域

# 注意：这些值仅为示例，实际应用中需要根据具体情况调整


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
