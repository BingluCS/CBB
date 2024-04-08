import sys
import re
  
def wrfget_data(filename):
    with open(filename, "r") as file:
        data = file.read()
    pattern_prefetch = r'Prefetch time_use is (\d+\.\d+) us'
    matches = re.findall(pattern_prefetch, data)
    prefetchTime = 0
    if matches:
        for match in matches:
            prefetchTime += float(match)/1000_000
    print(f"Prefetch time:\t{prefetchTime:.3f} s")

    pattern_flush = r'Demoting time_use is (\d+\.\d+) us'
    matches = re.findall(pattern_flush, data)
    flushTime = 0
    if matches:
        for match in matches:
            flushTime += float(match)/1000_000
    print(f"Flush time:\t{flushTime:.3f} s")

    pattern_write = r'real write time = (\d+\.\d+)  seconds'
    matches = re.findall(pattern_write, data)
    writeTime = 0
    if matches:
        for match in matches:
            print(match)
            writeTime += float(match)
    print(f"Write time:\t{writeTime:.3f} s")

    # pattern_write = r'real write time = (\d+\.\d+)  seconds'
    # matches = re.findall(pattern_write, data)
    # writeTime = 0
    # if matches:
    #     for match in matches:
    #         print(match)
    #         writeTime += float(match)
    # print(f"Write time:\t{writeTime:.3f} s")

file = sys.argv[1]
wrfget_data(file)

