import torch
from transformers import T5ForConditionalGeneration,T5Config,T5Tokenizer

t5_version = 't5-large'

config = T5Config.from_pretrained(t5_version)
tokenizer = T5Tokenizer.from_pretrained(t5_version)
model = T5ForConditionalGeneration.from_pretrained(t5_version,config=config)

model.save_pretrained('model')
