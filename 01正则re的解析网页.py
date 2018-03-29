import requests
import re
content = requests.get('https://book.douban.com/').text
# print(content)
# pattern = re.compile('<li.*?item.*?href="(.*?)".*?title="(.*?)".*?more-meta.*?author">(.*?)</span>.*?year">(.*?)</span>.*?</li>',re.S)
pattern = re.compile('<a.*?href="(.*?)"\s*?title="(.*?)">(.*?)</a>',re.S)
results = re.findall(pattern,content)
# print(results)
for result in results:
#     url ,name,author,date=result
    url,title,img = result
    print(url,title,img)