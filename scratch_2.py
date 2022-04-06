from bs4 import BeautifulSoup as bs
import requests
from collections import Counter
import io
import re
import pandas
import ssl
import urllib3
from urllib3 import poolmanager

## 1. _ Ask user to type the name of the artist and force it to lowercase
artist = input('Select Artist: ').lower()
## 1.1. _ Check if there's some article in artists' name and ignore it
if artist[0:4] == 'the ':
    artist = artist[4:]
elif artist[0:2] == 'a ':
    artist = artist[2:]
## 1.2. _ Make a list of replacements for a further URL usage (what to replace / by what) and execute replacements
replace_list_for_artists = (' ','_','.','_','&','and','(','',')','','+','and')
i = 1
while i < len(replace_list_for_artists):
    artist = artist.replace(replace_list_for_artists[i-1],replace_list_for_artists[i])
    i = i + 2

## 2. By now we have a decent artist name for a URL search at amalgama-lab project
url_artist = 'https://www.amalgama-lab.com/songs/' + artist[0] + '/' + artist
## 2.1. !Secuirty_warning! Found SSL Error decision @ https://stackoverflow.com/questions/61631955/python-requests-ssl-error-during-requests
class TLSAdapter(requests.adapters.HTTPAdapter):
    def init_poolmanager(self, connections, maxsize, block=False):
        """ Create and initialize the urllib3 PoolManager. """
        ctx = ssl.create_default_context()
        ctx.set_ciphers('DEFAULT@SECLEVEL=1')
        self.poolmanager = poolmanager.PoolManager(
                num_pools=connections,
                maxsize=maxsize,
                block=block,
                ssl_version=ssl.PROTOCOL_TLS,
                ssl_context=ctx)
session = requests.session()
session.mount('https://', TLSAdapter())
artist_response = session.get(url_artist).text.lower().splitlines()
## 2.2. By now we have a list of strings from HTML response from project as `artist_response`. We are aiming to get urls of songs
artist_songs_urls = []
i = 0
while i < len(artist_response):
    if artist_response[i].startswith('            <div class="list_songs"></div>') is True:
        break
    else:
        i = i+1
j = 0
while j < len(artist_response):
    if artist_response[j].startswith('\t\t\t<!-- ajax загрузка оставшихся переводов, если их количество превышает 250') is True:
        break
    else:
        j = j+1
artist_songs_urls = [response_piece for response_piece in artist_response[i:j]]

## print(artist_songs_urls)

# 2.3. By now we have some dirty list with URLS, so we're extracting URLs
every_song_url = []
for element in artist_songs_urls:
    soup = bs(element, 'html.parser').find_all('a')
    every_song_url.append(soup)

print(len(artist_songs_urls))
print(len(every_song_url))
print(every_song_url)