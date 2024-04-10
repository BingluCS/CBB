import sys
import re
import os

pattern_prefetch = r'Prefetch time_use is (\d+\.\d+) us'
pattern_flush = r'Demoting time_use is (\d+\.\d+) us'
pattern_write = r'real write time = (\d+\.\d+)  seconds'
pattern_total= r'real\s+(\d+)m(\d+\.\d+)s'
pattern_bdy = r"Timing for processing lateral boundary for domain\s+\d+:\s+(\d+\.\d+) elapsed seconds"
pattern_out = r"Timing for Writing .* for domain\s+\d+:\s+(\d+\.\d+) elapsed seconds"
pattern_input = r"Timing for processing wrfinput file \(stream \d+\) for domain\s+\d+:\s+(\d+\.\d+) elapsed seconds"
def get_wrfdata(filename):
    with open(filename, "r") as file:
        data = file.read()

    matches = re.findall(pattern_prefetch, data)
    prefetchTime = 0
    if matches:
        for match in matches:
            prefetchTime += float(match)/1000_000
            
    matches = re.findall(pattern_flush, data)
    flushTime = 0
    if matches:
        for match in matches:
            flushTime += float(match)/1000_000
    
    matches = re.findall(pattern_input, data)
    inTime = float(matches[0])

    matches = re.findall(pattern_bdy, data)
    bdyTime = float(matches[0])
    readTime = 0
    readTime = bdyTime + inTime - prefetchTime

    matches = re.findall(pattern_out, data)
    out,writeTime = 0,0
    if matches:
        for match in matches:
            out += float(match)
    writeTime = out-flushTime

    return prefetchTime,flushTime,readTime,writeTime

def get_wrftotal(filename):
    with open(filename, "r") as file:
        data = file.read()
    matches = re.search(pattern_total, data)
    totalTime = 0
    if matches:
        totalTime += float(matches.group(1))*60+float(matches.group(2))
    return totalTime

def get_amrdata(filename):
    with open(filename, "r") as file:
        data = file.read()
    matches = re.findall(pattern_prefetch, data)
    prefetchTime = 0
    if matches:
        for match in matches:
            prefetchTime += float(match)/1000_000

    matches = re.findall(pattern_flush, data)
    flushTime = 0
    if matches:
        for match in matches:
            flushTime += float(match)/1000_000
    matches = re.findall(pattern_write, data)
    writeTime = 0
    if matches:
        for match in matches:
            writeTime += float(match)

    matches = re.search(pattern_total, data)
    totalTime = 0
    totalTime += float(matches.group(1))*60+float(matches.group(2))

    return prefetchTime,flushTime,writeTime,totalTime

def pTime(prefetch,flush,write,total):
    print(f"Prefetch time:\t\t\t{prefetch:.3f} s")
    print(f"Flush time:\t\t\t{flush:.3f} s")
    print(f"Write time:\t\t\t{(write):.3f} s")
    print(f"Total time:\t\t\t{total:.3f} s")
    print("")

if __name__ == "__main__":
    data = []
    for type in ['nocom','com','cbb']:
        print(type)
        for i in range(10,50):
            if os.path.exists(f"{type}-wrf-{i}"):
                prefetch, flush, read, write = get_wrfdata(f"{type}-rsl-{i}")
                total = get_wrftotal(f"{type}-wrf-{i}")
                x = [0, i, 'wrf', prefetch, flush, read, write, total]
                print(x)
            if os.path.exists(f"{type}-nyx-{i}"):
                prefetch, flush, write, total = get_amrdata(f"{type}-nyx-{i}")
                x = [0, i, 'nyx', prefetch, flush, 0, write, total]
                print(x)
            if os.path.exists(f"{type}-nyx-{i}"):
                prefetch, flush, write, total = get_amrdata(f"{type}-warpx-{i}")
                x = [0, i, 'warpx', prefetch, flush, 0, write, total]
                print(x)

