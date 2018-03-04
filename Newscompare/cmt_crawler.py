# -*- coding: utf-8 -*-
"""

author

def get_ranking_news()
    모바일 랭킹 뉴스 리스트 크롤링
def get_comment(url)
    해당 url에서 댓글 정보 크롤링
"""

import urllib.request
from urllib.parse import quote_plus
from bs4 import BeautifulSoup
import pandas as pd
import re
import time
from selenium import webdriver

def get_comment(url):
# later, if it's already crawled, check it's update
    if url.find('naver.com')>=0:
        PRESS = 'naver'
        print(PRESS)
        # for windows
        #driver = webdriver.PhantomJS(executable_path=r'C:\Users\dev\phantomjs\bin\Phantomjs.exe')
        # for linux
        driver = webdriver.PhantomJS(executable_path='/usr/local/bin/phantomjs')
        print(url)
        driver.get(url)
        print(driver.current_url)
        time.sleep(1)
        print('naver url get')
        """
        tmp_count = '댓글'

        while(tmp_count == '댓글'):
            print('loading....')
            tmp_str = driver.find_element_by_xpath(
                "//a[@class='media_end_head_cmtcount_button']").text.replace("," , "")
            tmp_count = int(re.findall('\d+',tmp_str)[0])
        comment_total = int(0 if tmp_count == "" else tmp_count)
        time.sleep(1)
        """
        comment_press = []
        comment_text = []
        #comment_date = []
        comment_recommend = []
        comment_unrecommend = []

        #if comment_total > 0:
        #    #driver.find_element_by_xpath("//a[@data-log='RPS.new']").click()
        #    #time.sleep(1)
        #    driver.find_element_by_xpath("//a[@class='u_cbox_btn_view_comment']").click()
        #    time.sleep(1)

        #    repeat = ((comment_total-1) // 20 if comment_total > 0 else 0)

            # later, need to upgrade to check end of click RPC.more
            # check existence

        try:
            driver.find_element_by_xpath("//a[@data-log='RPC.allmore']").click()
            time.sleep(1)
        except:
            print('no RPC.allmore')


        click_more = True
        while click_more: #update on main project
            try:
                driver.find_element_by_xpath("//a[@data-log='RPC.more']").click()
                print('clicked')
                time.sleep(1)
            except:
                click_more = False

        tmp = driver.find_elements_by_xpath("//div[@class='u_cbox_content_wrap']/ul[@class='u_cbox_list']/li[@*]")
        print('line count')
        print(len(tmp))
        for line in tmp:
            line_text = line.find_element_by_class_name("u_cbox_text_wrap").text
            # line_date = line.find_element_by_class_name("u_cbox_date").text
            try:
                line.find_element_by_class_name("u_cbox_ico_exclamation")  # to raise "NoSuchElementException"
                line_recommend = "0"
                line_unrecommend = "0"
                print("except case : " + line_text)
            except:
                line_recommend = line.find_element_by_class_name("u_cbox_cnt_recomm").text
                line_unrecommend = line.find_element_by_class_name("u_cbox_cnt_unrecomm").text

                print("correct case : " + line_text)
                comment_press.append(PRESS)
                comment_text.append(line_text)
                # comment_date.append(line_date)
                comment_recommend.append(line_recommend)
                comment_unrecommend.append(line_unrecommend)

            """
            try:
                line_recommend = line.find_element_by_class_name("u_cbox_cnt_recomm").text
                line_unrecommend = line.find_element_by_class_name("u_cbox_cnt_unrecomm").text
                


                print("correct case : " + line_text)
                comment_press.append(PRESS)
                comment_text.append(line_text)
                # comment_date.append(line_date)
                comment_recommend.append(line_recommend)
                comment_unrecommend.append(line_unrecommend)
            except:
                line_recommend = "0"
                line_unrecommend = "0"
                print("except case : " + line_text)
            """

    elif url.find('daum.net')>=0:
        PRESS = 'daum'
        print(PRESS)
        # driver = webdriver.PhantomJS(executable_path=r'C:\Users\dev\phantomjs\bin\Phantomjs.exe')
        driver = webdriver.PhantomJS(executable_path='/usr/local/bin/phantomjs')
        driver.get(url)
        time.sleep(1)
        """
        tmp_count = '댓글'

        while (tmp_count == '댓글'):
            print('loading....')
            tmp_str = driver.find_element_by_xpath(
                "//span[@class='alex-count-area']").text.replace(",", "")
            tmp_count = int(re.findall('\d+', tmp_str)[0])
        comment_total = int(0 if tmp_count == "" else tmp_count)
        time.sleep(1)
        """

        comment_press = []
        comment_text = []
        # comment_date = []
        comment_recommend = []
        comment_unrecommend = []
        """
        if comment_total > 0:
            repeat = (comment_total+6) // 10
            print("repeat : ")
            print(repeat)
        """

            #for i in range(repeat):
            #    driver.find_element_by_xpath("//a[contains(@class,'link_fold') and contains(@class,'#more')]").click()
                # mathod to select multiple class ex. class="link_fold #more"
            #    print('more clicked')
            #    time.sleep(1)
            #    #time.sleep(1)

        click_more = True
        while click_more: #update on main project
            try:
                driver.find_element_by_xpath("//a[contains(@class,'link_fold') and contains(@class,'#more')]").click()
                print('clicked')
                time.sleep(1)
            except:
                click_more = False

        tmp = driver.find_elements_by_xpath("//ul[@class='list_comment']/li[@*]")
        print('line count')
        print(len(tmp))
        for line in tmp:
            try:
                line_text = line.find_element_by_tag_name("p").text
                # try:
                line_tmp = line.find_element_by_class_name("comment_recomm").text.replace(",", "")
                line_recommend = int(re.findall('\d+', line_tmp)[0])
                # print(line_recommend)
                line_unrecommend = int(re.findall('\d+', line_tmp)[1])
                # print(line_unrecommend)
                # print("correct case : " + line_text)
                comment_press.append(PRESS)
                comment_text.append(line_text)
                # comment_date.append(line_date)
                comment_recommend.append(line_recommend)
                comment_unrecommend.append(line_unrecommend)
                print("correct case : " + line_text)
            except:
                print("emoticon?")

    return pd.DataFrame({'text' : comment_text, 'recommend' : comment_recommend, 'unrecommend' : comment_unrecommend, 'press' : comment_press } )

