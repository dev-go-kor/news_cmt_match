from django.db import models
# Create your models here.

class News_list(models.Model):
    SECTION_LIST = {('사회', '사회'), ('경제', '경제'), ('정치', '정치'), ('문화', '문화'), ('세계', '세계'), 
                    ('IT', 'IT'), ('생활', '생활'), ('기타', '기타')}

    title = models.CharField(max_length=200)
    press = models.CharField(max_length=200)
    section = models.CharField(choices=SECTION_LIST, max_length=10) # check displayed order on admin page
    url_naver = models.URLField()
    url_daum = models.URLField()
    thumbnail = models.URLField(blank=True) # char type field can use black=True, it store ''
    date = models.DateField()
    count_cmt_naver = models.IntegerField(blank=True, null=True)
    count_cmt_daum = models.IntegerField(blank=True, null=True)
    collect_cmt_naver = models.BooleanField(default=False)
    collect_cmt_daum = models.BooleanField(default=False)
    analyzed = models.BooleanField(default=False)

    gap_ratio = models.IntegerField(null=True,blank=True) # It should use Null=True Integer dosen't allow ''

    def __str__(self):
        return self.title

class News_analyze(models.Model):
    PORTAL_LIST = {('Naver','Naver'),('Daum','Daum')}

    news = models.ForeignKey(News_list, on_delete = models.CASCADE)
    word_cloud = models.ImageField(blank=True, max_length=200, upload_to='wordcloud')##additional setting required
    rep_cmt = models.CharField(blank=True, max_length=200) #representative comment
    positive_cmt = models.IntegerField(blank=True, null=True)
    negative_cmt = models.IntegerField(blank=True, null=True)
    neutral_cmt = models.IntegerField(blank=True, null=True)
    portal = models.CharField(choices=PORTAL_LIST, max_length=10, blank=True, null=True)

    def __str__(self):
        return_text = self.news.title + "/" + self.portal
        return return_text

class Comment_buffer(models.Model):
    news = models.ForeignKey(News_list, on_delete = models.CASCADE)
    press = models.CharField(max_length=100)
    cmt_text = models.TextField()
    #cmt_date = models.DateTimeField()
    cmt_recom = models.IntegerField()
    cmt_unrecom = models.IntegerField()
    def __str__(self):
        return_text = self.news.title + "/" + self.press
        return return_text



