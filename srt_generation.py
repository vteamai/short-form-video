# -*- coding: utf-8 -*-
"""
Created on Tue Jul  6 09:42:57 2021

@author: Team AI
"""

import config
import datetime

def format_time(time):
    formatted_time = datetime.datetime(100,1,1,0,0,0)
    formatted_time = formatted_time + datetime.timedelta(seconds=time)
    return (formatted_time.strftime('%H:%M:%S,%f')[:-3])

def create_srt_format(block_number, text, start_time, end_time):
    start_time = str(start_time)
    end_time = str(end_time)
    srt = ''
    
    srt += str(block_number) + '\n'
    srt += start_time + ' --> '
    srt += end_time + '\n'
    srt += text + '\n\n'
    
    return srt
        
def create_srt(timestamps, segment_len, audio_filename):
    audioname = f"{audio_filename.split('.')[0]}.srt"
    block = 1
    j=0
    i=0
    srt_text = ''
    
    while i in range(len(timestamps)):
        text=''
        start = timestamps[i].get('start_ts')
        end = float(start) + segment_len
        word_end  = timestamps[i].get('end_ts')

        while float(word_end) < float(end):
            if j < len(timestamps):
                text += timestamps[j].get('word') + ' '
                word_end = timestamps[j].get('end_ts')
                j+=1
            else:
                break
        i=j
        format_start = format_time(start)
        format_end = format_time(word_end)
        srt_text += create_srt_format(block, text, format_start, format_end)
        text = ''
        block +=1
    
    with open(config.FILE_PATH + audioname, 'w') as file:
        file.seek(0)
        file.write(srt_text)
        file.truncate()
        
    srt_file = open(config.FILE_PATH + audioname, 'r').read()

    return srt_file