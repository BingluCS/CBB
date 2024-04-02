from transformers import AutoTokenizer, AutoModel
from torch import nn
import random
import linecache
from tqdm.auto import tqdm
from pprint import pprint
import h5py
import numpy as np
import os
os.environ["http_proxy"] = "http://192.168.104.45:7890"
os.environ["https_proxy"] = "http://192.168.104.45:7890"
tokenizer = AutoTokenizer.from_pretrained('bert-base-uncased')

def replace_mask(tokens,max_len):
    tokens = tokens.split(' ')
        # 为遮蔽语言模型的输入创建新的词元副本，其中输入可能包含替换的“<mask>”或随机词元
    mlm_input_tokens = [token for token in tokens]
    pred_positions_and_labels = []
    candidate_pred_positions = [i for i in range(len(tokens))]
    num_mlm_preds = max(1, round(max_len* 0.15))
    # 打乱后用于在遮蔽语言模型任务中获取15%的随机词元进行预测
    random.shuffle(candidate_pred_positions)
    for mlm_pred_position in candidate_pred_positions:
        if len(pred_positions_and_labels) >= num_mlm_preds:
            break
        masked_token = None
        # 80%的时间：将词替换为“<mask>”词元
        if random.random() < 0.8:
            masked_token = '[MASK]'
        else:
            # 10%的时间：保持词不变
           #if random.random() < 0.5:
            masked_token = tokens[mlm_pred_position]
            # 10%的时间：用随机词替换该词
            # else:
            #     masked_token = random.choice(vocab.idx_to_token)
        mlm_input_tokens[mlm_pred_position] = masked_token
        pred_positions_and_labels.append(
            (mlm_pred_position, tokens[mlm_pred_position]))
    return mlm_input_tokens, pred_positions_and_labels

#@save
def get_mlm_data_from_tokens(tokens,max_len):
    # candidate_pred_positions = []
    # # tokens是一个字符串列表
    # for i, token in enumerate(tokens):
    #     # 在遮蔽语言模型任务中不会预测特殊词元
    #     if token in ['<cls>', '<sep>']:
    #         continue
    #     candidate_pred_positions.append(i)
    # 遮蔽语言模型任务中预测15%的随机词元
    mlm_input_tokens, pred_positions_and_labels = replace_mask(tokens,max_len)
    pred_positions_and_labels = sorted(pred_positions_and_labels,
                                       key=lambda x: x[0])
    pred_positions = [v[0] for v in pred_positions_and_labels]
    mlm_pred_labels = [v[1] for v in pred_positions_and_labels]
    return " ".join(mlm_input_tokens), pred_positions," ".join(mlm_pred_labels)

class Vocab:
    def __init__(self,file):
        with open(file, 'r') as file:
            content = file.read()
        self.idx_to_token = content.split()
        self.token_to_idx = {token: idx
            for idx, token in enumerate(self.idx_to_token)}

    def __len__(self):
        return len(self.idx_to_token)
    
    def __getitem__(self,tokens):
        if not isinstance(tokens, (list, tuple)):
            return self.token_to_idx.get(tokens, self.unk)
        return [self.__getitem__(token) for token in tokens]
    
    def to_tokens(self, indices):
        if not isinstance(indices, (list, tuple)):
            return self.idx_to_token[indices]
        return [self.idx_to_token[index] for index in indices]
    
    def unk(self):  # 未知词元的索引为0
        return 100
# 使用空格分割字符串，得到单词列表
vocab=Vocab('./vocab.txt')
len(vocab)    
rand_num = [i for i in range(1, len(vocab)) if i not in (101, 102)]
def add_mask_and_label(input_ids):
    len_tokens=len(list(filter(lambda x: x != 0, input_ids)))

    num_mlm_preds = max(1, round(len_tokens* 0.15)-2)
    candidate_pred_positions=list(range(1,len_tokens-1))
    random.shuffle(candidate_pred_positions)

    pred_positions_and_labels=[]
    mlm_input_tokens=input_ids
    for mlm_pred_position in candidate_pred_positions:
        if len(pred_positions_and_labels) >= num_mlm_preds:
            break
        masked_token = None
        # 80%的时间：将词替换为“<mask>”词元
        if random.random() < 0.8:
            masked_token = 103
        else:
            # 10%的时间：保持词不变
            if random.random() < 0.5:
                masked_token = input_ids[mlm_pred_position]
            # 10%的时间：用随机词替换该词
            else:
                masked_token = random.choice(rand_num)
        pred_positions_and_labels.append(
            (mlm_pred_position,input_ids[mlm_pred_position]))
        mlm_input_tokens[mlm_pred_position] = masked_token
        #print(pred_positions_and_labels)
    return mlm_input_tokens,pred_positions_and_labels

