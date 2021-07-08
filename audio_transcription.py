# -*- coding: utf-8 -*-
"""
Created on Tue Jul  6 12:02:04 2021

@author: Team AI
"""
import config
import torch
import tensorflow as tf
import moviepy.editor as mp

def extract_audio(video_name):
    videofile = mp.VideoFileClip(config.FILE_PATH + video_name)
    audio_name = f"{video_name.split('.')[0]}.wav"
    videofile.audio.write_audiofile(config.FILE_PATH + audio_name)
    
    return audio_name
    
def english_transcription(audio_file):
    
    test_files = [config.FILE_PATH + audio_file] 
    batches = config.split_into_batches(test_files, batch_size=10)
    input = config.prepare_model_input(config.read_batch(batches[0]))
    wav_len = input.shape[1] / 16000
    
    #tf inference
    res = config.tf_model.signatures["serving_default"](tf.constant(input.numpy()))['output_0']
    decoded_text = config.decoder(torch.Tensor(res.numpy())[0])
    decoded_words = config.decoder(torch.Tensor(res.numpy())[0], wav_len, word_align=True)[-1]
    
    return decoded_words, decoded_text 

def apply_transcription(video_name):
    audio = extract_audio(video_name)
    timestamp, transcription = english_transcription(audio)
    return timestamp, transcription 