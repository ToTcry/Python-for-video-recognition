import numpy as np
import cv2
import os

# 构建相对路径，使用os.path.join拼接路径，确保跨平台兼容性
video_relative_path = "video.mp4"
video_path = os.path.join(os.path.dirname(__file__), 'video', video_relative_path)

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

    # 增加识别框大小的系数
    enlarge_factor = 10


    for cnt in cnts:  # 对于红色
        (x, y, w, h) = cv2.boundingRect(cnt)
        w_enlarged = int(w * enlarge_factor)  # 根据系数增大宽度
        h_enlarged = int(h * enlarge_factor)  # 根据系数增大高度
        x_center = x + w // 2
        y_center = y + h // 2
        cv2.rectangle(frame, (x_center - w_enlarged // 2, y_center - h_enlarged // 2),
                      (x_center + w_enlarged // 2, y_center + h_enlarged // 2), (0, 0, 255), 2)
        cv2.putText(frame, 'red', (x, y - 20), font, 0.7, (0, 0, 255), 2)

    # 类似地，对绿色和黑色的识别框也做同样的调整

try:
    cap = cv2.VideoCapture(video_path)

    if cap.isOpened():
        # 获取视频的宽度和高度
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        # 设定显示窗口的尺寸为视频尺寸的一定比例，以适应屏幕（这里以0.3为例，可根据实际情况调整）
        window_scale = 0.3
        cv2.namedWindow('image', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('image', int(width * window_scale), int(height * window_scale))

        while (cap.isOpened()):
            ret, frame = cap.read()
            # 如果读取帧失败，退出循环
            if not ret:
                break

            process_color(frame, lower_red, higher_red, 'Red')
            process_color(frame, lower_green, higher_green, 'Green')
            process_color(frame, lower_black, higher_black, 'Black')

            cv2.imshow('image', frame)  # 在窗口显示视频，一帧

            # q键退出
            k = cv2.waitKey(1)  # 视频播放的帧率
            if (k & 0xff == ord('q')):
                break

            # 按Esc键退出
            key = cv2.waitKey(1) & 0xFF
            if key == 27:
                break

            # 检测窗口是否仍然存在，若窗口已关闭则退出循环
            if cv2.getWindowProperty('image', cv2.WND_PROP_VISIBLE) < 1:
                break

    else:
        print(f"Error: Unable to open video file '{video_path}'.")

except Exception as e:
    print(f"Error occurred: {e}")

finally:
    if cap.isOpened():
        cap.release()
    cv2.destroyAllWindows()
