import subprocess
import json
import sys
import re
import os

HPCsystem ={
    "PFS": "",
    "BB0": "",
    "BB1": "",
    "json_file": "",
    "threshold": 0
}
def check():
    parameters ={
    "PFS": 0,
    "BB0": 0,
    "BB1": 0,
    "json_file": 0,
    "threshold": 0
    }
    pattern0 = r'(\w+)\s*=\s*(.+),*'
    pattern1 = r'"([^"]+)"'
    pattern2 = r'(.+)'
    config =""
    with open('BBconfig', 'r') as file:
        for line in file:
            string = line.strip() 
            matches = re.search(pattern0, string)
            if matches:
                key = matches.group(1)
                if key in parameters:
                    if parameters[key] == 0:
                        parameters[key] = 1
                    else :
                        print(f"({key}) Duplicate parameter setting!")
                        sys.exit()
                        
                    if(key=='threshold'):
                        value = re.search(pattern2, matches.group(2))
                        if(eval(value.group(1)) <= 0):
                            print("The threshold should be greater than 0!")
                            sys.exit()
                        HPCsystem[key] = eval(value.group(1))
                        config += f'\t.{key} = {value.group(1)},\n'
                    else : 
                        value = re.search(pattern1, matches.group(2))
                        if(not (os.path.exists(value.group(1)) or os.path.isdir(value.group(1)))):
                            print(f"({key}) File or directory does not exist!")
                            sys.exit()
                        config += f'\t.{key} = "{value.group(1)}",\n'
                        HPCsystem[key] = value.group(1)
                else :
                    print("Config parameter error!")
                    sys.exit()
            else :
                print("Config file format error!")
                print("-------------------------")
                print("PFS = -------------------")
                print("BB0 = -------------------")
                print("BB1 = -------------------")
                print("json_file = -------------")
                print("threshold = -------------")
                sys.exit()

def init_bb(BB1,file_json):
    command = "ls -d " + BB1 + '* | grep -v \'^' + BB1+ 'bk_\' ' + '| grep -v \'old\' '
    result = subprocess.run(command,shell=True, capture_output=True, text=True)
    file = result.stdout.strip().replace('\n', ' ')
    # print(command)
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
    # init_bb('/root/HPC/BB/nocompress/','/root/HPC/Cache/file_cache_nocompress.json')
    # init_bb('/root/HPC/BB/compress/','/root/HPC/Cache/file_cache_compress.json')
    # init_bb('/root/HPC/BB/cbb/','/root/HPC/Cache/file_cache_cbb.json')
    check()
    #print(HPCsystem['json_file'])
    init_bb(HPCsystem['BB1'],HPCsystem['json_file'])