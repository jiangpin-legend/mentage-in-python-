import os
import sys
sys.path.append(r'c:\users\ljp\anaconda3\lib\site-packages')
import requests
from bs4 import BeautifulSoup
import urllib.request


#设置下载目录
query = 'Frozen2'  # 名字可以随便换
path ='D:/mentage'  # 当前路径，可以替换成别的路径
# path = 'C:/Users/ASUS/Desktop/测试'
picpath = path + "/" + query  # 设置的图片目录
print(picpath)  # 输出设置的图片目录
if not os.path.isdir(picpath):  # 如果图片目录未创建则创建一个
    os.mkdir(picpath)


# 依照其规律遍历海报网站中的每一页
def get_posters():
    picture_list = []
    for i in range(0,490,30):#第一页为0，最后一页为240
      url="https://movie.douban.com/subject/25887288/photos?type=S&start=%s&sortby=like&size=a&subtype=a" %str(i)    
      data = opener.open(url).read()
      content = BeautifulSoup(data, "html.parser")
      chekc_point = content.find('span', attrs={'class': 'next'}).find('a')
      if chekc_point != None:
            data = content.find_all('div', attrs={'class': 'cover'})
            for k in data:
                plist = k.find('img')['src']
                picture_list.append(plist)
      else:
            break
    
    return  picture_list
    
#用于下载图片
def download(src, id):
    dir = picpath + '/' + str(id) + '.jpg'
    try:
        pic = opener.open(src).read()
    except requests.exceptions.ConnectionError:
        # print 'error, %d 当前图片无法下载', %id
        print('图片无法下载')
    fp = open(dir, 'ab+')
    fp.write(pic)
    fp.close()

      
#设置浏览器头
headers = ("User_Agent","Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:72.0) Gecko/20100101 Firefox/72.0")
opener = urllib.request.build_opener()
opener.addheaders =[headers]




p_list = get_posters()
total = len(p_list)

i = 0
for each_p in p_list:
    i = i+1
    download(each_p,i)
    print(i,'/',total)
    
    
