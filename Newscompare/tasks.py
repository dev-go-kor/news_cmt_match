from __future__ import absolute_import, unicode_literals
from celery import shared_task
from .cmt_crawler import get_comment
from django.shortcuts import render, get_object_or_404, redirect
from django.conf import settings
from .models import News_list, News_analyze ,Comment_buffer
from .cmt_analyzer import make_wordcloud, make_rep_sentence
"""
from .views import get_ranking_news
from .models import Newslist


@shared_task
def operate_get_rangking_news():
    crawled_news = get_ranking_news()
    for row in range(len(crawled_news)):
        form = Newslist(url = crawled_news.iloc[row]['url'], section = crawled_news.iloc[row]['section'], title = crawled_news.iloc[row]['title'], thumbnail = crawled_news.iloc[row]['thumbnail'], date = crawled_news.iloc[row]['date'])
        form.save()
"""
@shared_task
def get_comment_celery(pk):
    news = get_object_or_404(News_list, pk=pk)
    if news.collect_cmt_naver == False:
        Comment_buffer.objects.filter(news=news, press='naver').delete()
        target_url = news.url_naver
        try:
            cmts = get_comment(target_url)
            for row in range(len(cmts)):
                form_cmt = Comment_buffer(news=news, cmt_text=cmts.iloc[row]['text'],cmt_recom=int(cmts.iloc[row]['recommend']),
                                   cmt_unrecom=int(cmts.iloc[row]['unrecommend']), press=cmts.iloc[row]['press'])
                form_cmt.save()
            news.collect_cmt_naver = True
            news.save()
            print('naver done')
        except:
            print('naver failed')

    if news.collect_cmt_daum == False:
        Comment_buffer.objects.filter(news=news, press='daum').delete()
        target_url = news.url_daum
        try:
            cmts = get_comment(target_url)
            for row in range(len(cmts)):
                form_cmt = Comment_buffer(news=news, cmt_text=cmts.iloc[row]['text'],cmt_recom=int(cmts.iloc[row]['recommend']),
                                   cmt_unrecom=int(cmts.iloc[row]['unrecommend']), press=cmts.iloc[row]['press'])
                form_cmt.save()
            news.collect_cmt_daum = True
            news.save()
            print('daum done')
        except:
            print('daum failed')
    return 'get_comment_celery done.'

@shared_task
def cmt_wordcloud_celery(pk):
    news = get_object_or_404(News_list, pk=pk)
    cmt_list_naver = Comment_buffer.objects.filter(news=news, press='naver')
    cmt_list_daum = Comment_buffer.objects.filter(news=news, press='daum')

    cmt_set_naver = ""
    cmt_set_daum = ""

    for cmt in cmt_list_naver:
        cmt_set_naver += cmt.cmt_text + "\n"
    for cmt in cmt_list_daum:
        cmt_set_daum += cmt.cmt_text + "\n"

    make_wordcloud(cmt_set_naver).to_file(settings.MEDIA_ROOT + "/wordcloud/wordcloud_naver_%s.png" % pk)
    worldcloud_naver = "/wordcloud/wordcloud_naver_%s.png" % pk

    make_wordcloud(cmt_set_daum).to_file(settings.MEDIA_ROOT + "/wordcloud/wordcloud_daum_%s.png" % pk)
    worldcloud_daum = "/wordcloud/wordcloud_daum_%s.png" % pk


    # News_analyze.objects.filter(news=news, portal='Naver').delete()
    try:
        form_naver_analyze = get_object_or_404(News_analyze, news=news, portal='Naver')
        # form_naver_analyze = News_analyze.objects.get(news=news, portal='Naver')
        # if form_naver_analyze:
        form_naver_analyze.word_cloud = worldcloud_naver
    # else:
    except:
        form_naver_analyze = News_analyze(news=news, portal='Naver', word_cloud=worldcloud_naver)
    form_naver_analyze.save()

    # News_analyze.objects.filter(news=news, portal='Daum').delete()
    try:
        form_daum_analyze = get_object_or_404(News_analyze, news=news, portal='Daum')
        # form_daum_analyze = News_analyze.objects.get(news=news, portal='Daum')
        # if form_daum_analyze:
        form_daum_analyze.word_cloud = worldcloud_daum
    # else:
    except:
        form_daum_analyze = News_analyze(news=news, portal='Daum', word_cloud=worldcloud_daum)
    form_daum_analyze.save()

    return 'cmt_wordcloud_celery done.'

@shared_task
def rep_sentences_celery(pk):
    news = get_object_or_404(News_list, pk=pk)
    cmt_list_naver = Comment_buffer.objects.filter(news=news, press='naver')
    cmt_list_daum = Comment_buffer.objects.filter(news=news, press='daum')

    cmt_set_naver=""
    cmt_set_daum=""

    for cmt in cmt_list_naver:
        cmt_set_naver += cmt.cmt_text + "\n"
    for cmt in cmt_list_daum:
        cmt_set_daum += cmt.cmt_text + "\n"

    print("rep_basic_done.")

    rep_naver = make_rep_sentence(cmt_set_naver)
    print("rep_naver")
    rep_daum = make_rep_sentence(cmt_set_daum)
    print("rep_daum")

    try:
        form_naver_analyze = get_object_or_404(News_analyze, news=news, portal='Naver')
    #form_naver_analyze = News_analyze.objects.get(news=news, portal='Naver')
    #if form_naver_analyze:
        form_naver_analyze.rep_cmt = rep_naver
    #else:
    except:
        form_naver_analyze = News_analyze(news=news, portal='Naver', rep_cmt=rep_naver)
    form_naver_analyze.save()

    try:
        form_daum_analyze = get_object_or_404(News_analyze, news=news, portal='Daum')
    #form_daum_analyze = News_analyze.objects.get(news=news, portal='Daum')
    #if form_daum_analyze:
        form_daum_analyze.rep_cmt = rep_daum
    #else:
    except:
        form_daum_analyze = News_analyze(news=news, portal='Daum', word_cloud=rep_daum)
    form_daum_analyze.save()

    return 'rep_sentences_celery done.'

@shared_task
def mul(x, y):
    return x * y


@shared_task
def xsum(numbers):
    return sum(numbers)