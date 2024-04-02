# Cache hit rate test

## Model
readModel.py is a simplified model for obtaining cache hit rates between gzip compression, raw data and CBB without actually training the neural network.

The file information of the English wikitext and Toronto Book Corpus datasets is stored to json file

### Usage:
```
python3 readModel.py ori_info.json 0 10 1000
```

## Real Applications
```
cd BERT
```