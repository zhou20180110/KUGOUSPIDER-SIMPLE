import requests
import time
import os
from selenium import webdriver
from bs4 import BeautifulSoup
headers={
    'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36 Edg/87.0.664.60'
}
url = input('请输入拉取的url')
res = requests.get(url,headers=headers)
print('正在解析……')
time.sleep(1)
json = res.text
json =json.replace('callback123(','')
json =json[:len(json)-2]
json = eval(json)
list = []
for i in json['data']['lists']:
    print('名：'+i['FileName'])
    print('歌曲名:'+i['SongName'])
    print('歌手:'+i['SingerName'])
    try:
        print('专辑《'+i['AlbumName']+'》')
    except:
        pass
    if i['AlbumName']!='':
        url = 'https://www.kugou.com/song/#hash='+i['FileHash']+'&album_id='+i['AlbumID']
    else:
        url = 'https://www.kugou.com/song/#hash='+i['FileHash']
    print('url:'+url)
    print('\n\n')
    list.append([i['FileName'],url])

a = input('你要下载其中的歌吗？T/F')
if a=='T':
    for i in range(len(list)):
        list[i][0]=list[i][0].replace('<em>','')
        list[i][0]=list[i][0].replace('<\/em>','')
        list[i][0]=list[i][0].replace('\\','')
        list[i][0]=list[i][0].replace('/','')
        a = input(list[i][0]+'    T/F')
        list[i].append(a)
    print('请您离开，即将开始自动下载')
    time.sleep(1)
    driver = webdriver.Chrome()
    for i in range(len(list)):
        if(list[i][2]=='T'):
            driver.get(list[i][1])
            soup  = BeautifulSoup(driver.page_source,'html.parser')
            idd = soup.find(id='myAudio')
            list[i].append(idd['src'])
    driver.close()
    a = input('请输入根目录保存文件夹名')
    dir = 'PY\\酷狗实操\\'+a
    print('开始保存')
    try:
        os.makedirs('PY\\酷狗实操\\'+a)
    except:
        pass
    for i in range(len(list)):
        if list[i][2]=='T':
            r = requests.get(list[i][3])
            with open(dir+'\\'+list[i][0]+'.mp3','wb') as file:
                file.write(r.content)