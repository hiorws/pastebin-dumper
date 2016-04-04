# -*- coding: utf-8 -*-

import requests, re, time
from bs4 import BeautifulSoup as bs
from w3lib.encoding import html_to_unicode as cutf
import lxml.html
import os.path
from free_disk_space_check import disk_usage
from sys import argv

# check free diskspace
def check_disk_usage():
    current_disk_usage = disk_usage("/")
    total_space = float(current_disk_usage.total)
    used_space = float(current_disk_usage.used)
    free_space = float(current_disk_usage.free)
    return total_space, used_space, free_space

# check freespace higher than X
def freespace_higher_than(percent):
    total, used, free = check_disk_usage()
    if free / total > percent:
        return True
    else:
        return False

# edit link for the suitable format
def edit_links(html_source, home_url):
    d = lxml.html.fromstring(html_source)
    d.make_links_absolute(home_url)
    h = lxml.html.tostring(d)
    return (h)

def dump(url, file_name):
    query = requests.get(url).content
    open("dumps/" + file_name, 'wb').write(query)

# main url for 'the archive' page
url = 'http://pastebin.com/archive'

def main(percent_by_user=None):
    # infinite loop
    if not os.path.exists("dumps"):
        os.makedirs("dumps")
    while True and freespace_higher_than(percent_by_user):
        # total, used, free = check_disk_usage()
        # print("Total: " + total)
        # print("Used: " + used)
        # print("Free: " + free)
        print "Tries to dump"
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
    print("Not enough freespace on disk!")

if __name__ == "__main__":
    print("Started to dump...")
    if len(argv) == 2:
        main(int(argv[1]))
    else:
        print("Enter an argument for freespace percentage on disk, sample usage:")
        print("python paste.py 20")
