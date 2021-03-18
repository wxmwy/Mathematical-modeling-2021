import cv2
import sys
import numpy as np

src = sys.argv[1]

if int(src) < 322:
    path1 = src + "-1.bmp"
    path2 = src + "-2.bmp"
else:
    path1 = src + "-1.jpg"
    path2 = src + "-2.jpg"

# 彩色读取
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

    # 二值化，剔除蓝色背景  //效果8太好
    #low_hsv = np.array([100, 43, 46])
    #high_hsv = np.array([124, 255, 255])
    #mask = cv2.inRange(hsv, lowerb=low_hsv, upperb=high_hsv)
    #area = len(mask.astype(np.int8)[mask==0])


    # 画轮廓，调调参数勉强能用
    mat_img = cv2.imread(path1)
    mat_img2 = cv2.imread(path1, cv2.CV_8UC1)
    dst = cv2.adaptiveThreshold(mat_img2, 210, cv2.BORDER_REPLICATE, cv2.THRESH_BINARY_INV, 31, 10)
    #cv2.imshow('newimage', dst)
    #cv2.waitKey()
    #cv2.destroyAllWindows()
    # 提取轮廓
    contours, h = cv2.findContours(dst, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # 标记轮廓
    cv2.drawContours(mat_img, contours, -1, (255, 0, 255), 3)

    # 计算轮廓面积
    area = 0
    for i in contours:
        area += cv2.contourArea(i)
    #print("num is:", contours)
    #print("area is:", area)
    #cv2.imshow('newimage', mat_img)
    #cv2.waitKey()
    #cv2.destroyAllWindows()



print("Oil-bearing area area is", black/area*100, "%")

#cv2.imshow('newimage', mask)
#cv2.waitKey()
#cv2.destroyAllWindows()