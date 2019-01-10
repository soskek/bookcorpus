#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import time
import re

try:
    from cookielib import CookieJar
    cj = CookieJar()
    import urllib2
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    import urllib
    urlretrieve = urllib.urlretrieve
except ImportError:
    import http.cookiejar
    cj = http.cookiejar.CookieJar()
    import urllib
    opener = urllib.request.build_opener(
        urllib.request.HTTPCookieProcessor(cj))
    urlretrieve = urllib.request.urlretrieve

from bs4 import BeautifulSoup

import os
import datetime
import json

# If you wanna use some info, write them.
REQUIRED = [
    #    'page',
    #    'epub',
    #    'txt',
    #    'title',
    #    'author',
    #    'genres',
    #    'publish',
    #    'num_words',
    'b_idx',
]

search_url_pt = 'https://www.smashwords.com/books/category/1/downloads/0/free/medium/{}'
search_urls = [search_url_pt.format(i) for i in range(0, 18340 + 1, 20)]

num_words_pt = re.compile(r'Words: (\d+)')
pub_date_pt = re.compile(r'Published: ([\w\.]+\s[\d]+,\s[\d]+)')
lang_pt = re.compile(r'Language: (\w+)')
# Language: Spanish

target_langs = []
# if you want text only in selected languages, write them. e.g. ['English']


def main():
    start_time = time.time()
    dataset = []
    sys.stderr.write(str(datetime.datetime.now()) + '\n')

    book_index = 0

    for i, s_url in enumerate(search_urls):
        # print('#', i, s_url)
        response = opener.open(s_url)
        body = response.read()
        soup = BeautifulSoup(body, 'lxml')

        book_links = soup.find_all(class_="library-title")

        for b_link in book_links:
            book_index += 1
            b_url = b_link.get('href')
            response = opener.open(b_url)
            body = response.read()
            soup = BeautifulSoup(body, 'lxml')

            # get meta
            meta_infos = soup.find_all(class_="col-md-3")
            if not meta_infos:
                sys.stderr.write('Failed: meta_info {}\n'.format(b_url))
                continue

            # get lang
            meta_txts = []
            for m in meta_infos:
                match = lang_pt.search(m.text)
                if match:
                    lang = match.group(1)
                    meta_txts.append(m.text)
                    break
            else:
                sys.stderr.write('Failed: language {}\n'.format(b_url))
                continue

            # check lang
            if target_langs:
                if lang not in target_langs:
                    continue

            # get num words
            meta_txt = meta_txts[0].replace(',', '')
            match = num_words_pt.search(meta_txt)
            if match:
                num_words = int(match.group(1))
            elif 'num_words' in REQUIRED:
                sys.stderr.write('Failed: num_words {}\n'.format(b_url))
                continue
            else:
                num_words = 0

            # get publish date
            meta_txt = meta_txts[0]
            match = pub_date_pt.search(meta_txt)
            if match:
                pub_date = match.group(1)
            elif 'publish' in REQUIRED:
                sys.stderr.write('Failed: publish {}\n'.format(b_url))
                continue
            else:
                pub_data = ''

            # get genres
            genre_txts = soup.find_all(class_="category")
            if genre_txts:
                genres = [g.text.replace('\u00a0\u00bb\u00a0', '\t')
                          for g in genre_txts]
            elif 'genres' in REQUIRED:
                sys.stderr.write('Failed: genre {}\n'.format(b_url))
                continue
            else:
                genres = []

            # get title
            title = soup.find("h1")
            if title:
                title = title.text
            elif 'title' in REQUIRED:
                sys.stderr.write('Failed: title {}\n'.format(b_url))
                continue
            else:
                title = ''

            # get author
            author = soup.find(itemprop="author")
            if author:
                author = author.text
            elif 'author' in REQUIRED:
                sys.stderr.write('Failed: author {}\n'.format(b_url))
                continue
            else:
                author = ''

            # get epub
            epub_links = soup.find_all(
                title="Nook, Kobo, Sony Reader, and tablets")
            if epub_links:
                epub_url = epub_links[0].get('href')
                if epub_url:
                    epub_url = 'https://www.smashwords.com' + epub_url
                elif 'epub' in REQUIRED:
                    sys.stderr.write('Failed: epub2 {}\n'.format(b_url))
                    continue
                else:
                    epub_url = ''
            elif 'epub' in REQUIRED:
                sys.stderr.write('Failed: epub1 {}\n'.format(b_url))
                continue
            else:
                epub_url = ''

            # get txt if possible
            txt_links = soup.find_all(
                title="Archival; contains no formatting")
            if not txt_links:
                txt_url = ''
            else:
                txt_url = txt_links[0].get('href')
                if not txt_url:
                    txt_url = ''
                else:
                    txt_url = 'https://www.smashwords.com' + txt_url

            if not epub_url and not txt_url:
                sys.stderr.write('Failed: epub and txt {}\n'.format(b_url))
                continue

            data = {
                'page': b_url,
                'epub': epub_url,
                'txt': txt_url,
                'lang': lang,
                'title': title,
                'author': author,
                'genres': genres,
                'publish': pub_date,
                'num_words': num_words,
                'b_idx': book_index
            }
            print(json.dumps(data))


if __name__ == '__main__':
    main()
