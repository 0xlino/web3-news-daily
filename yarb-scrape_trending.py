# coding:utf-8

import datetime
import codecs
import requests
import os
import time
from pyquery import PyQuery as pq
import createMarkdown as cm
import constants as c
import utils as utils

# function that will get bitcoin price from coindesk api
def get_btc_price():
    url = 'https://api.coindesk.com/v1/bpi/currentprice.json'
    response = requests.get(url)
    data = response.json()
    price_in_usd = data['bpi']['USD']['rate']
    return price_in_usd

def saveCryptoPricesToFile(filename):
    # get current date
    strdate = datetime.datetime.now().strftime('%Y-%m-%d')
    filename = '{date}.md'.format(date=strdate)

    with codecs.open(filename, "a", "utf-8") as f:
        f.write('\n#### Crypto Prices\n')

        # get bitcoin price
        btc_price = get_btc_price()
        f.write(u"* Bitcoin Price: {btc_price}\n".format(btc_price=btc_price))

    # git add commit push
    # git_add_commit_push(strdate, filename)


def git_add_commit_push(date, filename):
    cmd_git_add = 'git add {filename}'.format(filename=filename)
    cmd_git_commit = 'git commit -m "{date}"'.format(date=date)
    cmd_git_push = 'git push -u origin master'

    os.system(cmd_git_add)
    os.system(cmd_git_commit)
    os.system(cmd_git_push)

def scrape(language, filename):
    url = utils.makeTrendingURL(language)
    r = requests.get(url, headers=c.HEADERS)
    assert r.status_code == 200
    
    d = pq(r.content)
    items = d('div.Box article.Box-row')

    # codecs to solve the problem utf-8 codec like chinese
    with codecs.open(filename, "a", "utf-8") as f:
        f.write('\n#### {language}\n'.format(language=language))

        for item in items:
            i = pq(item)
            title = i(".lh-condensed a").text()
            owner = i(".lh-condensed span.text-normal").text()
            description = i("p.col-9").text()
            url = i(".lh-condensed a").attr("href")
            url = "https://github.com" + url
            f.write(u"* [{title}]({url}):{description}\n".format(title=title, url=url, description=description))


def scrape2(language, filename, date):
    HEADERS = {
        'User-Agent'		: 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:11.0) Gecko/20100101 Firefox/11.0',
        'Accept'			: 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding'	: 'gzip,deflate,sdch',
        'Accept-Language'	: 'zh-CN,zh;q=0.8'
    }

    url = 'https://raw.githubusercontent.com/dubuqingfeng/yarb-web3/main/today.md'
    r = requests.get(url, headers=HEADERS)
    assert r.status_code == 200

    # print(r.content)
    
    # d = pq(r.content)
    # items = d('div.Box article.Box-row')

    with codecs.open(filename, "a", "utf-8") as f:
        f.write('\n#### {language}\n'.format(language=language))

        # strdate2 = datetime.datetime.now().strftime('%Y-%m-%d')
        # minus one day
        strdate2 = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime('%Y-%m-%d')
        print(strdate2)
        # remove # 每日 web3 资讯（2023-11-02) line
        content = r.content.decode('utf-8')

        content = content.replace('# 每日 web3 资讯（2023-11-02）', '')

        f.write(content)


def createAndScrape(title, filename, yearString, dateString, isToday=False):
    filename = '{date}.md'.format(date=dateString)

    # createMarkdown(dateString, filename)

    HEADERS = {
        'User-Agent'		: 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:11.0) Gecko/20100101 Firefox/11.0',
        'Accept'			: 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding'	: 'gzip,deflate,sdch',
        'Accept-Language'	: 'zh-CN,zh;q=0.8'
    }

    # f string https://raw.githubusercontent.com/dubuqingfeng/yarb-web3/main/archive/2023/2023-01-01.md

    if isToday:
        url = 'https://raw.githubusercontent.com/dubuqingfeng/yarb-web3/main/today.md'
    else:
        url = f'https://raw.githubusercontent.com/dubuqingfeng/yarb-web3/main/archive/{yearString}/{dateString}.md'

    # url = 'https://raw.githubusercontent.com/dubuqingfeng/yarb-web3/main/today.md'
    r = requests.get(url, headers=HEADERS)
    assert r.status_code == 200

    # print(r.content)
    
    # d = pq(r.content)
    # items = d('div.Box article.Box-row')

    with codecs.open(filename, "a", "utf-8") as f:
        f.write('#### {title}\n'.format(title=title))
        content = r.content.decode('utf-8')

        # use date string to replace date in # 每日 web3 资讯（2023-11-02) 
        datestring1 = '# 每日 web3 资讯'
        # content = content.replace(f'# 每日 web3 资讯（{dateString}) ', '')
        content = content.replace(datestring1, '-')
        f.write(content)


def job():
    strdate = datetime.datetime.now().strftime('%Y-%m-%d')
    todayDateFileName = '{date}.md'.format(date=strdate)

    yesterdayDate = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime('%Y-%m-%d')

    # create markdown file
    # createMarkdown(strdate, filename)
    
    # scrape('Shopify', filename)
    # scrape('Liquid', filename)
    # scrape('Typescript', filename)
    # scrape('Javascript', filename)
    # scrape('Python', filename)

    # saveCryptoPricesToFile(filename=filename)

    # scrape2('Web3 Yarb', filename, strdate)
    runDate = yesterdayDate
    filename = '{date}.md'.format(date=runDate)
    # filenameTrending = '{date}-trending.md'.format(date=runDate)

    # cm.createMarkdown(c.TRENDING_SCRAPE, filenameTrending)
    # scrape('Javascript', filenameTrending)
    # scrape('Typescript', filenameTrending)

    createAndScrape('Web3 Daily News Feed', filename, '2023', runDate)

if __name__ == '__main__':
    job()
    # jobnew('javascript-trending')