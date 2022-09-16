import json
import requests
import re
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup

def search(band, song):
    #song = input('Type the song:\n')
    #band = input('Type the band:\n')
    url = "https://www.google.co.uk/search?q="+song+band+"chordify" #Busqueda
    page = requests.get(url).text
    soup = BeautifulSoup(page, 'lxml');
    link = soup.find('a', href=re.compile('https://chordify.net'))
    link = link['href']
    url = re.search("https[^&]+",link).group(0) #Link chordify

    return url

def get_chords(band,song):
    #Crawl the link
    url = search(band,song)
    page = requests.get(url).text
    soup = BeautifulSoup(page, 'lxml');

    link = soup.find('link', href=re.compile('api/v2/songs/youtube'))
    sufix = link['href']
    prefix = 'https://chordify.net'
    new_url = prefix+sufix
    #Scrap the json
    req = Request(new_url, headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req)
    data = json.loads(webpage.read())

    return [data['derivedKey'].split(':')[0], data['chords'].split()]

def get_youtube(band,song):
    url = "https://www.google.co.uk/search?q="+song+band+"spotify"
    page = requests.get(url).text
    soup = BeautifulSoup(page, 'lxml');
    link = soup.find('a', href=re.compile('https://open.spotify.com'))
    link = link['href']
    url = re.search("https[^&]+",link).group(0) #Link
    return url

if __name__ == '__main__':
    get_chords()