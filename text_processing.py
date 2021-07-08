# -*- coding: utf-8 -*-
"""
Created on Mon Jul  5 18:16:48 2021

@author: Team AI
"""
#importing 
import warnings
warnings.filterwarnings('ignore')
import re, config

def process_text(text):
    res=text
    re1 = re.findall(r"\w+\s\W\w+",res)
    re2 = re.findall(r"\w+'\s",res)
    
    for txt in re1:
        split_txt = (re.split("\s", txt))
        word = split_txt[0] + split_txt[1]
        res = res.replace(txt,word)
    
    for txt in re2:
        split_txt = (re.split("'", txt))
        word = split_txt[0] + ' '
        res = res.replace(txt,word)

    res = res.replace(" ' "," ")
    return res

def create_spellcheck_trans(text):
    parse_text = ''
    i=0
        
    while i < len(text):
        end = min(i+600, len(text))
        for j in range(end-1, i-1, -1):
            if text[j] == ' ':
                end = j
                break
        parse_text += config.parser.parse(text[i:end])['result'] + ' '
        i= end+1
        
    return parse_text

#Perform sentence puntuation and segmentation using punctuator
def apply_punctuation(text):
    punc_text = config.punctuator.punctuate(text)
    punc_text = punc_text.replace(',,',',')
    punc_text = punc_text.replace(',.','.')
    punc_text = punc_text.replace('.,','.')
    punc_text = punc_text.replace('..','.')
    punc_text = punc_text.replace(',?','?')
    punc_text = punc_text.replace('?,','?')
    
    return punc_text
    
def apply_text_correction(text):
    preprocess = process_text(text)
    spellcheck = create_spellcheck_trans(preprocess)
    result = apply_punctuation(spellcheck)
    return result