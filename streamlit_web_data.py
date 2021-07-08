# -*- coding: utf-8 -*-
"""
Created on Wed Jul  7 10:28:41 2021

@author: Mehak
"""
import streamlit as st

value = True

def display_topic_para(keyword_dict):
    cb_list = []
    st.subheader("Your video has below key highlights in the content. Please select(max. 4) the ones you want to include:")
    for i in range(len(keyword_dict)):
        kw = keyword_dict[i]['keywords']
        topic_text  = ' * '.join([word for word in kw if len(word.split()) > 1]).title()
        para = keyword_dict[i]['para']
        st.write('\n\n')
        first,last = st.beta_columns([0.5,3])
        cb = first.checkbox(' ', False, key= f'{i}')
        cb_list.append(cb)
        with last.beta_expander(topic_text):
            st.write(para)

    return cb_list

def video_button_click(cb_list):
    topic_list = []
    for i in range(len(cb_list)):
        if cb_list[i]:
            topic_list.append(i)
    return topic_list

def check_cbcount(cb_list):
    count=0
    for cb in cb_list:
        if cb:
            count+=1
    if count > 4:
        st.error("More than 4 topics not allowed! Please review selection.")
        return False
    return True
        
