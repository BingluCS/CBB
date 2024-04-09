import subprocess
import json
import sys
import re
import os
import ctypes

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

def demotion_all(BB1,file_json):
    example_lib = ctypes.CDLL('./libbb.so')
    while(1):
        command = f"ls -cr -I 'bk_*' {BB1}"
        result = subprocess.run(command,shell=True, capture_output=True, text=True)
        file = result.stdout.strip().replace('\n', ' ')
        if file != '':
            example_lib.demotion()
        else:
            break
    
    
if __name__ == "__main__":
    check()
    demotion_all(HPCsystem['BB1'],HPCsystem['json_file'])
