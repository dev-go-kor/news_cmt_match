from django.urls import path
from . import views

urlpatterns = [
    path('', views.news_list_page, name='news_list_page'),
    path('news/<pk>/', views.news_page, name='news_page'),
    path('cmt/<pk>/', views.news_cmt_crawl, name='news_cmt_crawl'),
    path('wordcloud/<pk>/', views.cmt_wordcloud, name='cmt_wordcloud'),
    path('sentences/<pk>/', views.rep_sentences, name='rep_sentences'),
    path('analyze/<pk>/', views.news_analyze, name='news_analyze'),
]
"""
url(r'^post/(?P<pk>\d+)/$', views.news_detail, name='news_detail'),
url(r'^post/new/$', views.post_new, name='post_new'),
url(r'^post/(?P<pk>\d+)/edit/$', views.post_edit, name='post_edit'),
url(r'^operate/$', views.news_crawl, name='news_crawl'),
url(r'^cmt/(?P<pk>\d+)/$', views.cmt_crawl, name='cmt_crawl'),
url(r'^analyze/(?P<pk>\d+)/$', views.cmt_analyzer, name='cmt_analyzer'),
"""