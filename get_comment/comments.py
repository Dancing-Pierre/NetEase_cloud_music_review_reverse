import json
import time

import execjs
import requests
from fake_useragent import UserAgent


def get_argument(music_id, page):
    with open('./comments.js', 'r', encoding='utf-8') as f:
        time_now = int(round(time.time() * 1000))
        # 第一个 {} 符号被误识别为占位符，导致后面的键值对无法正确替换，可以使用双大括号 {{}} 来表示字面意义上的大括号
        aa = '{{"rid":"R_SO_4_{}","threadId":"R_SO_4_{}","pageNo":"{}","pageSize":"20","cursor":"{}","offset":"0","orderType":"1","csrf_token":""}}'.format(
            music_id, music_id, page, time_now)
        bb = '010001'
        cc = '00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7'
        dd = '0CoJUm6Qyw8W8jud'
        argument_data = execjs.compile(f.read()).call('d', aa, bb, cc, dd)
        params = argument_data['encText']
        encSecKey = argument_data['encSecKey']
    return params, encSecKey


def get_comment(params, encSecKey):
    url = 'https://music.163.com/weapi/comment/resource/comments/get?csrf_token='
    header = {
        "Origin": "https://music.163.com",
        "Pragma": "no-cache",
        "Referer": "https://music.163.com/song?id=65766",
        "Sec-Ch-Ua": "\"Not/A)Brand\";v=\"99\", \"Google Chrome\";v=\"115\", \"Chromium\";v=\"115\"",
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": "\"Windows\"",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": UserAgent().random
    }
    data = {
        "params": f"{params}",
        "encSecKey": f"{encSecKey}"
    }
    response = requests.post(url=url, headers=header, data=data)
    data = response.text
    return data


def parse_data(data):
    json_data = json.loads(data)
    comments = json_data['data']['comments']
    print('采集评论数据如下：')
    for i in comments:
        comment = i['content']
        print(comment)


if __name__ == '__main__':
    while True:
        music_id = input('请输入歌曲id：')
        page = input('请输入要采集第几页评论：')
        params, encSecKey = get_argument(music_id, page)
        response_data = get_comment(params, encSecKey)
        parse_data(response_data)
        is_continue = input('是否继续采集（y/n）：')
        if is_continue == 'n':
            break
