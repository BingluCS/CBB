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
    print("Prefetch time:", prefetchTime, "s")

    pattern_flush = r'Demoting time_use is (\d+\.\d+) us'
    matches = re.findall(pattern_flush, data)
    flushTime = 0
    if match:
        for match in matches:
            flushTime += float(match)/1000_000
    print("Flush time:", flushTime, "s")


    pattern_input = r"Timing for processing wrfinput file \(stream \d+\) for domain\s+\d+:\s+(\d+\.\d+) elapsed seconds"
    matches = re.findall(pattern_input, data)
    inTime = float(matches[0])

    pattern_bdy = r"Timing for processing lateral boundary for domain\s+\d+:\s+(\d+\.\d+) elapsed seconds"
    matches = re.findall(pattern_bdy, data)
    bdyTime = float(matches[0])

    print("Read time :", bdyTime + inTime - prefetchTime, " s")

    pattern_restart = r"Timing for Writing restart for domain\s+\d+:\s+(\d+\.\d+) elapsed seconds"
    matches = re.findall(pattern_restart, data)
    resTime = float(matches[0])
    print("Restart time:", resTime, " s")
    
    pattern_out = r"Timing for Writing .* for domain\s+\d+:\s+(\d+\.\d+) elapsed seconds"
    matches = re.findall(pattern_out, data)
    out1 = float(matches[0])
    out2 = float(matches[1])
    sumout = out1+out2
    print("Write time:", sumout, "s")

file = sys.argv[1]
wrfget_data(file)

