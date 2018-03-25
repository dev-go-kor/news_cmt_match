from wordcloud import WordCloud
from konlpy.tag import Twitter
from collections import Counter

from .sentence_creator import calc_cfd, generate_sentence

def make_wordcloud(cmt_set):

    print("before nlp")
    nlp = Twitter()
    print("nlp = Twitter()")
    nouns = nlp.nouns(cmt_set)
    print("nouns = nlp.nouns(buff)")
    count = Counter(nouns)
    print("count = Counter(nouns)")
    word_cloud = WordCloud(font_path='./HoonWhitecatR.ttf', max_words=20, font_step=5, mode='RGBA',
                          background_color=None).generate_from_frequencies(count)
    print(word_cloud.words_)
    del(nlp, nouns, count) # to solve memory error, 'nlp' make error when it work more then one time
    return word_cloud #need to make save img and return location

def calculate_bias(cmt_set):
    # 텍스트 뭉치로 들어올꺼고
    # 일단은 '\n' 으로 구분되니깐 한줄한줄 긍정 부정 중립 판별해서 변수에 수량 카운트
    return 0

def make_rep_sentence(cmt_set):
    # 대표문장 만들기 3개
    print(cmt_set)
    nlp = Twitter()
    nouns = nlp.nouns(cmt_set)
    count = Counter(nouns)
    print("count done")

    cfd = calc_cfd(cmt_set)
    print("cfd done")

    top_morphs = list(count.keys())[0]


    print("top morps choosen : ", top_morphs)
    rep_sentences = generate_sentence(cfd, top_morphs)

    print(rep_sentences)
    return rep_sentences

def make_word_freq(cmt_set):
    # 단어 빈도 그래프 만드기
    # 모델도 건드려야함
    # 폴더도 워드클라우드랑 구별하지뭐
    return 0

