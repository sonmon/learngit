import json
from multiprocessing import Pool
import requests
import re


## 先抓取一页的数据,一般只能抓取一些静态网页的数据
def get_one_page(url):

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
    }
    # 设置错误提取
    try:
        response = requests.get(url=url,headers=headers,timeout=10)
        if response.status_code == 200:
            return response.text

        return None
    except requests.ReadTimeout:
        return '请求超时'
    except requests.RequestException:
        return '请求不上'


# 定义正则匹配
def parse_one_page(html):
    pattern = re.compile('<dd>.*?board-index.*?>(\d+)</i>.*?data-src="(.*?)".*?name"><a.*?>(.*?)</a>.*?star">(.*?)</p>'
                         '+.*?releasetime">(.*?)</p>.*?integer">(.*?)</i>.*?fraction">(.*?)</i>.*?</dd>',re.S)
    results = re.findall(pattern,html)
    # print(results)
    for one in results:
        # 构造生成器
        yield {
            'index':one[0],
            'url':one[1],
            'title':one[2],
            'actor':one[3].strip()[3:],
            'time':one[4].strip()[5:],
            'score':one[5]+one[6]
        }


def write_movie_text(content):
    with open('movies.txt','a',encoding='utf-8')as f:
        f.write(json.dumps(content,ensure_ascii=False)+'\n')
        f.close()


# 测试函数
def main(i):
    url = 'http://maoyan.com/board/4?offset='+str(i)
    html = get_one_page(url)
    # print(html)
    for one in parse_one_page(html):
        print(one)
        write_movie_text(one)

if __name__ == '__main__':
    # for i in range(1,10):
        # main(i*10)
    pool = Pool()
    pool.map(main,[i*10 for i in range(10)])

