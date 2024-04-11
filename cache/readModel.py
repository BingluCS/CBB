import torch
import json
from collections import deque
import numpy as np
import argparse

q=deque([])

class Wiki_book_Dataset(torch.utils.data.Dataset):
    def __init__(self, train_path,idd):
        self.train_path=train_path
        self.chunk = 10000
        self.id = idd

    def __len__(self):
        # return the number of samples
        return 3353*10_000


    def __getitem__(self, i):
        file_idx,content_idx = i//self.chunk,i%self.chunk
        if self.id == 1:
            if np.random.rand() < 0.2:
                file_idx = int(3353 * (0.2+0.8 * np.random.rand()))
            else :
                file_idx = int(3353 * 0.2 * np.random.rand())
        file = ['inputm_%d.h5'%(file_idx), 'attm_%d.h5'%(file_idx), 'pred_%d.h5'%(file_idx),\
                                        'label_%d.h5'%(file_idx), 'weight_%d.h5'%(file_idx)]
        # size = []
        # for i in range(len(file)):
        #     size.append(self.file_size[file[0]]['size'])

        return file


def train( train_loader, learning_rate, num_steps,bb_size,data_size):
    size, step = 0, 0
    num_steps_reached =False
    miss_num, hit_num, flush_num= 0, 0, 0 
    threshold = 1024 * 1024 * 1024 * bb_size
    while step < num_steps and not num_steps_reached:
        for file in train_loader:
            step += 1
            for i in range(len(file[0])):
                while size > threshold:
                    file_name =  q.popleft()
                    size -= data_size[file_name]['size']
                    flush_num += 1
                for j in range(len(file)):
                    if file[j][i] not in q:
                        miss_num += 1
                        q.append(file[j][i])
                        size += data_size[file[j][i]]['size']
                    else:
                        hit_num+=1

            # print(size,threshold,q)
            if step == num_steps:
                num_steps_reached = True
                break
    print(f'miss num: {miss_num}, hit num: {hit_num}, flush num: {flush_num}')
    print(f'cache git rate: {hit_num/(hit_num+miss_num)}')

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('json_file', type=str, 
                        help='the file information of datasets')
    parser.add_argument('mode', type=int, 
                        help='train mode: 0 is Random, 1 is Pareto principle')
    parser.add_argument('bb_size', type=int,
                        help='Burst Buffer size')
    parser.add_argument('num_steps', type=int,
                        help='train num steps')
    args = parser.parse_args()
    return args

if __name__=="__main__":
    args = main()
    with open(args.json_file, 'r') as f:
        data_size = json.load(f)
    train_path='wiki_book/'
    train_dataset=Wiki_book_Dataset(train_path,args.mode)
    train_loader = torch.utils.data.DataLoader(dataset=train_dataset, batch_size=16,num_workers=4,shuffle = True)
    train(train_loader,learning_rate=0.0001,num_steps=args.num_steps,bb_size=args.bb_size, data_size = data_size)




