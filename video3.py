import numpy as np
import cv2
import os

def play_video(video_path):
    # 检查视频文件是否存在
    if not os.path.isfile(video_path):
        print(f"Error: Video file '{video_path}' does not exist.")
        return

    try:
        cap = cv2.VideoCapture(video_path)

        # 检查视频是否能成功打开
        if not cap.isOpened():
            print(f"Error: Unable to open video file '{video_path}'.")
            return

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
            cv2.imshow('image', frame)

            # 检测窗口是否仍然存在，若窗口已关闭则退出循环
            if cv2.getWindowProperty('image', cv2.WND_PROP_VISIBLE) < 1:
                break

            k = cv2.waitKey(20)
            # q键退出
            if (k & 0xff == ord('q')):
                break

    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        # 确保释放资源和关闭窗口
        if 'cap' in locals() or 'cap' in globals():
            cap.release()
        cv2.destroyAllWindows()

# 调用示例，传入视频文件的路径
play_video('D:/English Word/Pycharm/type/pythonProject2/video/video.mp4')
