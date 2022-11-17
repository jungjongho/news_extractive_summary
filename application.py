from flask import Flask, render_template, request
import numpy as np
import math
import itertools
from newspaper import Article
from collections import Counter
import pandas as pd
import re
from ho_function import summary_kkma, summary_split, summary_okt

app = Flask(__name__)


@app.route("/")
def hello():
    return render_template("hello.html")


@app.route('/post', methods=['GET','POST'])
def post():
    
    if request.method == 'POST':
        value = request.form['id_name']
        number = request.form['number']
        
        # url= value
        url = value
        vote=[]
        vote.append(summary_kkma(url))

        print('='*300)

        vote.append(summary_split(url))

        print('='*300)

        vote.append(summary_okt(url))

        print('='*300)

        # vote.append(summary_mecab(url))

        # print('='*300)

        # vote.append(summary_twitter(url))

        vote=list(itertools.chain.from_iterable(vote))
        vote=dict(Counter(vote))
        vote

        vote=sorted(vote.items(), key=lambda x: x[1], reverse=True)
        vote

        # url = 'https://n.news.naver.com/mnews/article/658/0000009208?sid=105'


        article = Article(url, language='ko')
        article.download()
        article.parse()
        text=article.text

        # text = re.sub(r"\n+", " ", text)
        # sentences = re.split("[\.?!]\s+", text)

        # print("sentences: ",sentences)

        # # sentences = kkma.sentences(sentences[0])

        # print('sentences_length: ', len(sentences))

        # print(sentences[0])
        # print(sentences[1])


        text = re.sub(r"\n+", " ", text)
        # sentences = re.split("[\.?!]\s+", text)

        split_sentence=[]

        for i in text.split('다.'):
            split_sentence.append(i + '다.')

        for idx in range(0, len(split_sentence)):
          # print(idx)
          if len(split_sentence[idx]) <= 10:
            split_sentence[idx-1] += (' ' + split_sentence[idx])
            split_sentence[idx] = ''


        data = []
        for sentence in split_sentence:
            if(sentence == "" or len(sentence) == 0):
                continue
            temp_dict = dict()
            temp_dict['sentence'] = sentence
            temp_dict['token_list'] = sentence.split() #가장 기초적인 띄어쓰기 단위로 나누자!

            data.append(temp_dict)

        df_news = pd.DataFrame(data) #DataFrame에 넣어 깔끔하게 보기
        df_news


        important=[]

        text_list=[]

        p=0
        for i in vote:
            if p==number:
                break

            important.append(i[0])
            p=p+1

        for index in sorted(important): # sorted 하는 이유는 원래 문장 순서에 맞춰 보여주기 위함
            # print(df_news['sentence'][index])
            # print('')
            text_list.append(df_news['sentence'][index])
            
            
            
        
    #     # return render_template('post.html', value = str(text_list)[1:-2])
        

    
    return render_template('post.html', value1 = "1. " + str(text_list[0]), value2="2. " + str(text_list[1]) , value3="3. " + str(text_list[2]) , overall=text)



if __name__ == "__main__":
    app.run(host='0.0.0.0')   #, port=int(sys.argv[1])
