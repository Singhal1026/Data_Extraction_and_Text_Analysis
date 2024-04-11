# importing required liberaries

import os
import string
import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
import nltk
from nltk.corpus import stopwords
nltk.download('punkt')
nltk.download('stopwords')
import re



data = pd.read_excel('Input.xlsx')



# Fetching data from URLs using BeautifulSoup
# Storeing data in local directory named as "Extracted_articles"

url_id_not_found = []

for url, url_id in zip(data['URL'], data['URL_ID']):
    try:
        response = requests.get(url)
        response.raise_for_status() 
        
        soup = BeautifulSoup(response.text, 'lxml')
        
        title = soup.find('title')
        
        post_content = soup.find('div', class_='td-post-content')
        
        content = ''
        for i in post_content.find_all('p'):
            content += ' ' + i.text
        
    except requests.exceptions.RequestException as e:
        print(f'URL with url_id - {url_id} not Found.')
        url_id_not_found.append(url_id)
        
    except AttributeError as e:
        print(f'Attribute Error at URL with url_id - {url_id}')
        url_id_not_found.append(url_id)
        
    else:
        path = 'Extracted_articles'
        if not os.path.exists(path):
                os.mkdir(path)
        file_path = os.path.join(path, f'{url_id}.txt')
        if not os.path.exists(file_path):
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(f'{title.text}\n{content}')



# loading all stopwords from StopWords Directory and storing it in common list

stop_word = []
for file in os.listdir('StopWords'):
    with open(os.path.join('StopWords', file), 'r') as f:
        for line in f.readlines():
            stop_word.append(line.strip().split('|')[0].strip().lower())
stop_word = set(stop_word)



# Loading all positive and Negative words from MasterDictionary Directory and storing it in different list

pos = []
neg = []
for file in os.listdir('MasterDictionary'):
    with open(os.path.join('MasterDictionary', file), 'r') as f:
        if file == 'positive-words.txt':
            pos.extend(f.read().splitlines())
        else:
            neg.extend(f.read().splitlines())



# Loading scrapped data from local directory 
# Calculating few required Features

articles = []
tokenized_articles = []
positive_score = []
negative_score = []
subjectivity_score = []
polarity_score = []

for file in os.listdir('Extracted_articles'):
    with open(os.path.join('Extracted_articles', file), 'r', encoding='utf-8') as f:
        text = f.read()
        articles.append(text)

for text in articles:
    words = nltk.word_tokenize(text)
    tokenized_articles = [word for word in words if word.lower() not in stop_word]
    p_count = sum([1 for word in tokenized_articles if word.lower() in pos])
    n_count = sum([-1 for word in tokenized_articles if word.lower() in neg])*-1
    subjectivity_score.append((p_count+n_count)/((len(tokenized_articles)) + 0.000001))
    polarity_score.append((p_count-n_count)/((p_count+n_count) + 0.000001))
    positive_score.append(p_count)
    negative_score.append(n_count)



# Calculatoin rest of the Features

stop_words = stopwords.words('english')
exclude = string.punctuation


def find(text):
    # removing pucntuation
    new_text = text.translate(str.maketrans('','',exclude))
    
    # word tokenizing
    new_text = nltk.word_tokenize(new_text)
    
    # removing stop_words
    words = [word for word in new_text if word.lower() not in stop_words]
    total_words = len(words)                              # WORD COUNT
    
    # sentence tokenization
    sentences = nltk.sent_tokenize(text)
    total_sentences = len(sentences)
    avg_len_of_sen = total_words/total_sentences          # AVG SENTENCE LENGTH 
    
    # Finding complex words count, syllable count, syllable word count
    complex_words = 0                                     # COMPLEX WORD COUNT
    syllable_cnt = 0
    syllable_wrd_cnt = 0
    for word in words:
        if word.endswith('es'):
            word = word[:-2]
        if word.endswith('ed'):
            word = word[:-2]
        cnt = 0
        flag = True
        for i in word.lower():
            if i in 'aeiou':
                if flag:
                    flag = False
                    syllable_wrd_cnt+=1
                syllable_cnt+=1
                cnt+=1
        if cnt>2:
            complex_words+=1
    
    complex_words_in_pct = complex_words/total_words      # PERCENTAGE OF COMPLEX WORDS
    fi = 0.4 * (avg_len_of_sen+complex_words_in_pct)      # FOG INDEX
    avg_no_of_wrds_per_sen = total_words/total_sentences  # AVG NUMBER OF WORDS PER SENTENCE
    syll_per_wrd = syllable_cnt/syllable_wrd_cnt          # SYLLABLE PER WORD
    
    total_char = sum([len(word) for word in words])
    avg_wrd_len = total_char/total_words                  # AVG WORD LENGTH
    
    return [avg_len_of_sen, complex_words_in_pct, fi, avg_no_of_wrds_per_sen, complex_words, total_words, syll_per_wrd, avg_wrd_len]
    
def count_personal_pronouns(text):
    # regex pattern to match personal pronouns
    pattern = r'\b(?:I|we|my|ours|us)\b'

    matches = re.findall(pattern, text, flags=re.IGNORECASE)

    # exclude "US" as a country name
    country_pattern = r'\b(?:US)\b'
    country_matches = re.findall(country_pattern, text, flags=re.IGNORECASE)
    for country_match in country_matches:
        matches = [match for match in matches if match != 'US']

    # Count the number of matches
    count = len(matches)
    return count



avg_sentence_length = []
Percentage_of_complex_words = []
Fog_index = []
Avg_no_of_words_per_sentence = []
word_count = []
complex_word_count = []
personal_pronoun_count = []
syllable_per_word = []
avg_word_len = []


# Function calling for each arcicle to calculate required features

for text in articles:
    lst = find(text)
    avg_sentence_length.append(lst[0])
    Percentage_of_complex_words.append(lst[1])
    Fog_index.append(lst[2])
    Avg_no_of_words_per_sentence.append(lst[3])
    word_count.append(lst[5])
    complex_word_count.append(lst[4])
    syllable_per_word.append(lst[6])
    avg_word_len.append(lst[7])
    personal_pronoun_count.append(count_personal_pronouns(text))



# read "Output Data Structure.xlsx" File

output = pd.read_excel('Output Data Structure.xlsx')



# drop rows for which url not found

output = output[~output['URL_ID'].isin(url_id_not_found)]



# replacing data with calculated data

output['POSITIVE SCORE'] = positive_score
output['NEGATIVE SCORE'] = negative_score
output['POLARITY SCORE'] = polarity_score
output['SUBJECTIVITY SCORE'] = subjectivity_score
output['AVG SENTENCE LENGTH'] = avg_sentence_length
output['PERCENTAGE OF COMPLEX WORDS'] = Percentage_of_complex_words
output['FOG INDEX'] = Fog_index
output['AVG NUMBER OF WORDS PER SENTENCE'] = Avg_no_of_words_per_sentence
output['COMPLEX WORD COUNT'] = complex_word_count
output['WORD COUNT'] = word_count
output['SYLLABLE PER WORD'] = syllable_per_word
output['PERSONAL PRONOUNS'] = personal_pronoun_count
output['AVG WORD LENGTH'] = avg_word_len



# save output as csv file

output.to_csv('Output_Data.csv')

