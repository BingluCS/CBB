import os
from transformers import AutoTokenizer, AutoModel
from torch import nn
import torch
from d2l import torch as d2l
from tqdm.auto import tqdm
import h5py
from torch.optim import Adam

class Wiki_book_Dataset(torch.utils.data.Dataset): 
    def __init__(self, train_path): 
        self.train_path=train_path
    
    def __len__(self): 
        # return the number of samples 
        return 3353*10_000
 
    def __getitem__(self, i):
        file_idx,content_idx = i//100_000,i%100_000
        inputm_path = self.train_path+'/inputm/inputm_%d.h5'%(file_idx)
        attm_path = self.train_path+'/attm/attm_%d.h5'%(file_idx)
        pred_path = self.train_path+'/pred/pred_%d.h5'%(file_idx)
        labels_path = self.train_path+'/label/label_%d.h5'%(file_idx)
        weight_path = self.train_path+'/weight/weight_%d.h5'%(file_idx)
        with h5py.File(inputm_path, 'r') as f:
            inputm =f['data'][content_idx]
        with h5py.File(attm_path, 'r') as f:
            attm =f['data'][content_idx]
        with h5py.File(pred_path, 'r') as f:
            pred =f['data'][content_idx]
        with h5py.File(labels_path, 'r') as f:
            label =f['data'][content_idx]
        with h5py.File(weight_path, 'r') as f:
            weight =f['data'][content_idx]
        inputm_t = torch.tensor(inputm)
        attm_t = torch.tensor(attm)
        pred_t = torch.tensor(pred)
        label_t = torch.tensor(label)
        weight_t = torch.tensor(weight)

        #return 1,2
        return inputm_t,attm_t,pred_t,label_t,weight_t


def _get_batch_loss_bert(net, loss, vocab_size, tokens_X,
                         attention_mask,
                         pred_positions_X, mlm_weights_X,
                         mlm_Y):
    # forward
    mlm_Y_hat = net(tokens_X, attention_mask, pred_positions_X)
    # calculate losss
    mlm_l = loss(mlm_Y_hat.reshape(-1, vocab_size), mlm_Y.reshape(-1)) *\
    mlm_weights_X.reshape(-1, 1)
    mlm_l = mlm_l.sum() / (mlm_weights_X.sum() + 1e-8)

    return mlm_l


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
    
    def unk(self):  
        return 100

class MaskLM(nn.Module):
    """BERT的掩蔽语言模型任务"""
    def __init__(self, vocab_size, num_hiddens, num_inputs=768, **kwargs):
        super(MaskLM, self).__init__(**kwargs)
        self.mlp = nn.Sequential(nn.Linear(num_inputs, num_hiddens),
                                 nn.ReLU(),
                                 nn.LayerNorm(num_hiddens),
                                 nn.Linear(num_hiddens, vocab_size))

    def forward(self, X, pred_positions):
        num_pred_positions = pred_positions.shape[1]
        pred_positions = pred_positions.reshape(-1)
        # print(type(X))
        batch_size = X.shape[0]
        batch_idx = torch.arange(0, batch_size)
        batch_idx = torch.repeat_interleave(batch_idx, num_pred_positions)
        masked_X = X[batch_idx, pred_positions]
        masked_X = masked_X.reshape((batch_size, num_pred_positions, -1))
        mlm_Y_hat = self.mlp(masked_X)
        return mlm_Y_hat
    
class BERTModel(nn.Module):
    """BERT模型"""
    def __init__(self, models,vocab_size, num_hiddens=768, hid_in_features=768, mlm_in_features=768):
        super(BERTModel, self).__init__()
        self.encoder = models
        # self.hidden = nn.Sequential(nn.Linear(hid_in_features, num_hiddens),
        #                             nn.Tanh())
        self.mlm = MaskLM(vocab_size, num_hiddens, mlm_in_features)

    def forward(self, tokens, attention_mask,pred_positions=None):
        encoded_X = self.encoder(tokens, attention_mask=attention_mask)['last_hidden_state']
        mlm_Y_hat = self.mlm(encoded_X, pred_positions)
        # 
        return mlm_Y_hat

def train(net, train_loader, learning_rate, num_steps,vocab_size):
    use_cuda = torch.cuda.is_available()
    device = torch.device("cuda" if use_cuda else "cpu")
    # loss 
    loss = nn.CrossEntropyLoss()
    optimizer = Adam(net.parameters(), lr=learning_rate)
    step = 0
    # timer = d2l.Timer()
    # animator = d2l.Animator(xlabel='step', ylabel='loss',
    #                         xlim=[1, num_steps], legend=['mlm', 'nsp'])
    # metric = d2l.Accumulator(3)
    if use_cuda:
        net = net.to(device)
        loss = loss.to(device)
    # train
    num_steps_reached =False 
    while step < num_steps and not num_steps_reached:
        for inputm,attm,pred,label,weight in tqdm(train_loader):
            inputm = inputm.to(device)
            attm = attm.to(device)
            pred = pred.to(device)
            label = label.to(device)
            weight = weight.to(device)
            optimizer.zero_grad()
            # timer.start()
            l = _get_batch_loss_bert(net, loss, vocab_size, inputm, attm, pred, weight, label)
            l.backward()
            optimizer.step()
            # timer.stop()
            # metric.add(l, inputm.shape[0],1)
            # animator.add(step + 1,metric[0] / metric[2])
            step += 1
            if step == num_steps:
                num_steps_reached = True
                break
           
    # print(f'loss {metric[0] / metric[2]:.3f}')
    # print(f'{timer.sum():.2f} ')

model = AutoModel.from_pretrained('bert-base-uncased')
train_path='wiki_book/'
vocab=Vocab('./vocab.txt')
net=BERTModel(models=model,vocab_size=len(vocab), num_hiddens=768, hid_in_features=768, mlm_in_features=768)
train_dataset=Wiki_book_Dataset(train_path)
train_loader = torch.utils.data.DataLoader(dataset=train_dataset, batch_size=16,num_workers=0,shuffle=True)

train(net,train_loader,learning_rate=0.0001,num_steps=1000,vocab_size=len(vocab))