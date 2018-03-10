from django.shortcuts import render, get_object_or_404, redirect
from .models import News_list, News_analyze ,Comment_buffer
from.cmt_crawler import get_comment
from.cmt_analyzer import make_wordcloud, make_rep_sentence
from django.conf import settings
from .tasks import get_comment_celery, cmt_wordcloud_celery, rep_sentences_celery
# Create your views here.

def news_list_page(request):
    news_list = News_list.objects.order_by('-id').all()
    #news_analyze_list = News_list.news_analyze_set.all
    #리스트 볼때마다 기사들 댓글, 분석상태 점검 필요??? 너무과한가?
    return render(request, 'Newscompare/news_list_page.html', {'news_list': news_list})

def news_page(request, pk):
    news = get_object_or_404(News_list, pk=pk)
    news_analyze = News_analyze.objects.filter(news=news)
    #cloud = Newsanalyzer.objects.filter(news_id=pk)

    return render(request, 'Newscompare/news_page.html', {'news' : news, 'newsanalyze' : news_analyze})

def news_cmt_crawl(request, pk):
    get_comment_celery.delay(pk=pk)
    """
    news = get_object_or_404(News_list, pk=pk)
    if news.collect_cmt_naver == False:
        Comment_buffer.objects.filter(news=news, press='naver').delete()
        target_url = news.url_naver
        cmts = get_comment(target_url)
        for row in range(len(cmts)):
            form_cmt = Comment_buffer(news=news, cmt_text=cmts.iloc[row]['text'],cmt_recom=int(cmts.iloc[row]['recommend']),
                               cmt_unrecom=int(cmts.iloc[row]['unrecommend']), press=cmts.iloc[row]['press'])
            form_cmt.save()
        news.collect_cmt_naver = True
        news.save()
        print('naver done')

    if news.collect_cmt_daum == False:
        Comment_buffer.objects.filter(news=news, press='daum').delete()
        target_url = news.url_daum
        cmts = get_comment(target_url)
        for row in range(len(cmts)):
            form_cmt = Comment_buffer(news=news, cmt_text=cmts.iloc[row]['text'],cmt_recom=int(cmts.iloc[row]['recommend']),
                               cmt_unrecom=int(cmts.iloc[row]['unrecommend']), press=cmts.iloc[row]['press'])
            form_cmt.save()
        news.collect_cmt_daum = True
        news.save()
        print('daum done')
    """
    return redirect('news_list_page')

def news_analyze(request, pk):
    news = get_object_or_404(News_list, pk=pk)
    try:
        cmt_wordcloud_celery.delay(pk=pk)
        rep_sentences_celery.delay(pk=pk)
        news.analyzed = True # delay 로 worker에 넣어버리고 바로 돌아옴, 따라서 잘되든 못되는 본 줄이 실행됨
        news.save()
        print('analyzed')
    except:
        print('analyzing failed')
    return redirect('news_list_page')

def cmt_wordcloud(request, pk): # 워드클라우드 뿐만아니라 다른 분석툴도 다 하자, 단 오류 대비
    cmt_wordcloud_celery.delay(pk=pk)
    """
    news = get_object_or_404(News_list, pk=pk)
    cmt_list_naver = Comment_buffer.objects.filter(news=news, press='naver')
    cmt_list_daum = Comment_buffer.objects.filter(news=news, press='daum')

    cmt_set_naver=""
    cmt_set_daum=""

    for cmt in cmt_list_naver:
        cmt_set_naver += cmt.cmt_text + "\n"
    for cmt in cmt_list_daum:
        cmt_set_daum += cmt.cmt_text + "\n"

    make_wordcloud(cmt_set_naver).to_file(settings.MEDIA_ROOT+"/wordcloud/wordcloud_naver_%s.png" % pk)
    worldcloud_naver = "/wordcloud/wordcloud_naver_%s.png" % pk
    print(worldcloud_naver)
    make_wordcloud(cmt_set_daum).to_file(settings.MEDIA_ROOT+"/wordcloud/wordcloud_daum_%s.png" % pk)
    worldcloud_daum = "/wordcloud/wordcloud_daum_%s.png" % pk
    print(worldcloud_daum)

    #News_analyze.objects.filter(news=news, portal='Naver').delete()
    try:
        form_naver_analyze = get_object_or_404(News_analyze, news=news, portal='Naver')
    #form_naver_analyze = News_analyze.objects.get(news=news, portal='Naver')
        print("wc naver" +form_naver_analyze)
    #if form_naver_analyze:
        form_naver_analyze.word_cloud = worldcloud_naver
    #else:
    except:
        form_naver_analyze = News_analyze(news=news, portal='Naver', word_cloud=worldcloud_naver)
    form_naver_analyze.save()

    #News_analyze.objects.filter(news=news, portal='Daum').delete()
    try:
        form_daum_analyze = get_object_or_404(News_analyze, news=news, portal='Daum')
    #form_daum_analyze = News_analyze.objects.get(news=news, portal='Daum')
        print("wc daum" + form_daum_analyze)
    #if form_daum_analyze:
        form_daum_analyze.word_cloud = worldcloud_daum
    #else:
    except:
        form_daum_analyze = News_analyze(news=news, portal='Daum', word_cloud=worldcloud_daum)
    form_daum_analyze.save()
    """
    return redirect('news_page', pk=pk)
# 동작 확인 함, db 연결, store 저장, 윈도우에서는 두번 실행 안되니 리눅스로 전환

def rep_sentences(request, pk):
    rep_sentences_celery.delay(pk=pk)
    """
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
        print(form_naver_analyze)
    #if form_naver_analyze:
        form_naver_analyze.rep_cmt = rep_naver
    #else:
    except:
        form_naver_analyze = News_analyze(news=news, portal='Naver', rep_cmt=rep_naver)
    form_naver_analyze.save()

    try:
        form_daum_analyze = get_object_or_404(News_analyze, news=news, portal='Daum')
    #form_daum_analyze = News_analyze.objects.get(news=news, portal='Daum')
        print(form_daum_analyze)
    #if form_daum_analyze:
        form_daum_analyze.rep_cmt = rep_daum
    #else:
    except:
        form_daum_analyze = News_analyze(news=news, portal='Daum', word_cloud=rep_daum)
    form_daum_analyze.save()
    """
    return redirect('news_page', pk=pk)

def cmt_sentiment_analyze():
    # 차후 개발과제

    return 0

def clr_cmt(request):
    # 각 동작 완수한 경우 cmt db에서 제거하기
    return 0