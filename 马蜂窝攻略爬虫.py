#encoding:utf-8
from urllib import parse
import requests
from requests.exceptions import RequestException
from bs4 import BeautifulSoup
import re
from selenium import webdriver


def get_one_page(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None

def parse_one_page(html):
    '''抓取游记网址'''
    bs = BeautifulSoup(html, "html.parser")
    sub_URL = bs.findAll("div", {"class": "ct-text"})
    #print(sub_URL)
    pattern = re.compile('http://www.mafengwo.cn/i/[0-9]*\.[a-z]*')
    items = re.findall(pattern, html)
    items = list(set(items))
    return items


def get_url(keyWord, start):
    '''keyWord为搜索关键词，start用于翻页'''
    url='http://www.mafengwo.cn/search/s.php?q={}&p='.format(parse.quote(keyWord)) + str(start) + '&t=info&kt=1'
    #print(url)
    items = parse_one_page(get_one_page(url))
    #print(items)
    return items


def get_text(url):
    '''抓取游记中的文字'''
    bs = BeautifulSoup(scroll_foot(url).page_source, "lxml")
    text_1 = bs.findAll("p", {"class": "_j_note_content"})
    text = []
    for p in text_1:
        text.append(p.get_text)
    #print(text)
    title = re.findall('\d+',url)
    with open('.\\攻略\\' + str(title) + '.txt', 'w', encoding="utf-8") as f:
        for i in range(len(text)):
            t = re.sub(u"\\<.*?\\>|\\{.*?}|\\[.*?]", '', str(text[i]))
            t = t.replace(" ", "")
            f.write(str(t))


def scroll_foot(URL):
    Chrome_login = webdriver.Chrome(
        executable_path=r'C:\Users\ASUS\AppData\Local\Programs\Python\Python36\chromedriver.exe')
    Chrome_login.get(URL)
    js = "var q=document.documentElement.scrollTop=100000"
    for i in range(5):  #下拉5次
        Chrome_login.execute_script(js)
    return Chrome_login


def main(keyword, page):
    items = []
    for i in range(1,page): #查询a到b-1页
        for ii in get_url(keyword, i):
            items.append(ii)
    items = list(set(items))
    #print(items)
    for i in items:
        get_text(i)

if __name__ == '__main__':
    main(keyword="斐济游记", page=30)


'''
bs = BeautifulSoup(scroll_foot('http://www.mafengwo.cn/i/750833.html').page_source, "lxml")
text_1 = bs.findAll("p", {"class": "_j_note_content"})
text = []
for p in text_1:
    text.append(p.get_text)
print(str(text[0]))
t = re.sub(u"\\<.*?\\>|\\{.*?}|\\[.*?]", '', str(text[0]))
print(t)
'''




