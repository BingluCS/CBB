#!/bin/bash

# 定义虚拟机信息
ip_prefix="192.168.122"
suffixes=("92" "24" "250" "105" "62" "146" "130" "55" "145" "187" "112" "176")
#suffixes=("105" "62" "146" "130" "55" "145" "187" "112" "176")
username="root"
password="1234"
mountpath="python3 /root/HPC/Cache/monitor/monitor.py 10"
#mountpath="mount -t nfs ubuntuhpc0:/root/CSD CSD/"
# 循环遍历虚拟机信息
# sshpass -p 1234  scp -o StrictHostKeyChecking=no HPC/patch/libbb.so root@192.168.122.92:/root/
for i in "${!suffixes[@]}"; do
    ip_address="${ip_prefix}.${suffixes[$i]}"

    # 使用 scp 复制文件到远程主机
    sshpass -p 1234 ssh -o StrictHostKeyChecking=no $username@$ip_address $mountpath
done
