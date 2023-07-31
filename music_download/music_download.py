import requests
from fake_useragent import UserAgent
# json 序列化模块
import os
import subprocess
from functools import partial

subprocess.Popen = partial(subprocess.Popen, encoding='utf-8')
# 导入Python中执行 js 代码的模块
import execjs


def get_download_url(sound_number):
    page_url = 'https://music.163.com/weapi/song/enhance/player/url/v1?csrf_token='

    # 打开JS 代码文件
    # 注意这里可能会报一个错误：文中出现了连‘gb18030’也无法编码的字符，可以使用‘ignore’属性进行忽略
    # UnicodeDecodeError: 'gbk' codec can't decode byte 0xbc in position 405: illegal multibyte sequence
    with open("music_download.js", encoding='gb18030', errors="ignore") as f:
        # 将JS 代码读出来
        jsCode = f.read()
    # 将读出来的JS代码交给 execjs 进行编译
    JS_sign_t = execjs.compile(jsCode)
    key = '{"ids":"[%s]","level":"standard","encodeType":"aac","csrf_token":""}' % sound_number
    # call() 运行代码中的xxx函数. 后续的参数是xxx的参数 # 后面的参数可留空
    encryptionParams = JS_sign_t.call('main', key)
    encText = encryptionParams[0]
    encSecKey = encryptionParams[1]

    # headers 伪装
    headers = {
        'User-Agent': UserAgent().random
    }

    params = {
        'params': encText,
        'encSecKey': encSecKey
    }
    session = requests.Session()

    response = session.post(url=page_url, headers=headers, params=params)
    data_json = response.json()

    # print(response.text)
    download_url = data_json['data'][0]['url']
    return download_url


def download_sound(download_url, sound_name):
    # 发起请求，获取到数据
    response = requests.get(download_url)
    # 转为二进制数据
    data = response.content
    # 文件操作，判断文件夹是否存在以及对歌曲的命名
    filename = 'music'
    if not os.path.exists(filename):
        os.mkdir(filename)
    soundName = sound_name + '.mp4'
    print(soundName)
    file_path = os.path.join(filename, soundName)
    try:
        with open(file_path, 'wb') as f:
            f.write(data)
            print(f'{soundName}下载成功')
    except Exception as e:
        print(e)


def choose():
    # 加一个判断是否继续下载下一首
    count = 0
    chose = input('请输入是否继续下砸下一首(y/n):>>>')
    if chose == 'y':
        count += 1
        print(f'你已经下载了{count}首歌曲了哦 (≖ᴗ≖)✧')
        main()
    else:
        print("感谢您的使用，谢谢！ (｡･ω･｡) ")


def main():
    sound_number = input('请输入歌曲的id:>>>>')
    sound_number = int(sound_number)
    download_url = get_download_url(sound_number)
    sound_name = input('请输入歌曲的名字:>>>>')
    if download_url:
        download_sound(download_url, sound_name)
    else:
        print('该歌曲是vip歌曲，暂不能下载！')
    choose()


if __name__ == '__main__':
    main()
