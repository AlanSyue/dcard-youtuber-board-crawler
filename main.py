from bs4 import BeautifulSoup
import requests
import datetime
import lineTool
import schedule
import time

def job():
    api = 'https://www.dcard.tw/service/api/v2/forums/youtuber/posts?limit=100'

    headers = {'user-agent': 'Mozilla/5.0 (Macintosh Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'}

    res = requests.get(api, headers=headers)
    posts = res.json()

    token = 'Replace your token here'
    post_url = 'https://www.dcard.tw/f/youtuber/p/'

    for post in posts:
        # 貼文建立時間
        created_at = post['createdAt']
        date = created_at[:10]
        # 不是今天的貼文就過濾掉
        if date != str(datetime.date.today()):
            continue
        now = datetime.datetime.now()
        hour = int(created_at[11:13]) + 8
        current_hour = now.hour
        # 不是上個小時的貼文就過濾掉
        if hour >= current_hour or hour < (current_hour - 1):
            continue
        title = post['title']
        content = post['excerpt']
        if 'school' in post:
            school = post['school']
        else:
            school = ''
        if 'department' in post:
            department = post['department']
        else:
            department = ''
        reply = post['totalCommentCount']
        like = 0
        for reation in post['reactions']:
            like = like + reation['count']
        link = post_url + str(post['id'])
        msg = 'title:' + title + "\n" + 'content:' + content + "\n" + 'like: ' + str(like) + "\n" + "reply: " + str(reply) + "\n" + "link: " + link
        lineTool.lineNotify(token,msg)

# 每小時執行 job 這個 function
schedule.every().hour.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
