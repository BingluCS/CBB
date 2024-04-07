import os
import sys 
import re
import subprocess
import json
import tqdm
prefix = '/home/ubutnu/hardDisk/DeepLearning/wiki/'
def run_test_for_files(directory, script =None):
    # 获取目录下所有文件
    filename_list = []
    filepath_list = []
    dpzip_info = {} 
    for root, directories, files in os.walk(directory):
        for filename in files:
            tmp = os.path.join(root, filename)
            filepath_list.append(tmp)
            #tmp = tmp[len(prefix):]
            filename_list.append(filename)
        #print(directories)
    # 遍历文件
    for i,file in  enumerate(filepath_list):
        # if i==2: 
        #     break
        if os.path.isfile(file):
            # 构建运行命令
            command = f"python3 {script} {file}"
        result = subprocess.run(command,shell=True, capture_output=True, text=True).stdout.strip().replace('\n', ' ')
        match = re.search(r'Total compressed bytes: (\d+)', result)
        size = float(match.group(1))
        dpzip_info[filename_list[i]] = {"size": size}
    # with open('2dpzip_info.json', 'w') as f:
    #     json.dump(dpzip_info, f, indent=4)
    #     command = f"dd if=/dev/zero of={filename_list[i]} bs={size} count=1"
    #     os.system(command)

if __name__ == "__main__":
    # if len(sys.argv) != 3:
    #     print("Usage: python3 run_test_for_files.py directory script")
    #     sys.exit(1)
    
    # directory = sys.argv[1]  # 目录路径
    # script = sys.argv[2]  # 脚本路径
    directory = '/home/ubutnu/hardDisk/DeepLearning/wiki_book2/'
    run_test_for_files(directory,"/home/ubutnu/hardDisk/test/zip_sim.py dpzip" )

