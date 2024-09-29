
import re
import json
import requests
from bs4 import BeautifulSoup
from mongoengine import connect
from mongoengine import Document, StringField, ListField, ReferenceField



connect(db='GoIT3-3', host="mongodb+srv://rezvaserg:FdhiHDdmAphGFbzg@cluster0.5izpshs.mongodb.net/GoIT3-3?retryWrites=true&w=majority")


class Author(Document):
    fullname = StringField(required=True)
    born_date = StringField()
    born_location = StringField()
    description = StringField()

class Quote(Document):
    tags = ListField(StringField())
    author = ReferenceField(Author)
    quote = StringField()



base_url = "https://quotes.toscrape.com"


def get_url():
    p=1
    new_url = base_url
    while True:
        print('--------------------------------------------',p,new_url)
        spider(new_url)
        response = requests.get(new_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        content = str(soup.select('li[class=next] a'))
        
        search_url = re.search(r"/page/\d+/",content)
        # break
        if search_url:
            new_url = base_url + search_url.group()
            p +=1
        else:
            break

def spider(url):

    global quotes_json
    global authors_dict

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    quotes = soup.find_all('span', class_='text')
    authors = soup.find_all('small', class_='author')
    tags = soup.find_all('div', class_='tags')
    

    first_div = str(soup.select('div[class=quote] a '))
    authors_a = re.findall(r"/author/\w*-*\w*-*\w*-*\w*-*\w*-*\w*-*",first_div)

    for i in range(0, len(quotes)):

        tagsforquote = tags[i].find_all('a', class_='tag')
        all_tags = []
        authors_dict.update({authors[i].text:authors_a[i]})
        for tagforquote in tagsforquote:
            all_tags.append(tagforquote.text)

        quotes_json.append({"tags":all_tags,"author":authors[i].text,"quote":quotes[i].text})

        
def spider_authors():
    global authors_dict
    global authors_json
    for key, url in authors_dict.items():
        response = requests.get(base_url + url)
        soup = BeautifulSoup(response.text, 'html.parser')
        born = soup.find('span', class_='author-born-date').text
        location = soup.find('span', class_='author-born-location').text
        description = soup.find('div', class_='author-description').text
        
        authors_json.append({"fullname":key,"born_date":born,"born_location":location,"description":description})





quotes_json = []
authors_dict= {}
authors_json = []
get_url()
spider_authors()

with open('quotes.json', 'w', encoding='utf-8') as f:
    json.dump(quotes_json, f, ensure_ascii=False, indent=4)


with open('authors.json', 'w', encoding='utf-8') as f:
    json.dump(authors_json, f, ensure_ascii=False, indent=4)




for author_data in authors_json:

    author = Author(**author_data)
    author.save()



for quote_data in quotes_json:
    author_name = quote_data['author']
    author = Author.objects(fullname=author_name).first()
    if author:
        quote_data['author'] = author
        quote = Quote(**quote_data)
        quote.save()