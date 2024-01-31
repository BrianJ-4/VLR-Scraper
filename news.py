import requests
import json
from bs4 import BeautifulSoup, Comment

def getNews(page = 1):
    newsDic = {}
    url = "https://www.vlr.gg/news/?page=" + str(page)
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    news = soup.find('div', class_ = 'wf-card').findAll('a')
    i = 0
    for article in news:
        articleURL = article['href']
        parts = articleURL.split('/')
        articleNum = parts[1]
        text = article.find('div', style = True)
        title = text.findAll('div', style = True)[0].getText().strip()
        subTitle = text.findAll('div', style = True)[1].getText().strip()
        section = text.find('div', class_ = 'ge-text-light').getText().strip()
        parts = section.split(" • ")
        date = parts[0].strip()
        date = date[date.index("•") + 2:]
        author = parts[1]
        author = author[author.index("by") + 3:]
        newsDic[i] = {
            "Title" : title,
            "subTitle" : subTitle,
            "Date" : date,
            "Author" : author,
            "URLNum" : articleNum,
        }
        i += 1
    
    return newsDic

def getArticle(articleNum):
    url = "https://www.vlr.gg/" + articleNum
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    #Remove uneeded text that is not visible on webpage
    for div in soup.find_all("span", class_ = 'wf-hover-card mod-article article-ref-card'): 
        div.decompose()

    #Remove comment text
    comments = soup.findAll(text = lambda text:isinstance(text, Comment))
    for comment in comments:
        comment.extract()
    
    # #Remove caption text
    # captions = soup.findAll('em')
    # for caption in captions:
    #     caption.extract()

    article = soup.find('div', class_  = 'article-body')
    print(url)
    return article.prettify()

    # with open("temp.html", "w", encoding = 'utf-8') as outfile:
    #     outfile.write(str(article.prettify()))

    # #look into this kind: https://www.vlr.gg/264266/riot-previews-major-balance-changes-to-11-agents