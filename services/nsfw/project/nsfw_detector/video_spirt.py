#! python

import os
import cv2


def save_img(img, addr, num):
    naddr = "%s/%d.jpg" % (addr, num)
    ret = cv2.imwrite(naddr, img)
    # print("ret :",ret)
    return ret


def video_to_image(srcFile, imageDir):
    #srcFile = "/tmp/mupgoayv3wqul9mzi7os.mp4"

    if not os.path.isdir(imageDir):
        os.mkdir(imageDir)

    videoCapture = cv2.VideoCapture(srcFile)

    # 总帧数(frames)
    frames = videoCapture.get(cv2.CAP_PROP_FRAME_COUNT)
    print('视频帧数' + str(frames))

    a = 1
    b = 2
    c = 3
    d = 4
    e = 5
    if frames >= 8:
        a = 1
        c = int(frames / 2)
        b = int(c / 2)
        d = c + b
        e = int(frames)

    isOK, frame = videoCapture.read()
    i = 0
    list = []
    while isOK:
        i = i + 1
        if i == a or i == b or i == c or i == d or i == e:
            if not save_img(frame, imageDir, i):
                print("error occur!")
                break
            else:
                print("load success item:", i)
                list.append(imageDir + '/' + str(i) + '.jpg')
        isOK, frame = videoCapture.read()
    print('图片抽取结果：', list)
    return list



# 将视频文件路径转化为标准的路径
# videoPath=videoPath.replace("\\","/").replace('"','').replace("'","").strip()
# # 视屏获取
# videoCapture=cv2.VideoCapture(videoPath)
# # 帧率(frames per second)
# fps = videoCapture.get(cv2.CAP_PROP_FPS)
# # 总帧数(frames)
# frames = videoCapture.get(cv2.CAP_PROP_FRAME_COUNT)

