import bisect
import itertools
import random

import nltk
from konlpy.corpus import kolaw
from konlpy.tag import Twitter #Mecab 안되서 Twitter로 바꿈


#고도화 필요
def generate_sentence(cfdist, word, max_len=20):
    sentence = []
    sentence.append(word)
    end_sign = 1
    end_list = ['.', 'ㅋ', 'ㅎ','?']
    del_list = ['(',')','-','/', '-(',',']
    # Generate words until we meet a period
    # word != (word.find('.') or word.endswith('다') or word.find('ㅋ') or word.find('ㅎ'))

    while end_sign :

        # Generate the next word based on probability # 171008 여기서부터 조금 더 고민해보자.
        # word 와 연결(연관) 상태의 단어들을 choices, 그의 가중치(정도)를 weights로 지정
        ########### 최적의 결과 단어당 1개만 도출방법 고안(현재는 렌덤으로 여러개 생성중
        cfdtmp = cfdist[word]
        for clr in del_list:
            del cfdtmp[clr]

        if cfdist[word] == {}:
            end_sign = 0
            break

        print(cfdtmp.items())

        choices, weights = zip(*cfdtmp.items())  # *는 unpank operator, cfdist[word].items()로 반환되는 dict를 묶어줌

        #cumdist = list(itertools.accumulate(weights))  # 왜 누적해서 리스트를 만들지?
        #tmp = cumdist[-1]
        #x = random.random() * tmp # 0~1까지 난수를 random으로 생성하여 cumdist에 곱함
        x = max(weights) # 최선값 용 생성
        #word2 = choices[bisect.bisect(cumdist, x)] # 이진검색(bisect)을 통해 x에 가장 가까운 애 추출
                                                  # 이럴경우 빈도가 높은 녀석이 선택될 확률이 높음. 무조건은 아님
        weights_list = list(weights) #Tuple 이라서, find가 안먹혀서 바꿈
        y = weights_list.index(x)
        word = choices[y] # 최선값 용 생성

        sentence.append(word) # 마지막 판별값 입력을 위해 맨 앞에서 여기로 이동.
        del_list.append(word)

        if len(sentence)>=max_len:
            end_sign = 0

        for end in end_list:
            if word.find(end) >= 0 :
                end_sign = 0
                break

    return ' '.join(sentence)

def calc_cfd(doc):
    # Calculate conditional frequency distribution of bigrams
    words = [w for w in Twitter().morphs(doc, norm=True)] #Mecab을 Twitter로, pos->morphs, 음절이 아닌 어절로
    bigrams = nltk.bigrams(words) #bigram에 대하여 공부(바료 옆과의 관계로 끝?
    return nltk.ConditionalFreqDist(bigrams)
