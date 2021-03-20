import cv2
import sys
import numpy as np
from image_segmentation import run

src = sys.argv[1]

if int(src) < 322:
    path1 = src + "-1.bmp"
    path2 = src + "-2.bmp"
else:
    path1 = src + "-1.jpg"
    path2 = src + "-2.jpg"

# 彩色读取
print(path2)
img = cv2.imread(path2, 1)

# 转化为hsv图
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

# 设定黄绿颜色区间
low_hsv = np.array([26, 43, 46])
high_hsv = np.array([77, 255, 255])

# 二值化，白色部分为黄绿色
mask = cv2.inRange(hsv, lowerb=low_hsv, upperb=high_hsv)
black = len(mask.astype(np.int8)[mask==255])

if int(src) < 322:
    area = mask.size
else:
    low_hsv = np.array([26, 43, 46])
    high_hsv = np.array([77, 255, 255])

    '''
    方法一
    # 二值化，剔除蓝色背景  //效果8太好
    low_hsv = np.array([100, 43, 46])
    high_hsv = np.array([124, 255, 255])
    mask = cv2.inRange(hsv, lowerb=low_hsv, upperb=high_hsv)
    area = len(mask.astype(np.int8)[mask==0])
    '''

    '''
    方法二 直接分块，参数不好调
    # 画轮廓，调调参数勉强能用
    mat_img = cv2.imread(path1)
    mat_img2 = cv2.imread(path1, cv2.CV_8UC1)
    dst = cv2.adaptiveThreshold(mat_img2, 210, cv2.BORDER_REPLICATE, cv2.THRESH_BINARY_INV, 31, 10)

    # 提取轮廓
    contours, h = cv2.findContours(dst, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # 标记轮廓
    cv2.drawContours(mat_img, contours, -1, (255, 0, 255), 3)

    # 计算轮廓面积
    area = 0
    for i in contours:
        area += cv2.contourArea(i)
    '''

    # 方法三 无监督的学习

    # 下采样四次 缩小图片减少开销
    src = cv2.imread(path1)
    image = cv2.pyrDown(src)
    image = cv2.pyrDown(image)
    image = cv2.pyrDown(image)
    image = cv2.pyrDown(image)

    # 求取分色图
    color_image = run(image)
    color = color_image[int(color_image.shape[0] / 2)][int(color_image.shape[1] / 2)]
    print("color is", color)
    area = 256*len(color_image.astype(np.int8)[color_image == color])
    cv2.imwrite('350-4.jpg', image)
    cv2.imwrite('350-5.jpg', color_image)
    #cv2.waitKey()
    #cv2.destroyAllWindows()


print("Oil-bearing area area is", black*100/area, "%")

#cv2.imshow('newimage', mask)
#cv2.waitKey()
#cv2.destroyAllWindows()