import numpy as np
import screeninfo
import pyautogui
import cv2
import tesserocr


# 创建一个透明灰度
def create_masker(width: int, height: int):
    img = np.ones([height, width, 4], np.uint8)
    img[:, :, 3] = 50
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGRA)
    return img


# 指定区域截屏
def screen_shot(width: int, height: int, x=0, y=0):
    img = pyautogui.screenshot(region=[x, y, width, height])  # x,y,w,h
    img = cv2.cvtColor(np.asarray(img), cv2.COLOR_RGBA2BGRA)
    return img


# 指定区域进行模糊
def screen_blurry(img, width: int, height: int, x: int, y: int, rate: float):
    # 先判断是否是透明图
    aimg = img
    img_height, img_width, img_channels = img.shape
    if img_channels != 4:
        aimg = cv2.cvtColor(img, cv2.COLOR_RGB2BGRA)
    print(img_channels)

    return img


# 全屏显示图像
def img_show(img):
    window_name = 'screenshot'
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    cv2.imshow(window_name, img)
    cv2.waitKey()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    # 屏幕个数
    screen_id = 0
    is_color = False

    # get the size of the screen
    screen = screeninfo.get_monitors()[screen_id]
    width, height = screen.width, screen.height

    img_show(screen_shot(width, height))
