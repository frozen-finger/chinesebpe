import requests
from bs4 import BeautifulSoup
import re
import os
from PIL import Image
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import collections


def crawl(word):
    headers = {'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1'}
    try:
        url = 'https://dictionary.goo.ne.jp/word/kanji/{0}'.format(word)
        response = requests.get(url=url, headers=headers).text
        content = BeautifulSoup(response, 'lxml')
        soup = content.find('dt', text="部首")
        if soup == None:
            # url = 'https://dict.baidu.com/s?wd={0}&ptype=zici'.format(word)
            # response = requests.get(url=url,headers=headers).text
            # content = BeautifulSoup(response,'lxml')
            # # print(response)
            # # 笔顺动图
            # soup = content.find(id="word_bishun")
            # bishun = re.findall(r'data-src="(.*?)"',str(soup))[0]
            # # 拼音
            # soup = content.find(id="pinyin")
            # pinyins = soup.find_all('b')
            # pinyin = ''
            # for i in pinyins:
            #     i = re.findall(r'>(.*?)<',str(i))[0]
            #     pinyin = pinyin + ' ' + i
            # pinyin = pinyin.strip(' ')
            # # 部首
            # soup = content.find(id="radical")
            # bushou = soup.find('span').get_text()
            # # 笔画
            # soup = content.find(id="stroke_count")
            # bihua = soup.find('span').get_text()
            # # 组词
            # soup = content.find(class_="related_idiom").get_text()
            # zuci = soup.replace('\n',' ').strip(' ').rstrip(' 更多') # 当组词过多时防止末尾出现更多这一链接词
            # # 近反义词
            # try:
            #     syns = content.find(id="synonym-content").get_text().strip('\n') # 单独执行时不报错且不执行后面的语句
            #     syn = ''
            #     for i in syns:
            #         if ishan(i):
            #         	syn += i
            # except:
            #     syn = 'Nan'
            # try:
            #     ants = content.find(id="antonym-content").get_text().strip('\n')
            #     ant = ''
            #     for i in ants:
            #         if ishan(i):
            #         	ant += i
            # except:
            #     ant = 'Nan'
            # jinfan = syn + ' ' + ant
            # # print(word, bishun, pinyin, bushou, bihua, zuci, jinfan)
            print('wrong')
            print("can't find character" + word + "in goo")
            bushou = word
        else:

            # 拼音


            try:
                soup = soup.find_next_sibling().find('a').get_text().split()[0]
                bushou = soup
                bushou = bushou
            except:
                print("can't find character" + word + "in goo")
                bushou = word

            # pinyins = soup.find_all('b')
            # pinyin = ''
            # for i in pinyins:
            #     i = re.findall(r'>(.*?)<',str(i))[0]
            #     pinyin = pinyin + ' ' + i
            # pinyin = pinyin.strip(' ')
            # # 部首
            # soup = content.find(id="radical")
            # bushou = soup.find('span').get_text()
            # # 笔画
            # soup = content.find(id="stroke_count")
            # bihua = soup.find('span').get_text()
            # # 组词
            # soup = content.find(class_="related_idiom").get_text()
            # zuci = soup.replace('\n',' ').strip(' ').rstrip(' 更多') # 当组词过多时防止末尾出现更多这一链接词
            # # 近反义词
            # try:
            #     syns = content.find(id="synonym-content").get_text().strip('\n') # 单独执行时不报错且不执行后面的语句
            #     syn = ''
            #     for i in syns:
            #         if ishan(i):
            #         	syn += i
            # except:
            #     syn = '暂无近义词'
            # try:
            #     ants = content.find(id="antonym-content").get_text().strip('\n')
            #     ant = ''
            #     for i in ants:
            #         if ishan(i):
            #         	ant += i
            # except:
            #     ant = '暂无反义词'
            # jinfan = syn + ' ' + ant

        result = {
            'word': word,
            # 'bishun': bishun,
            # 'pinyin': pinyin,
            'bushou': bushou,
            # 'bihua': bihua,
            # 'zuci': zuci,
            # 'jinfan': jinfan
        }
        return result
    except:
        None

# find_all() 方法没有找到目标是返回空列表, find() 方法找不到目标时,返回 None

# 判断是否为一个中文汉字
def ishan(text):
	if '\u3400' <= text <= '\u4DB5' or '\u4e00' <= text <= '\u9fff':
		return True
	else:
		return False


with open("Data/train", encoding='utf-8') as f:
    lines = f.readlines()
corpus = collections.defaultdict(int)
for li in lines:
    for i in li:
        if ishan(i):
            corpus[i] += 1


# def giftopng(text, url):
#     r = requests.get(url=url)
#     if r.status_code == 200:
#         open("C:/Users/99388/Desktop/Charactergif/"+text+".gif", 'wb+').write(r.content)
#         print("done")
#     giffile = "C:/Users/99388/Desktop/Charactergif/"+text+".gif"
#     im = Image.open(giffile)
#     try:
#         while True:
#             current = im.tell()
#             print(current)
#             im1 = im.resize((448, 448), Image.ANTIALIAS)
#             im1.save("C:/Users/99388/Desktop/Character/" + text + ".png")
#             im.seek(current+1)
#     except EOFError:
#         pass

if __name__ == '__main__':
    index = 0
    jbushouindex = collections.defaultdict(int)
    jkanji = collections.defaultdict(int)
    for i in corpus.keys():
        result = crawl(i)
        if result['bushou'] in jbushouindex:
            jkanji[i] = jbushouindex[result['bushou']]
        else:
            jbushouindex[result['bushou']] = index
            jkanji[i] = index
            index += 1

        index += 1
    with open("Data/jbushouindex", 'a', encoding='utf-8', ) as f:
        for i in jbushouindex:
            f.write(i + ' ' + str(jbushouindex[i]) + '\n')
    with open("Data/jkanjii", 'a', encoding='utf-8', ) as f:
        for i in jkanji:
            f.write(i + ' ' + str(jkanji[i]) + '\n')
    # print(crawl('費'))
