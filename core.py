#!/usr/bin/env python2
# -*- coding: utf8 -*-

import sys
import os
import time
import random
import argparse

from selenium import webdriver
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

def conv_to_list(text_file):
    with open(text_file) as f:
        lines = f.readlines()
        line_list = []
        for line in lines:
            if not line.strip():
                continue
            if line.startswith('#'):
                continue
            else:
                line_list.append(line.strip())
    return line_list

def start_browser(useragent_list):
    user_agent = random.choice(useragent_list)
    profile = webdriver.FirefoxProfile()
    profile.set_preference("general.useragent.override", user_agent)
    br = webdriver.Firefox(profile)
    br.implicitly_wait(10)
    return br

def make_up_url(google_add, keyword, page100=True):
    if page100:
        the_url = google_add + 'search?num=100&q=' + keyword
    else:
        the_url = google_add + 'search?q=' + keyword
    return the_url

def scrape_the_page(br):
    # Xpath will find a subnode of h3, a[@href] specifies that we only want <a> nodes
    # with any href attribute that are subnodes of <h3> tags that have a class of 'r'
    links = br.find_elements_by_xpath("//h3[@class='r']/a[@href]")
    results = []
    for link in links:
        title = link.text
        url = link.get_attribute('href')
        title_url = title + ' ; ' + url
        title_url = title_url.encode('utf8', 'ignore')
        results.append(title_url)
    return results

def scrape_the_count(br):
    count_txt = br.find_elements_by_xpath("//div[@id='resultStats']")[0].text
    count = count_txt.split()[1]
    return count

def scrape_keyword_count(keyword, useragent_list, url, result_dir):
    br = start_browser(useragent_list)
    print url
    br.get(url)
    time.sleep(random.randint(5,10))
    if 'sorry/IndexRedirect'  in br.current_url or '400' in br.title:
        br.quit()
        return None
    else:
        count = scrape_the_count(br)
        keyword_count = keyword + ' ; ' + count
        br.quit()
    return keyword_count

def scrape_keyword_result(keyword, useragent_list, start_url, result_dir):
    br = start_browser(useragent_list)
    br.get(start_url)
    all_result_list = []
    if 'sorry/IndexRedirect'  in br.current_url or '400' in br.title:
        br.quit()
        return None
    else:
        result_list = scrape_the_page(br)
        all_result_list.extend(result_list)
        time.sleep(random.randint(5,10))
        while True:
            try:
                br.find_element_by_id('pnnext')
        # Google's next page button have id 'pnnext'
        # if we can not find it. we should have get all the pages
            except NoSuchElementException:
                break
            else:
                br.find_element_by_id('pnnext').click()
                result_list = scrape_the_page(br)
                all_result_list.extend(result_list)
                time.sleep(random.randint(5,10))
        save_result_to_file(keyword, all_result_list, result_dir)
        br.quit()
        return True

# we save all result in the sub-dir 'keyword-result'
def save_result_to_file(keyword, result_list, result_dir):
    file_name = keyword  + '.txt'
    if not os.path.exists(result_dir):
        os.makedirs(result_dir)
    result_file = os.path.join(result_dir, file_name)
    results = '\n'.join(result_list)
    with open(result_file, 'w') as f:
        f.write(results)

def crawl_all_keyword(keywords_list, keywords_remain, google_adds, useragent_list, \
        result_dir):
    google_adds_list = conv_to_list(google_adds)
    # Get a copy of the keywords_list
    # Or something will get wrong when removing item from it
    for k in keywords_list[:]:
        google_add = random.choice(google_adds_list)
        start_url = make_up_url(google_add, k)
        keyword_result =  scrape_keyword_result(k, useragent_list, start_url, result_dir)
        while not keyword_result:
            google_add = random.choice(google_adds_list)
            start_url = make_up_url(google_add, k)
            keyword_result =  scrape_keyword_result(k, useragent_list, start_url, result_dir)
        print '%s Finish. Removeing it from the list' % k
        keywords_list.remove(k)
        with open(keywords_remain, 'w') as f:
                f.write('\n'.join(keywords_list))

def crawl_all_keyword_count(keywords_list, keywords_remain, google_adds, useragent_list, \
        result_dir):
    google_adds_list = conv_to_list(google_adds)
    count_file = os.path.join(result_dir, 'keyword_state.txt')
    for k in  keywords_list[:]:
        google_add = random.choice(google_adds_list)
        url = make_up_url(google_add, k, False)
        keyword_count = scrape_keyword_count(k, useragent_list, url, result_dir)
        while not keyword_count:
            google_add = random.choice(google_adds_list)
            url = make_up_url(google_add, k, False)
            keyword_count = scrape_keyword_count(k, useragent_list, url, result_dir)
        print '%s Finish. Removeing it from the list' % k
        keywords_list.remove(k)
        with open(keywords_remain, 'w') as f:
            f.write('\n'.join(keywords_list))
        with open(count_file, 'a') as c:
            c.write(keyword_count)
            c.write('\n')
