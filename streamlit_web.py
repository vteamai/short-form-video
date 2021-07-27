# -*- coding: utf-8 -*-
"""
Created on Wed Jul  7 10:17:07 2021
@author: Mehak
"""
import config, os
import streamlit as st
from streamlit_web_data import *
from audio_transcription import apply_transcription
from text_processing import apply_text_correction
from keyword_generation import apply_keyword_generation
from video_generation import generate_short_videos

st.header("Swamped with piles of unwatched and disregarded long videos?")
st.title("Use our AI powered platform to turn your hour long videos into short-form videos within minutes")
video_file = st.file_uploader("Upload Video", type=['mp4'])

# If folder doesn't exist, then create it.
if not os.path.isdir(config.FILE_PATH):
    os.makedirs(config.FILE_PATH)
    print('os')
    
if video_file is not None: 
    st.video(video_file)

    if 'uid' not in st.session_state and 'renamed_file' not in st.session_state:
        print('uid')
        st.session_state.uid = config.generate_uid()
        with open(config.FILE_PATH + video_file.name, 'wb') as f:
            f.write(video_file.getbuffer())
        st.session_state.renamed_file = f"{video_file.name.split('.')[0]}_{st.session_state.uid}.{video_file.name.split('.')[1]}"
        os.rename(config.FILE_PATH + video_file.name,config.FILE_PATH + st.session_state.renamed_file)
    
    with st.spinner('Please wait a few minutes while we process the video...'):
        print('main')
        if 'word_ts' not in st.session_state and 'audio_trans' not in st.session_state:
            st.session_state.word_ts, st.session_state.audio_trans = apply_transcription(st.session_state.renamed_file)
        if 'punctuated_trans' not in st.session_state:
            st.session_state.punctuated_trans = apply_text_correction(st.session_state.audio_trans)
        if 'keyword_ts_dict' not in st.session_state:
            st.session_state.keyword_ts_dict = apply_keyword_generation(st.session_state.word_ts, st.session_state.punctuated_trans)            
    st.success('Done!') 
            
    cb_list = display_topic_para(st.session_state.keyword_ts_dict)
    st.write('\n')
    
    if st.button('Create Short Video', key = 'bt_create'):
        print('video')
        topic_list = video_button_click(cb_list)
        with st.spinner('Video creation in progress...'):
            #short_videoname, srt = generate_short_videos(video_file.name, st.session_state.keyword_ts_dict, topic_list)
            short_videoname = generate_short_videos(st.session_state.renamed_file, st.session_state.keyword_ts_dict, topic_list)
        st.success('Done!')
        
        short_video = open(config.FILE_PATH + short_videoname, 'rb')
        video_bytes = short_video.read()
        st.video(video_bytes)