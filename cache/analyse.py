# 从文件中读取数据
with open('ratio', 'r') as file:
    data = file.read()

# 将数据拆分成块
blocks = data.split('BB size:')

# 处理每个块
for block in blocks[1:]:
    lines = block.strip().split('\n')
    size = lines[0].strip()
    print("BB size:", size)
    for i in range(1, len(lines), 2):
        numbers = lines[i].split()
        value = lines[i + 1].strip()
        print(numbers, value)

