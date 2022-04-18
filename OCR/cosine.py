import re
import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import wordnet
from numpy import dot
from numpy.linalg import norm
import math



nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')
nltk.download('omw')


def cosineAnswer(correct_answer,submitted_answer):
    line=correct_answer
    line1=submitted_answer
    def Word_POS(word):
        tag = nltk.pos_tag([word])[0][1][0].upper()
        tag_dict = {"J": wordnet.ADJ,
                    "N": wordnet.NOUN,
                    "V": wordnet.VERB,
                    "R": wordnet.ADV}
        return tag_dict.get(tag, wordnet.NOUN)
    lemmatizer = WordNetLemmatizer()
    word_count={}
    def PreProcessing(line):
        line = line.lower()
        tokenized_word=word_tokenize(line)
        
        redundantchar=['@','#','!',"%",":",";","/","'",".",",","*","$","...","-","(",")"]
        stop_words =set(stopwords.words("english"))
        lemmatized_words=[]
        filteredwords=[]
        for word in tokenized_word:
            if word not in stop_words and word not in redundantchar:
                filteredwords.append(word)
        
        for word in filteredwords:
            lemmatized_words.append(lemmatizer.lemmatize(word, Word_POS(word)))
            
        for word in lemmatized_words:
            if word not in word_count.keys():
                word_count[word] = 1
            else:
                word_count[word] += 1  
        
        return lemmatized_words
    def vectorize(ans1):
        vector=[]
        for word in word_count:
            vector.append(ans1.count(word))
        return vector
    def Cos_Sim(correct_ans1,ans1):
        a = vectorize(ans1)
        b = vectorize(correct_ans1)
        cos_sim = dot(a, b)/(norm(a)*norm(b))
        return cos_sim
    #Preprocessing of Answers
    Correct_Ans = PreProcessing(line)
    Ans1 = PreProcessing(line1)
    a = vectorize(Ans1)
    b = vectorize(Correct_Ans)
    cos_sim = dot(a, b)/(norm(a)*norm(b))
    return cos_sim
