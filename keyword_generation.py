# -*- coding: utf-8 -*-
"""
Created on Mon Jul  5 23:02:09 2021

@author: Team AI
"""

import config
from nltk.tokenize import sent_tokenize

def correct_timestamp_entry(ts_copy, punctuated_text):
    trans_words = punctuated_text.split(" ")
    
    if len(ts_copy) > len(trans_words):
        time_stamp_length = len(ts_copy) - len(trans_words)
        count = 0
        for i in range(len(ts_copy)):
            if len(ts_copy[i]['word']) == 1:
                ts_copy.pop(i)
                count+=1
                if count == time_stamp_length:
                    break
    elif len(ts_copy) < len(trans_words):
        time_stamp_length = len(trans_words) - len(ts_copy)
        count = 0
        for i in range(len(ts_copy)):
            if len(ts_copy[i]['word']) == 1:
                start_ts = round(ts_copy[i]['start_ts'] + 0.10,2)
                end_ts = round(ts_copy[i]['end_ts'] + 0.10,2)
                ts_copy.insert(i+1,{'word': ' ', 'start_ts': start_ts, 'end_ts': end_ts})
                count+=1  
                if count == time_stamp_length:
                    break

    for i in range(len(trans_words)):
        ts_copy[i]['word'] = trans_words[i]
                    
    return ts_copy

def break_trans_into_para(trans):
    split_sentences = sent_tokenize(trans)
    para_list = []
    para = ''
    para_len=0

    for i in range(0,len(split_sentences)):
        word_len = len(split_sentences[i].split())
        para_len +=word_len
        if para_len <= 60:
            para += ' ' + split_sentences[i]
        elif para_len > 60:
            para_list.append(para.strip())
            para_len = word_len
            para = split_sentences[i]
        if i == len(split_sentences)-1:
            para_list.append(para.strip())

    return para_list

def extract_keywords(para):
    keywords = []
    topics = config.kw_model.extract_keywords(para, keyphrase_ngram_range=(1, 2), stop_words='english', use_mmr=True, diversity=0.7)
    keywords = [t[0] for t in topics]
        
    return keywords

def create_paragraph_timestamps(word_trans, paragraph_list):
    index = 0
    topic_timestamps = []
    word_trans_copy = word_trans
    
    for i in range(len(paragraph_list)):
        len_para = len(paragraph_list[i].split())
        ts_start = word_trans_copy[index]['start_ts']
        ts_end = word_trans_copy[index + len_para - 1]['end_ts']
        kw = extract_keywords(paragraph_list[i])
        topic_timestamps.append({'para': paragraph_list[i], 'start_ts': ts_start, 'end_ts': ts_end, 'keywords': kw})
        index += len_para
        
    return topic_timestamps

def apply_keyword_generation(word_timestamp, punctuated_trans):
    corrected_ts = correct_timestamp_entry(word_timestamp, punctuated_trans)
    para_list = break_trans_into_para(punctuated_trans)
    keyword_ts_dict = create_paragraph_timestamps(corrected_ts, para_list)
    
    return keyword_ts_dict