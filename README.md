# Mathematical-modeling-2021

### 1.分类

颜色：深灰 浅灰 灰 灰黑 黑

品质：细砂 粉砂 泥 煤 粉砂质泥 泥质粉砂

图片：jpg图片不全是岩土，需要裁剪

<font color=#FF0000> // To Do </font>

<font color=#FF0000> 进行分类 颜色用阈值判断？ 品质用图片纹理判断？ </font>

### 2.油性区域占比

#### 2.1油性区域面积计算

```python
img = cv2.imread(path2, 1)

# 转化为hsv图
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

# 设定黄绿颜色区间
low_hsv = np.array([26, 43, 46])
high_hsv = np.array([77, 255, 255])

# 二值化，白色部分为黄绿色
mask = cv2.inRange(hsv, lowerb=low_hsv, upperb=high_hsv)

# 求白色像素点数量
black = len(mask.astype(np.int8)[mask==255])
```

#### 2.2总岩土面积计算

##### 2.2.1 bmp图

对于bmp图片，可以直接使用**mask.size**表示总面积，效果比较好

##### 2.2.2 cv2自带的图片分割方法(已弃用)

对于jpg图片，需要剔除背景部分，不太好调

```python
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
```

但是在计算面积时，**adaptiveThreshold**的倒数第二个参数需要调控，很大影响到面积计算

以350图片为例：

| 参数 | 油性面积占比（%） |
| ---- | ----------------- |
| 11   | 17.43             |
| 21   | 8.10              |
| 31   | 5.93              |
| 51   | 3.28              |
| 101  | 2.36              |
| 201  | 2.27              |

原始图片-荧光照射-荧光提取

<img src=".\image\350-1.jpg" alt="350-1" style="zoom: 8%;" /><img src=".\image\350-2.jpg" alt="350-2" style="zoom: 8%;" /><img src=".\image\350-black.jpg" alt="350-black" style="zoom: 8%;" />

参数 11-21-31

<img src=".\image\350-11-17.43.jpg" alt="350-11" style="zoom: 8%;" /><img src=".\image\350-21-8.10.jpg" alt="350-21" style="zoom: 8%;" /><img src=".\image\350-31-5.93.jpg" alt="350-31" style="zoom: 8%;" />

参数 51-101-201

<img src=".\image\350-51-3.28.jpg" alt="350-51" style="zoom: 8%;" /><img src=".\image\350-101-2.36.jpg" alt="350-101" style="zoom: 8%;" /><img src=".\image\350-201-2.27.jpg" alt="350-31" style="zoom: 8%;" />

参数值影响到了面积计算，这种方法把图片的一些不相干区域例如图右侧的水迹计算在内，右上角的痕迹有可能计算在内

##### 2.2.3 无监督学习方法

按照https://github.com/Yonv1943/Unsupervised-Segmentation/tree/master修改后使用，详情见**image_segmentation**文件，由于运行时间过长，添加了图片下采样操作，同时没有使用大训练迭代次数，有小概率会跑崩

下采样图和分割结果如下图所示，取分割后中心颜色区域为矿土面积，表现效果目前最好：

<img src=".\image\350-4.jpg" alt="350-4" style="zoom: 200%;" /><img src=".\image\350-5.jpg" alt="350-5" style="zoom: 200%;" />

#### 2.3代码运行

图片放在脚本同级文件夹

```shell
python question2.py 350
```



