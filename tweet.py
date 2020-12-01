import time
import emoji
import re
import os
import json
from requests_oauthlib import OAuth1Session
import pandas as pd

# .env ファイルをロードして環境変数へ反映
from dotenv import load_dotenv
load_dotenv()


# OAuth認証部分
CK = os.getenv('CK')
CS = os.getenv('CS')
AT = os.getenv('AT')
ATS = os.getenv('ATS')
twitter = OAuth1Session(CK, CS, AT, ATS)

# Twitter Endpoint(ユーザータイムラインを取得する)


def remove_emoji(src_str):
    """
    絵文字の削除
    """
    return ''.join(c for c in src_str if c not in emoji.UNICODE_EMOJI)


def user_search(keyword):
    """
    APIによるユーザの検索
    """
    url = 'https://api.twitter.com/1.1/users/search.json'

    # Enedpointへ渡すパラメーター
    params = {
        'q': keyword
    }
    req = twitter.get(url, params=params)

    if req.status_code == 200:
        res = json.loads(req.text)
        for line in res:
            print(line['description'])
            print(line['followers_count'])
            print(line['name'])
            print(line['friends_count'])
            print('*******************************************')
    else:
        print("Failed: %d" % req.status_code)


def user_timeline_search(count, user_name):
    """
    ユーザのタイムラインのデータを取得
    """
    url = "https://api.twitter.com/1.1/statuses/user_timeline.json"

    # パラメーター
    params = {
        'count': count,             # 取得するtweet数 最大値200
        'screen_name': user_name,  # twitterアカウント名
        'include_rts': False,
        'exclude_replies': False
    }
    time.sleep(1)
    req = twitter.get(url, params=params)

    all_text = ''
    if req.status_code == 200:
        res = json.loads(req.text)
        for line in res:
            text = re.sub(
                r'https?://[\w/:%#\$&\?\(\)~\.=\+\-…]+', "", line['text'])
            text = re.sub('RT', "", text)
            text = re.sub('お気に入り', "", text)
            text = re.sub('まとめ', "", text)
            text = re.sub(r'[!-~]', "", text)  # 半角記号,数字,英字
            text = re.sub(r'[︰-＠]', "", text)  # 全角記号
            text = re.sub('\n', " ", text)  # 改行文字
            text = re.sub('…', " ", text)  # 改行文字
            # print(text)
            if text[-1] == '。':
                all_text += text
                # print(text)
            else:
                n_text = text + '。'
                all_text += n_text
    else:
        print("Failed: %d" % req.status_code)

    path_w = './text_model/text_w.txt'

    all_text = remove_emoji(all_text)

    with open(path_w, mode='w') as f:
        f.write(all_text)


# user_search('プログラミング ')
# user_timeline_search(200, '@poly_soft')
user_timeline_search(200, '@manabubannai')