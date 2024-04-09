import sys
import re
  
def get_data(filename):
    with open(filename, "r") as file:
        data = file.read()
    pattern_prefetch = r'Prefetch time_use is (\d+\.\d+) us'
    matches = re.findall(pattern_prefetch, data)
    prefetchTime = 0
    if matches:
        for match in matches:
            prefetchTime += float(match)/1000_000

    pattern_flush = r'Demoting time_use is (\d+\.\d+) us'
    matches = re.findall(pattern_flush, data)
    flushTime = 0
    if matches:
        for match in matches:
            flushTime += float(match)/1000_000

    pattern_write = r'real write time = (\d+\.\d+)  seconds'
    matches = re.findall(pattern_write, data)
    writeTime = 0
    if matches:
        for match in matches:
            writeTime += float(match)

    pattern_total= r'real\s+(\d+)m(\d+\.\d+)s'
    matches = re.search(pattern_total, data)
    totalTime = 0
    totalTime += float(matches.group(1))*60+float(matches.group(2))
    return prefetchTime,flushTime,writeTime,totalTime

def insufficient(filename):
    with open(filename, "r") as file:
        data = file.read()
    pattern_flush = r'Demoting time_use is (\d+\.\d+) us'
    matches = re.findall(pattern_flush, data)
    flushTime = 0
    if matches:
        for match in matches:
            flushTime += float(match)/1000_000
    return flushTime

def pTime(prefetch,flush,read,write,total):
    print(f"Prefetch time:\t\t\t{prefetch:.3f} s")
    print(f"Flush time:\t\t\t{flush:.3f} s")
    print(f"Write + compression time:\t{(write):.3f} s")
    print(f"Total + decompression time:\t{total:.3f} s")
    print("")

file = sys.argv[1]
get_data(file)
prefetch, flush, write, total = get_data(file)

print("BB is insufficient:")
pTime(prefetch, flush, write, total)

if len(sys.argv) > 3:
    f = insufficient(file + "f")
    print("BB is insufficient:")
    pTime(prefetch, flush + f, write, total + f)