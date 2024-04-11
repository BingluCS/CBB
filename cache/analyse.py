with open('ratio', 'r') as file:
    data = file.read()

blocks = data.split('BB size:')

for block in blocks[1:]:
    lines = block.strip().split('\n')
    size = lines[0].strip()
    print("BB size:", size)
    for i in range(1, len(lines), 2):
        numbers = lines[i].split()
        value = lines[i + 1].strip()
        print(numbers, value)

