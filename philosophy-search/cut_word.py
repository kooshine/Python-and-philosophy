#coding:utf-8

import jieba
import jieba.analyse
import pandas as pd
import numpy as np
from PIL import Image
from wordcloud import WordCloud     #https://www.lfd.uci.edu/~gohlke/pythonlibs/#wordcloud   下载wheel包，安装
import matplotlib.pyplot as plt
#下面两句解决图形中不显示中文的问题
plt.rcParams['font.sans-serif']=['SimHei']
plt.rcParams['axes.unicode_minus']=False
import matplotlib
from collections import Counter

def set_cloud(book_abstract):
    img = np.array(Image.open('cat.jpg'))
    font_path='Monaco Yahei.ttf'

    
    abstract = ""
    for item in book_abstract:
        abstract += item
    pic_cloud = WordCloud(scale=4,mask=img, font_path=font_path,background_color='white', max_words=400,max_font_size=100,random_state=24).generate(abstract)
    
    plt.imshow(pic_cloud)
    plt.axis('off')
    plt.show()
    pic_cloud.to_file('result.jpg')

def get_top_words(book_abstract):
    #print (book_abstract)
    #读取停用词表
    stop_words_f = open('stop_words_ch.txt','r')
    stopwords_list = []
    for line in stop_words_f.readlines():
        stopwords_list.append(line.strip())
    abstract_word =[]
    for item in book_abstract:
        #去停用词
        item = item.split(" ")
        for word in item:
            if word not in stopwords_list and word.isdigit() == False:
                abstract_word.append(word)
    #获取出现频次最高的1000词
    word_counts = pd.value_counts(abstract_word).head(50)
    print (word_counts)
    word_list = list(word_counts.head(100).index)
    print (word_list)
    #生成高频词柱状图
    bins = 10       #bins代表y轴间距   
    #chinfo = matplotlib.font_manager.FontProperties(fname='Monaco Yahei.ttf')
    word_counts.plot(kind='barh', color='#607c8e', alpha=0.5)
    plt.ylabel('Top words(50)')
    #plt.xticks(word_list)
    plt.xlabel('Reference times')
    plt.title('What is Philosophy')
    plt.grid(True)
    plt.show()

def get_title(obj_tables):
    f = open('book_title.txt','a+',encoding='utf-8')
    book_name = []

    for i in obj_tables.iloc[:,1]:
        i = i.replace('\n','').replace('\r','').replace(' ', '')
        print (i)
        book_name.append(i)
        f.write(i)
        f.write('\n')
    
    f.close()
    return book_name

def get_abstract(obj_tables):
    abstract = []
    for i in obj_tables.iloc[:,2]:
        try:
            i = i.replace('\n','').replace('\r','').replace(' ', '')
            print (i)
            item = jieba.cut(i)
            abstract.append(' '.join(item))
        except:
            print ('no abstract')

    return abstract

if __name__ == "__main__":
    obj_tables = pd.read_csv('book.csv', encoding='utf-8',header=None)      #header=None 表示不把第一行作为列索引

    #book_name = get_title(obj_tables)
    abstract = get_abstract(obj_tables)
    print (abstract)
    #set_cloud(abstract)
    get_top_words(abstract)