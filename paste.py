# -*- coding: utf-8 -*-

import requests, re, time
from bs4 import BeautifulSoup as bs
from w3lib.encoding import html_to_unicode as cutf
import lxml.html
import os.path


# edit link for the suitable format
def edit_links(html_source, home_url):
    d = lxml.html.fromstring(html_source)
    d.make_links_absolute(home_url)
    h = lxml.html.tostring(d)
    return (h)


def dump(url, file_name):
    query = requests.get(url).content
    open(file_name, 'wb').write(query)

# main url for 'the archive' page
url = 'http://pastebin.com/archive'

# infinite loop
while True:
    r = requests.get(url).content
    u = cutf(None, r)[1]
    h = edit_links(u, url)
    s = bs(h, "lxml")
    for i in s.find_all('table', class_=re.compile('(?i)^maintable$')):
        for j in i.find_all('a', href=re.compile('.*')):
            link = '%s' % j.get('href')
            if len(re.findall('(?i)archive', link)) > 0: continue
            file_name = '%s.txt' % re.sub('.+/', '', link)
            if os.path.isfile(file_name): continue
            raw_link = 'http://pastebin.com/raw.php?i=%s' % re.sub('.+/', '', link)
            dump(raw_link, file_name)
    time.sleep(1)
