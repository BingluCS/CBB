
from tqdm.auto import tqdm
from datasets import load_dataset
import re

dataset = load_dataset('sradc/chunked-wikipedia20220301en-bookcorpusopen',cache_dir='./datasets_ori/',split="train")

file_count=0
text_data = []
#save the original data
for sample in tqdm(dataset['text']):
    sample =re.sub(r'\s+',' ',sample.replace('\n', ' ')).strip()
    text_data.append(sample)
    if len(text_data) == 10000: 
        with open(f'dataset_txt/text_{file_count}.txt', 'w', encoding='utf-8') as fp: 
            fp.write('\n'.join(text_data))
        text_data=[]
        file_count += 1 