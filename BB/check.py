import re

parameters ={
    "PFS": 0,
    "BB0": 0,
    "BB1": 0,
    "json_file": 0,
    "threshold": 0
}
pattern0 = r'(\w+)\s*=\s*(.+),*'
pattern1 = r'("[^"]+")'
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
                    print("Duplicate parameter setting!")
                if(key=='threshold'):
                    value = re.search(pattern2, matches.group(2))
                    if(eval(value.group(1)) <= 0):
                        print("The threshold should be greater than 0!")
                else : 
                    value = re.search(pattern1, matches.group(2))
                    

                if(value):

                    config += f'.{key} = {value.group(1)}\n'
            else :
                print("Config parameter error!")
            # if(value):
            #     match

        else :
            print("enter right format")
print(parameters,config)
# data1 = '''.PFS ="/root/PFS/nocompress/",
# .BB0 = "/root/HPC/BB/nocompress/",
# .BB1 = "/root/HPC/BB/nocompress/",
# .json_file = "/root/HPC/Cache/file_cache_nocompress.json",
# .threshold = 1024*1024*1024*50.0'''

# # 定义正则表达式模式
# pattern = r'(\w+)\s*=\s*"([^"]+)"'

# # 使用正则表达式找到匹配项
# matches = re.findall(pattern, data)

# # 将结果存储为字典
# result = {key: value for key, value in matches}

# # 打印结果
# print(data[0])

