# BERT
## dataset download
note: need to have access to hugging face
```
mkdir $(pwd)/datasets_ori/
mkdir $(pwd)/dataset_txt/
. build.sh
python3 download_data.py
```
## process data
```
python3 Process.py
```
## compress data
```
python3 compress.py 3 //压缩等级
```
## running 
```
python3 BERT.py
```