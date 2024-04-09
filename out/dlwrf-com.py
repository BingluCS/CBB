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
    print(f"Prefetch time:\t\t\t{prefetchTime:.3f} s")

    pattern_flush = r'Demoting time_use is (\d+\.\d+) us'
    matches = re.findall(pattern_flush, data)
    flushTime = 0
    if matches:
        for match in matches:
            flushTime += float(match)/1000_000
    print(f"Flush time:\t\t\t{flushTime:.3f} s")


    pattern_input = r"Timing for processing wrfinput file \(stream \d+\) for domain\s+\d+:\s+(\d+\.\d+) elapsed seconds"
    matches = re.findall(pattern_input, data)
    inTime = float(matches[0])

    pattern_bdy = r"Timing for processing lateral boundary for domain\s+\d+:\s+(\d+\.\d+) elapsed seconds"
    matches = re.findall(pattern_bdy, data)
    bdyTime = float(matches[0])

    print(f"Read + decompression time :\t{(bdyTime + inTime - prefetchTime):.3f} s")

    
    pattern_out = r"Timing for Writing .* for domain\s+\d+:\s+(\d+\.\d+) elapsed seconds"
    matches = re.findall(pattern_out, data)
    out = 0.0
    if matches:
        for match in matches:
            out += float(match)
    sumout = out #+resTime
    print(f"Write + compression time:\t{(sumout-flushTime):.3f} s")

def get_total(filename):
    with open(filename, "r") as file:
        data = file.read()
    pattern_total= r'real\s+(\d+)m(\d+\.\d+)s'
    matches = re.search(pattern_total, data)
    totalTime = 0
    if matches:
        totalTime += float(matches.group(1))*60+float(matches.group(2))
    print(f"Total time:\t\t\t{totalTime:.3f} s")


file0, file1= sys.argv[1],sys.argv[2]
get_data(file0)
get_total(file1)
