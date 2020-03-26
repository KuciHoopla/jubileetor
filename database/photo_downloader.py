
from urllib.request import urlopen
from bs4 import BeautifulSoup
import urllib


def url_getter():
    url = "https://www.pinterest.ca/search/pins/?q=shoes%20mens&rs=guide&term_meta[]=shoes%7Ctyped&add_refine=mens%7Cguide%7Cword%7C0"
    html = urlopen(url)
    photos_urls = []
    soup = BeautifulSoup(html)
    for res in soup.findAll('img'):
        photo_url = res.get('src')
        photos_urls.append(photo_url)
        print(photo_url)
    return photos_urls


def loader():
    i = 61
    for photo in url_getter():
        photo_name = f'{i}.jpg'
        image = urllib.request
        image.urlretrieve(photo, photo_name)
        i +=1

url_getter()
