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
    print(f"Prefetch time:\t\t\t{prefetchTime:.3f} s")

    pattern_flush = r'Demoting time_use is (\d+\.\d+) us'
    matches = re.findall(pattern_flush, data)
    flushTime = 0
    if matches:
        for match in matches:
            flushTime += float(match)/1000_000
    print(f"Flush time:\t\t\t{flushTime:.3f} s")

    pattern_write = r'real write time = (\d+\.\d+)  seconds'
    matches = re.findall(pattern_write, data)
    writeTime = 0
    if matches:
        for match in matches:
            writeTime += float(match)
    print(f"Write + compression time:\t{writeTime:.3f} s")

    pattern_total= r'real\s+(\d+)m(\d+\.\d+)s'
    matches = re.search(pattern_total, data)
    totalTime = 0
    totalTime += float(matches.group(1))*60+float(matches.group(2))
    print(f"Total time:\t\t\t{totalTime:.3f} s")

file = sys.argv[1]
wrfget_data(file)

