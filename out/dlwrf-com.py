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

    pattern_input = r"Timing for processing wrfinput file \(stream \d+\) for domain\s+\d+:\s+(\d+\.\d+) elapsed seconds"
    matches = re.findall(pattern_input, data)
    inTime = float(matches[0])

    pattern_bdy = r"Timing for processing lateral boundary for domain\s+\d+:\s+(\d+\.\d+) elapsed seconds"
    matches = re.findall(pattern_bdy, data)
    bdyTime = float(matches[0])
    readTime = 0
    readTime = bdyTime + inTime - prefetchTime

    pattern_out = r"Timing for Writing .* for domain\s+\d+:\s+(\d+\.\d+) elapsed seconds"
    matches = re.findall(pattern_out, data)
    out,writeTime = 0,0
    if matches:
        for match in matches:
            out += float(match)
    writeTime = out-flushTime
    return prefetchTime,flushTime,readTime,writeTime

def get_total(filename):
    with open(filename, "r") as file:
        data = file.read()
    pattern_total= r'real\s+(\d+)m(\d+\.\d+)s'
    matches = re.search(pattern_total, data)
    totalTime = 0
    if matches:
        totalTime += float(matches.group(1))*60+float(matches.group(2))
    return totalTime

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
    print(f"Read time :\t\t\t{read:.3f} s")
    print(f"Write + compression time:\t{(write):.3f} s")
    print(f"Total + decompression time:\t{total:.3f} s")
    print("")

file0, file1 = sys.argv[1], sys.argv[2]
prefetch, flush, read, write = get_data(file1)
total = get_total(file0)

print("BB is insufficient:")
pTime(prefetch, flush, read, write, total)

if len(sys.argv) > 3:
    f = insufficient(file0 + "f")
    print("BB is insufficient:")
    pTime(prefetch, flush + f, read, write, total + f)