"""
def get_ranking_news():
    ranking_news_url = 'http://m.news.naver.com/rankingList.nhn'
    req = urllib.request.Request(ranking_news_url)
    urlopen = urllib.request.urlopen(req)
    status = urlopen.status

    if status == 200 :
        html = urlopen.read()
        soup = BeautifulSoup(html,'lxml')

        date_text = soup.find('div', class_='pg2 rank_pg2').strong.text
        date_re = re.compile(r'\d\d\d\d.\d\d.\d\d')
        date_search = date_re.search(date_text)
        date_get = date_search.group()
        date = date_get.translate({ord('.') : '-'})

        section_list = soup.find_all('div', class_='ranking_news')

        article_section = []
        article_title = []
        article_url = []
        article_thumbnail = []
        article_date = []

        for section in section_list:
            section_name = section.find('h2').text

            section_article = section.find_all('li')

            for list in section_article:
                title = list.find('div', class_='commonlist_tx_headline').text
                url = list.find('a')['href']
                try:
                    thumbnail = list.find('img')['src']
                except:
                    thumbnail = ""

                article_section.append(section_name)
                article_title.append(title)
                article_url.append('http://m.news.naver.com'+url)
                article_thumbnail.append(thumbnail)
                article_date.append(date)

    data_news_list = pd.DataFrame({'section' : article_section, 'title' : article_title, 'url' : article_url, 'thumbnail' : article_thumbnail,'date' : article_date})

    return data_news_list
"""