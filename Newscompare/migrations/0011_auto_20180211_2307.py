# Generated by Django 2.0.1 on 2018-02-11 23:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Newscompare', '0010_auto_20180211_1025'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news_analyze',
            name='portal',
            field=models.CharField(blank=True, choices=[('Daum', 'Daum'), ('Naver', 'Naver')], max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='news_analyze',
            name='word_cloud',
            field=models.ImageField(blank=True, max_length=200, upload_to='wordcloud'),
        ),
        migrations.AlterField(
            model_name='news_list',
            name='section',
            field=models.CharField(choices=[('사회', '사회'), ('생활', '생활'), ('문화', '문화'), ('IT', 'IT'), ('경제', '경제'), ('정치', '정치'), ('세계', '세계'), ('기타', '기타')], max_length=10),
        ),
    ]
