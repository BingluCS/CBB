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
    if match:
        for match in matches:
            flushTime += float(match)/1000_000
    print(f"Flush time:\t{flushTime:.3f} s")


    pattern_input = r"Timing for processing wrfinput file \(stream \d+\) for domain\s+\d+:\s+(\d+\.\d+) elapsed seconds"
    matches = re.findall(pattern_input, data)
    inTime = float(matches[0])

    pattern_bdy = r"Timing for processing lateral boundary for domain\s+\d+:\s+(\d+\.\d+) elapsed seconds"
    matches = re.findall(pattern_bdy, data)
    bdyTime = float(matches[0])

    print(f"Read time :\t{(bdyTime + inTime - prefetchTime):.3f} s")

    # pattern_restart = r"Timing for Writing restart for domain\s+\d+:\s+(\d+\.\d+) elapsed seconds"
    # matches = re.findall(pattern_restart, data)
    # resTime = float(matches[0])
    #print(f"Restart time:\t{resTime:.3f} s")
    
    pattern_out = r"Timing for Writing .* for domain\s+\d+:\s+(\d+\.\d+) elapsed seconds"
    matches = re.findall(pattern_out, data)
    out = 0.0
    if match:
        for match in matches:
            out += float(match)
    sumout = out #+resTime
    print(f"Write + compression time:\t{(sumout-flushTime):.3f} s")

file = sys.argv[1]
wrfget_data(file)

