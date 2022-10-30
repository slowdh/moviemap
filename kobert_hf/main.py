import time

import torch
from transformers import BertModel

from kobert_tokenizer import KoBERTTokenizer


device = "mps"
tokenizer = KoBERTTokenizer.from_pretrained('skt/kobert-base-v1')

# CPU
model = BertModel.from_pretrained('skt/kobert-base-v1')
text = "한국어 모델을 공유합니다."
inputs = tokenizer.batch_encode_plus([text])
input_ids = torch.tensor(inputs['input_ids'])
attention_mask = torch.tensor(inputs['attention_mask'])

tic = time.time()
out = model(input_ids=input_ids,
            attention_mask=attention_mask)
delay = time.time() - tic
print(f"CPU infer time: {delay}")


# GPU
model = BertModel.from_pretrained('skt/kobert-base-v1').to(device)
text = "한국어 모델을 공유합니다."
inputs = tokenizer.batch_encode_plus([text])
input_ids = torch.tensor(inputs['input_ids']).to(device)
attention_mask = torch.tensor(inputs['attention_mask']).to(device)

tic = time.time()
out = model(input_ids=input_ids,
            attention_mask=attention_mask)
delay = time.time() - tic
print(f"MPS GPU infer time: {delay}")
