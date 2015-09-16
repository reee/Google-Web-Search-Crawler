#!/usr/bin/env python2
# -*- coding: utf8 -*-

import os
import string
import urllib2
import textract
import uuid

from boilerpipe.extract import Extractor

def format_filename(s):
    valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
    filename = ''.join(c for c in s if c in valid_chars)
    filename = filename.replace(' ','_') # I don't like spaces in filenames.
    return filename

def url_file_parser(url_file):
    line_list = open(url_file).readlines()
    line_list = [line.decode('utf-8') for line in line_list]
    title_url_list = [line.split(' ; ') for line in line_list]
    return title_url_list

def parse_pdf(pdf_url):
    file_name = str(uuid.uuid4()) + '.pdf'
    # We put the temp pdf in /tmp beacuse it is a ramfs
    file_path = os.path.join('/tmp', file_name)
    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', useragent)]
    try:
        response = opener.open(html_url).read()
    # We could run into any errors when downloading
    # So we use 'except:' to handle all the errors!
    # It's UGLY i know.
    except:
        print 'Downloading Error: %s' % pdf_url
        pass
    else:
        with open(file_path) as f:
            f.write(respinse)
        pdftxt = textract.process(file_path)
        os.remove(file_path)
        return pdftxt

def parse_html(html_url):
    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', useragent)]
    try:
        response = opener.open(html_url).read()
        extractor = Extractor(extractor='ArticleExtractor', html=response)
    # Again, I know it's UGLY!!!
    except:
        print 'Downloading Error: %s' % html_url
        pass
    else:
        return extractor.getText().encode('utf-8')

def get_text_data(title_url, result_dir):
    title = title_url[0].strip()
    url = title_url[1].strip()
    if '.pdf' in url:
        print 'Processing PDF %s' % url
        content = parse_pdf(url)
    else:
        print 'Processing HTML %s' % url
        content = parse_html(url)
    if content:
        filename = format_filename(title) + '.txt'
        filepath = os.path.join(result_dir, filename)
        with open(filepath, 'w') as f:
            f.write(content)

def get_url_file_list(result_remain_file):
    if not os.path.isfile(result_remain_file):
        url_file_list = os.listdir(url_file_dir)
        with open(result_remain_file, 'w') as f:
            f.write('\n'.join(url_file_list))
    else:
        with open(result_remain_file) as f:
            url_file_list = f.readlines()
            url_file_list = [url_file.strip() for url_file in url_file_list]
    return url_file_list

def get_all_text(url_file_list, url_file_dir):
    for url_file in url_file_list:
        keyword = os.path.splitext(url_file)[0]
        result_dir = os.path.join(base_dir, 'text-result-drive', keyword)
        if not os.path.exists(result_dir):
            os.makedirs(result_dir)
        url_file_path = os.path.join(url_file_dir, url_file)
        title_url_list = url_file_parser(url_file_path)
        for title_url in title_url_list:
            get_text_data(title_url, result_dir)
        print '%s Finish. Removeing it from the list' % keyword
        url_file_list.remove(url_file)
        with open(result_remain_file, 'w') as f:
            f.write('\n'.join(url_file_list))

base_dir = '/data/google-web-search-crawler/'
result_remain_file = os.path.join(base_dir, 'text-result-drive', 'remain.txt')
url_file_dir =  os.path.join(base_dir, 'keyword-result-drive')
useragent = 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.124 Safari/537.36'

url_file_list = get_url_file_list(result_remain_file)
if url_file_list:
    get_all_text(url_file_list, url_file_dir)
