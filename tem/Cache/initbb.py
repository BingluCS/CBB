import subprocess
import json


PFS = "/root/HPC/PFS/nocompress/"
BB0 = "/root/HPC/BB/nocompress/"
#BB1 = '/root/HPC/BB/nocompress/'

#file_json = "/root/HPC/Cache/file_cache_nocompress.json"
threshold =   1024*1024*1024*20

def init_bb(BB1,file_json):
    command = "ls -d " + BB1 + '* | grep -v \'^' + BB1+ 'bk_\' ' + '| grep -v \'old\' '
    result = subprocess.run(command,shell=True, capture_output=True, text=True)
    file = result.stdout.strip().replace('\n', ' ')
    print(command)
    if len(file) != 0:
        # file = ['BB' + item for item in file]
        command = "du -csb " + file
        result = subprocess.run(command,shell=True, capture_output=True, text=True)
        output = result.stdout.strip().split()
    else:
        output = ['0','total']
    
    with open(file_json, 'r') as F:
        data = json.load(F)
    file = file.replace(BB1, ' ').split()
    data['ALL']['size'] = float(output[-2])
    data = {key: {'valid': 0 if key in file else 1, 'size': value['size']} for key, value in data.items()}

    with open(file_json, 'w') as F:
        json.dump(data, F, indent=4)
    # with open(BB1, 'r') as F:
    #     data = json.load(F)
    print("running!")
    
    
if __name__ == "__main__":
    # check_interval = 5
    # scheduler = BlockingScheduler()
    # scheduler.add_job(init_bb, 'interval', seconds=check_interval, args=[])
    # scheduler.start()
    init_bb('/root/HPC/BB/nocompress/','/root/HPC/Cache/file_cache_nocompress.json')
    init_bb('/root/HPC/BB/compress/','/root/HPC/Cache/file_cache_compress.json')
    init_bb('/root/HPC/BB/cbb/','/root/HPC/Cache/file_cache_cbb.json')
