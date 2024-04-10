import os
import sys 
import re
import subprocess
import zstd
def run_test_for_files(directory, prefix,script =None):

    filename_list = []
    path_list = []
    subpath_list = []
    dpzip_info = {} 
    for root, directories, files in os.walk(directory):
        for filename in files:
            tmp = os.path.join(root, filename)
            path_list.append(tmp)
            tmp = tmp[len(prefix):]
            subpath_list.append(tmp)
            filename_list.append(filename)

    #print(filename_list,path_list)
    for i,file in  enumerate(path_list):
        if os.path.isfile(file):
            command = f"python3 {script} {file}"
        result = subprocess.run(command,shell=True, capture_output=True, text=True).stdout.strip().replace('\n', ' ')
        match = re.search(r'Total compressed bytes: (\d+)', result)
        size = int(match.group(1))
        # dpzip_info[filename_list[i]] = {"size": size}
        # print(filename_list[i],size)
        command = f"dd if=/dev/zero of={f'{prefix}sim_files/{filename_list[i]}'} bs={size} count=1"
        os.system(command)
    # # with open('2dpzip_info.json', 'w') as f:
    #     json.dump(dpzip_info, f, indent=4)


if __name__ == "__main__":
    directory = sys.argv[1]
    #print(directory[:-4])
    run_test_for_files(directory,directory[:-4],f"{directory[:-4]}sim_bb/DPZipSim/dpzip_sim.py dpzip",)