def add_mask_and_label(input_ids):
    len_tokens=len(list(filter(lambda x: x != 0, input_ids)))

    num_mlm_preds = max(1, round(len_tokens* 0.15)-2)
    candidate_pred_positions=list(range(1,len_tokens-1))
    random.shuffle(candidate_pred_positions)

    pred_positions_and_labels=[]
    mlm_input_tokens=input_ids
    for mlm_pred_position in candidate_pred_positions:
        if len(pred_positions_and_labels) >= num_mlm_preds:
            break
        masked_token = None
        # 80%的时间：将词替换为“<mask>”词元
        if random.random() < 0.8:
            masked_token = 103
        else:
            # 10%的时间：保持词不变
            if random.random() < 0.5:
                masked_token = input_ids[mlm_pred_position]
            # 10%的时间：用随机词替换该词
            else:
                masked_token = random.choice(rand_num)
        pred_positions_and_labels.append(
            (mlm_pred_position,input_ids[mlm_pred_position]))
        mlm_input_tokens[mlm_pred_position] = masked_token
        #print(pred_positions_and_labels)
    return mlm_input_tokens,pred_positions_and_labels


file_count=0
text_data,pred,labels = [],[],[]
max_len=512
i=0
path='/home/ubutnu/hardDisk/DeepLearning/ww'
#front = [x.replace('\n', '').split(' ') for x in paragraphs[:10]]
# front = paragraphs[0].replace('\n', '')
mlm_input_tokens_all,pred_positions_all,mlm_pred_labels_all,weight_all,attention_mask_all = [],[],[],[],[]
for file_idx in tqdm(range(3353)):
    text_path = '/home/ubutnu/hardDisk/DeepLearning/wiki_txt'+'/text_%d.txt'%(file_idx)
    for content_idx in range(1,10001):
        text = linecache.getline(text_path,content_idx).strip()

        inputs = tokenizer(text,truncation=True,padding='max_length',max_length=max_len)
        input_ids,token_type_ids,attention_mask=inputs['input_ids'],inputs['token_type_ids'],inputs['attention_mask']

        mlm_input_tokens, pred_positions_and_labels  = add_mask_and_label(input_ids)
        
        pred_positions_and_labels = sorted(pred_positions_and_labels,
                                        key=lambda x: x[0])
        pred_positions = [v[0] for v in pred_positions_and_labels]
        mlm_pred_labels = [v[1] for v in pred_positions_and_labels]
        pred_positions.extend([0]*(512-len(pred_positions)))
        pred_positions = pred_positions[:70]
        mlm_pred_labels.extend([0]*(512-len(mlm_pred_labels)))
        mlm_pred_labels = pred_positions[:70]


        pred_positions_all.append(pred_positions)
        mlm_pred_labels_all.append(mlm_pred_labels)
        attention_mask_all.append(attention_mask)
        mlm_input_tokens_all.append(mlm_input_tokens)

    non_zero_counts = np.count_nonzero(pred_positions_all, axis=1)
    weight=np.zeros_like(pred_positions_all)
    for x, count in enumerate(non_zero_counts):
        weight[x, :count] = 1

    mlm_input_path = path+'/inputm/inputm_%d.h5'%(i)
    pred_path = path+'/pred/pred_%d.h5'%(i)
    label_path = path+'/label/label_%d.h5'%(i)
    attention_mask_path = path+'/attm/attm_%d.h5'%(i)
    weight_path = path+'/weight/weight_%d.h5'%(i)

    with h5py.File(mlm_input_path, 'w') as h5f:
        h5f.create_dataset('data', data=mlm_input_tokens_all) 
    with h5py.File(weight_path, 'w') as h5f:
        h5f.create_dataset('data', data=weight) 
    with h5py.File(attention_mask_path, 'w') as h5f:
        h5f.create_dataset('data', data=attention_mask_all) 
    with h5py.File(pred_path, 'w') as h5f:
        h5f.create_dataset('data', data=pred_positions_all) 
    with h5py.File(label_path, 'w') as h5f:
        h5f.create_dataset('data', data=mlm_pred_labels_all) 
    i+=1
    mlm_input_tokens_all,pred_positions_all,mlm_pred_labels_all,token_type_ids_all,attention_mask_all = [],[],[],[],[]

