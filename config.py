# -*- coding: utf-8 -*-
"""
Created on Tue Jul  6 13:24:20 2021
@author: Team AI
"""

import datetime
import uuid, random, string
import torch
import tensorflow_hub as tf_hub
from punctuator import Punctuator
from gingerit.gingerit import GingerIt
from keybert import KeyBERT

TF_HUB_PATH = './models/silero-models-master'
TF_MODEL_PATH = './models/silero-stt'
PUNCTUATOR_PATH = './models/punctuator/Demo-Europarl-EN.pcl'

#Create day/datewise folder for video uploads
FILE_PATH = f"./files/{datetime.datetime.today().strftime('%y%m%d')}/"

# load provided utils using torch.hub for brevity
model, decoder, utils = torch.hub.load(repo_or_dir = TF_HUB_PATH, model='silero_stt', language='en', source='local')
(read_batch, split_into_batches, read_audio, prepare_model_input) = utils

# load the actual tf model
tf_model = tf_hub.load(TF_MODEL_PATH)

#Punctuator
punctuator = Punctuator(PUNCTUATOR_PATH)

#Spell check parser
parser = GingerIt()

#Keyword generator
kw_model = KeyBERT('distilbert-base-nli-mean-tokens')

#Create unique IDs for the video/audio files
def generate_uid():
    #uid1 = str(uuid.uuid4())[:8]
    a = string.ascii_lowercase + string.digits
    uid = ''.join(random.choices(a, k=8))
    return uid