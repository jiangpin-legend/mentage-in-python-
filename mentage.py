#coding = utf-8

#将安装的第三方库加入到文件阅读目录
import sys
sys.path.append(r'c:\users\ljp\anaconda3\lib\site-packages')

import os
import cv2
import collections
import numpy as np

#全局变量：文件路径
readPath = r"D:\mentage\Zootopia"
savePath = r"D:\mentage\New_Zootopia"

#下面两个变量为生成的图库的图片的大小*
#推荐值为16:9，实测效果较好值为4:3
SIZE_WIDTH_db=4
SIZE_HEIGHT_db=3


def Resize():
    #创建列表保存图片文件名字
    files = os.listdir(readPath)
    n = 0
    for file in files:
        n+=1
        imgPath=readPath+ "\\" + file#构造图片路径
        img=cv2.imread(imgPath)#读取图片到内存img变量
        img=cv2.resize(img,(100,100))#更改图片的大小
        # 更改之后写入文件，方便以后使用。否则你生成一张马赛克就要处理一次10万张图片
        cv2.imwrite(savePath+ "\\"+file,img)
        print(n)


def Rgb_List(path):
    readPath=path
    files=os.listdir(readPath)
    n=0
    s=''
    for file in files  :
        bgr = []
        n+=1
        imgPath = readPath + "\\" + file
        img=cv2.imread(imgPath)
        for i in range(100):
            for j in range(100):
                b=img[i,j,0]
                g=img[i,j,1]
                r=img[i,j,2]
                bgr.append((b,g,r))
#        a = input()
        most=collections.Counter(bgr).most_common(1)
        s += file
        s += ":"
        s += str(most[0][0]).replace("(","").replace(")","")
        s += "\n"
        print(n)
    f = open('Frozenfilename.txt','w')
    f.write(s)

    

 
def readIndex():
   
    fs = open(r"D:\mentage\zoofilename.txt","r")
    n=0
    dic=[]
    
    for line in fs.readlines():
        n+=1
        print('loading:No',n)
        temp=line.split(":")
        file=temp[0]
        bgr=temp[1].split(",")
        b=int(bgr[0])
        g=int(bgr[1])
        r=int(bgr[2])
        dic.append((file,(b,g,r)))
    return dic

def Cal_BGR(img):
    count = SIZE_HEIGHT_db*SIZE_WIDTH_db
    b=g=r=0
    for i in range(SIZE_HEIGHT_db):
            for j in range(SIZE_WIDTH_db):
                b+=img[i,j,0]
                g+=img[i,j,1]
                r+=img[i,j,2]
    BAvg=round(b/count, 0)
    GAvg=round(g/count, 0)
    RAvg=round(r/count, 0)
    return (BAvg, GAvg, RAvg)

def Deal_black(img,list,height,big):
    #处理坐标为 x= 0 这一行的坐标


    #处理 y = 0 这一列
    x1=SIZE_HEIGHT_db
    y1=0
    y2=y1+SIZE_WIDTH_db
    for x1 in range(height-SIZE_HEIGHT_db,0,-SIZE_HEIGHT_db): 
        x2=x1+SIZE_HEIGHT_db
       
        temp_img = img[x1:x2,y1:y2]

        #获取图像当前位置的BGR值
        bgr = Cal_BGR(temp_img)
        np.random.shuffle(list)#打乱索引文件
        
        is_found=1
        max = 60
        while(is_found):
            max = max + 10
            
            for item in list:
                imgb=item[1][0]
                imgg=item[1][1]
                imgr=item[1][2]#获取索引文件的RGB值
                
                distance=(imgb-bgr[0])**2+(imgg-bgr[1])**2+(imgr-bgr[2])**2#欧式距离
                if distance<max:
                    filepath=savePath+"\\"+str(item[0])#定位到具体的图片文件
                    is_found=0
                    if max<=60 :
                        num=num+1
                
                    break
        
        close_image=cv2.imread(filepath)#读取整个最相近的图片
        big[x1:x2,y1:y2]=cv2.resize(close_image,(SIZE_WIDTH_db,SIZE_HEIGHT_db))
    return big

def Mentage():
    print("生成图片中...")
    files = os.listdir(readPath)
    imgPath=readPath+ "\\" +files[-6]
    img=cv2.imread(imgPath)
    print(imgPath)
    cv2.imshow('whichbear',img)
    cv2.waitKey(0)
    
    s=np.shape(img)
    width = s[1]
    height = s[0]
    print(width,height)
    
    #计算需要的马赛克总数
    count_images=round((width * height)/(SIZE_WIDTH_db*SIZE_HEIGHT_db))

    big= np.zeros((s[0],s[1], 3), dtype=np.uint8)
    

    list=readIndex()#读取索引文件到变量中
    i = 0 
    num = 0

    #big=Deal_black(img,list,height,big)

    for x1 in range(height-SIZE_HEIGHT_db,0,-SIZE_HEIGHT_db):#遍历行和列
        for y1 in range(width-SIZE_WIDTH_db,0,-SIZE_WIDTH_db):
            i=i+1
            print(i,'/',count_images)
            
            
            x2=x1+SIZE_HEIGHT_db
            y2=y1+SIZE_WIDTH_db
            temp_img = img[x1:x2,y1:y2]

            #获取图像当前位置的BGR值
            bgr = Cal_BGR(temp_img)
            np.random.shuffle(list)#打乱索引文件
            
            is_found=1
            max = 60
            while(is_found):
                max = max + 10
                
                for item in list:
                    imgb=item[1][0]
                    imgg=item[1][1]
                    imgr=item[1][2]#获取索引文件的RGB值
                    
                    distance=(imgb-bgr[0])**2+(imgg-bgr[1])**2+(imgr-bgr[2])**2#欧式距离
                    if distance<max:
                        filepath=savePath+"\\"+str(item[0])#定位到具体的图片文件
                        is_found=0
                        if max<=60 :
                            num=num+1
                    
                        break
            
            close_image=cv2.imread(filepath)#读取整个最相近的图片
            big[x1:x2,y1:y2]=cv2.resize(close_image,(SIZE_WIDTH_db,SIZE_HEIGHT_db))

    print(num)
    #print(big)
    Path = readPath + '\\' + 'bigguitar'+'.img'
    cv2.imwrite(r"D:\mentage\happybirthdaysweeties.jpg",big)#输出大图到文件中

#main 
#Resize()
#Rgb_List(savePath)
Mentage()



