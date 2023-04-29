# -*- coding: utf-8 -*-

import os
import threading #导入threading
import time

from PIL import Image
from PIL import ImageChops

def stop():
    n = 1
    while n == 1:
        print("开始暂停15秒---------------")
        num = 15
        while num > 0:
            time.sleep(1)
            # print(num)
            num -= 1

        screenshot() # 截图

        # isSame = compare_image("./screenshot.png", "./screenshot1.png")

        s = similer("./screenshot.png", "./screenshot1.png") # 比较相似度

        if int(s) > 95:
            print("已经停了，按下手机")
            os.system("adb shell input tap 950 570")
            # os.system("adb shell input tap 25 1000")   
        else:
         print("视频正在播放，继续 。。。。。。")


def compare_image(origin_location, new_location):

    origin_image = Image.open(origin_location)
    origin = origin_image.crop((1,1,120,120)).convert("L")

    new_image = Image.open(new_location)
    new = new_image.crop((1,1,120,120)).convert("L")

    origin.save("./1111111.png")
    new.save("./2222222.png")

    result = ImageChops.difference(origin_image, new_image)

    # if result.getbbox() is None:
    if result == "100":
        print('两张图片相同')
        return True
    else:
        print('两张图片不同')
        return False

# compare_image()

def screenshot():
   #  os.system("adb shell input tap 500 500")
    time.sleep(1)
    print("开始截取图片")
    os.system('adb shell screencap -p /sdcard/screenshot1.png')
    os.system('adb pull /sdcard/screenshot1.png .')

def getGray(image_file):
   tmpls=[]
   for h in range(0,  image_file.size[1]):#h
      for w in range(0, image_file.size[0]):#w
         tmpls.append( image_file.getpixel((w,h))  )
          
   return tmpls
 
def getAvg(ls):#获取平均灰度值
   return sum(ls)/len(ls)
 
def getMH(a,b):#比较100个字符有几个字符相同
   dist = 0;
   for i in range(0,len(a)):
      if a[i]==b[i]:
         dist=dist+1
   return dist
 
def getImgHash(image_file):
   # image_file = Image.open(fne) # 打开
   image_file=image_file.resize((12, 12))#重置图片大小我12px X 12px
   image_file=image_file.convert("L")#转256灰度图
   Grayls=getGray(image_file)#灰度集合
   avg=getAvg(Grayls)#灰度平均值
   bitls=''#接收获取0或1
   #除去变宽1px遍历像素
   for h in range(1,  image_file.size[1]-1):#h
      for w in range(1, image_file.size[0]-1):#w
         if image_file.getpixel((w,h))>=avg:#像素的值比较平均值 大于记为1 小于记为0
            bitls=bitls+'1'
         else:
            bitls=bitls+'0'
   return bitls
'''         
   m2 = hashlib.md5()   
   m2.update(bitls)
   print m2.hexdigest(),bitls
   return m2.hexdigest()
'''

def similer(origin_location, new_location):

   #  origin_image = Image.open(origin_location)
   #  origin = origin_image.crop((480,900,600,1020))
   #  origin.save('origin.png', 'png')

    origin = Image.open('origin.png')

    new_image = Image.open(new_location)
    new = new_image.crop((480,900,600,1020))

    a = getImgHash(origin)
    b = getImgHash(new)
    compare=getMH(a, b)
    print(u'相似度' + str(compare)+"%")
    return str(compare)

if __name__ == '__main__':
    stop()
   # s = similer("./screenshot.png", "./screenshot1.png")




