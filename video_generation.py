# -*- coding: utf-8 -*-
"""
Created on Mon Jul  5 23:38:10 2021

@author: Team AI
"""

import config
from keyword_generation import correct_timestamp_entry
from srt_generation import create_srt
from audio_transcription import extract_audio, english_transcription
from text_processing import apply_punctuation
from moviepy.editor import VideoFileClip, concatenate_videoclips

def split_videos(videoname, topic_timestamps):
    # loading video
    clip = VideoFileClip(config.FILE_PATH + videoname)
    video_dict = {}

    for i in range(len(topic_timestamps)):
        # split into subclips as per timestamps
        subclip = clip.subclip(topic_timestamps[i]['start_ts'], topic_timestamps[i]['end_ts'])
        video_dict[str(i)] = subclip
        
    return video_dict

def create_videos_srt(user_topics, topic_video_dict, videoname):

    video_clips = [topic_video_dict[str(x)] for x in user_topics]
    
    #Merge the video clips
    short_video = concatenate_videoclips(video_clips)
    
    # showing final clip
    short_videoname = f"{videoname.split('.')[0]}_shortform.mp4"
    short_video.write_videofile(config.FILE_PATH + short_videoname)

    #generate transcription of final video
    final_audio = extract_audio(short_videoname)
    word_ts, video_trans = english_transcription(final_audio)
    video_trans = apply_punctuation(video_trans)
    word_ts = correct_timestamp_entry(word_ts, video_trans)
    srt_file = create_srt(word_ts, 4, final_audio)
    
    return short_videoname, srt_file

def generate_short_videos(videoname, topic_timestamps, user_topics):
    topic_video_dict = split_videos(videoname, topic_timestamps)
    short_videoname, srt_file = create_videos_srt(user_topics, topic_video_dict, videoname)
    
    return short_videoname, srt_file