import h5py
import tqdm.auto as tqdm
import sys 

level = sys.argv[1]
oripath = './wiki_book'
compress_path = f'./wiki_bookzip{level}'
def ctoc(path,file_idx,level):
    with h5py.File(oripath+path+f'{file_idx}.h5', 'r') as f:
        data=f['data'][:]
    with h5py.File(compress_path+path+f'{file_idx}.h5', 'w') as new_file:
        new_file.create_dataset('data', data=data,compression='gzip', compression_opts=level)

for file_idx in tqdm(range(3353)):
    inputm_path = '/inputm/inputm_'
    attm_path = '/attm/attm_'
    pred_path = '/pred/pred_'
    labels_path = '/label/label_'
    weight_path = '/weight/weight_'
    ctoc(inputm_path,file_idx)
    ctoc(attm_path,file_idx)
    ctoc(pred_path,file_idx)
    ctoc(labels_path,file_idx)
    ctoc(weight_path,file_idx)