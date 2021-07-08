# -*- coding: utf-8 -*-
"""
Created on Wed Jul  7 10:17:07 2021

@author: Mehak
"""
import config
import streamlit as st
from streamlit_web_data import *
from audio_transcription import apply_transcription
from text_processing import apply_text_correction
from keyword_generation import apply_keyword_generation
from video_generation import generate_short_videos

st.header("Swamped with piles of unwatched and disregarded long videos?")
st.title("Use our AI powered platform to turn your hour long videos into short-form videos within minutes")
video_file = st.file_uploader("Upload Video", type=['mp4'])

if video_file is not None:  
    with open(config.FILE_PATH + video_file.name, 'wb') as f:
        f.write(video_file.getbuffer())
           
    long_video = open(config.FILE_PATH + video_file.name, 'rb')
    video = long_video.read()
    st.video(video)
    
    with st.spinner('Please wait a few minutes while we process the video...'):
        if 'word_ts' not in st.session_state and 'audio_trans' not in st.session_state:
            st.session_state.word_ts, st.session_state.audio_trans = apply_transcription(video_file.name)
        if 'punctuated_trans' not in st.session_state:
            st.session_state.punctuated_trans = apply_text_correction(st.session_state.audio_trans)
        if 'keyword_ts_dict' not in st.session_state:
            st.session_state.keyword_ts_dict = apply_keyword_generation(st.session_state.word_ts, st.session_state.punctuated_trans)            
    st.success('Done!') 
            
    cb_list = display_topic_para(st.session_state.keyword_ts_dict)
    st.write('\n')
    
    if st.button('Create Short Video', key = 'bt_create'):
        topic_list = video_button_click(cb_list)
        with st.spinner('Video creation in progress...'):
            short_videoname, srt = generate_short_videos(video_file.name, st.session_state.keyword_ts_dict, topic_list)
        st.success('Done!')
        
        short_video = open(config.FILE_PATH + short_videoname, 'rb')
        video_bytes = short_video.read()
        st.video(video_bytes)