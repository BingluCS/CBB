# CBB
This project is a simulation implementation of a computational burst buffer (CBB) based on a computational storage driver (CSD).

While preparing the artifacts, we deploy a 12-node virtual cluster on data center servers with two Intel Xeon Gold 6330 2.0 GHz CPUs and 128GB DDR4 memory to simulate the HPC storage infrastructure. Each compute node is deployed with 8 vCPUs and 8GB DRAM. The CBB node has a PCIe Gen5 x4 CSD directly attached via vfio passthrough.

## Minimum system requirements
OS: Ubuntu (20.04 is recommended)
Memory: >= 16 GB RAM
Processor: >= 8 cores (>=16 is recommended)
Storage: a SSD >= 128 GBs, a HDD >= 128 GBs
gcc/9.5.0


## 1. Install
please make sure your installation directory is in the SSD.
### 1.1 Set environment

```
. environment.sh
```
### 1.2 Install dependent libraries and packages (1 mins)
```
sudo apt install libtool automake autoconf make m4 grads default-jre csh time
. requirements.sh
```
### 1.3 Load or install MPICH (7 mins)

```
. mpi.sh
```
### 1.4 Initial the BB config (1 mins)
```
cd DME
. testBB-nocom.sh 
. cJson.sh
. BB.sh
```
### 1.5 Download and install the HDF5 and netcdf library  (5 mins)

```
cd $CBB_HOME
. hdf5.sh
. netcdf.sh
```
### 1.6 Intsall the SZ compressor (2 mins)
```
. compressor.sh
```
### 1.7 Install the WRF with compress and no-compress mode (14 mins)

```
. wrf.sh
```
### 1.8 Install the Nyx with compress and no-compress mode (4 mins)

```
. nyx.sh
```
### 1.9 Install the WarpX with compress and no-compress mode (4 mins)

```
. warpx.sh
```

## 2. test
### 2.1 Download the no-compress dateset 
If necessary, you need to change the PFS directory to be on the HDD for simulating the real Parallel File System(PFS). 
#### Download the no-compress dateset  
```
cd $CBB_HOME/run/PFS/nocompress
wget https://www2.mmm.ucar.edu/wrf/src/non_compressed_12km.tar.gz
tar xvf non_compressed_12km.tar.gz
cd non_compressed_12km
cp wrfinput_d01 $CBB_HOME/run/PFS/nocompress
cp wrfbdy_d01 $CBB_HOME/run/PFS/nocompress
cp wrfinput_d01 $CBB_HOME/run/BB/cbb
cp wrfbdy_d01 $CBB_HOME/run/BB/cbb
```
#### Download the compress dateset  
```
wget https://www2.mmm.ucar.edu/wrf/src/conus12km.tar.gz # The file is about 1.8GB including the output file
tar xvf conus12km.tar.gz
cd conus12km
cp wrfinput_d01 $CBB_HOME/run/PFS/compress
cp wrfbdy_d01 $CBB_HOME/run/PFS/compress
```

### Download the datasets of wrf and nyx
For the datasets of wrf and nyx, we share them on Onedrive(https://hnueducn-my.sharepoint.com/:f:/g/personal/lbcs_hnu_edu_cn/EulfVRRn01VNoNwQ0QH6yA8BDJibuZymfsXo5DqIIKIg6A)
```
cp /your/install/chk00005 $CBB_HOME/run/PFS/nocompress
cp /your/install/chk001000 $CBB_HOME/run/PFS/nocompress
cp /your/install/chk00005 $CBB_HOME/run/PFS/compress
cp /your/install/chk001000 $CBB_HOME/run/PFS/compress
cp /your/install/chk00005 $CBB_HOME/run/BB/cbb
cp /your/install/chk001000 $CBB_HOME/run/BB/cbb
```

### 2.2 run application with no-compress format
#### Initial the BB with no-compress format
```
cd $CBB_HOME/DME
. testBB-nocom.sh
. BB.sh
```

#### run wrf with no-compress format
```
cd $CBB_HOME/test
. test-nocom.sh wrf
```
#### Run NYX with no-compress format
```
cd $CBB_HOME/test
. test-nocom.sh nyx
```
#### Run Warpx with no-compress format
```
cd $CBB_HOME/test
. test-nocom.sh warpx
```
#### Evaluation
```
cd $CBB_HOME/out
. analyse.sh nocom
```

### 2.3 run application with software compress format
#### Initial the BB with software compress format
```
cd $CBB_HOME/DME
. testBB-com.sh
. BB.sh
```

#### run wrf with software compress format
```
cd $CBB_HOME/test
. test-com.sh wrf
```
#### Run NYX with software compress format
```
cd $CBB_HOME/test
. test-com.sh nyx
```
#### Run Warpx with software compress format
```
cd $CBB_HOME/test
. test-com.sh warpx
```
#### Evaluation
```
cd $CBB_HOME/out
. analyse.sh com
```

### 2.4 run application with CBB
#### Simulate the CBB files
Note: CBB is based on Real Computational Storage Drive(CSD). For this experiment, We offer some simualtion files of real applicaitons based on CSD compression and their metadata file in advance. If necessary, we support the manual creation of these files using the scripts we provide. If you have CSD cand can apply CSD to BB, you don't use scripts to simulate the CSD files. 

Method 1: 
```
cd   $CBB_HOME/run/
tar xvf sim_bb.tar.gz
cd sim_bb && cp * $CBB_HOME/run/PFS/cbb -r
```

Method 2:
```
cd  $CBB_HOME/sim_bb
git clone https://github.com/taovcu/DPZipSim.git
python3 sim_file.py $$CBB_HOME/tmp/
```
#### Initial the BB with CBB
```
cd $CBB_HOME/DME
. testBB-cbb.sh
. BB.sh
```

#### run wrf with CBB
```
cd $CBB_HOME/test
. test-cbb.sh wrf
```
#### Run NYX with CBB
```
cd $CBB_HOME/test
. test-cbb.sh nyx
```
#### Run Warpx with CBB
```
cd $CBB_HOME/test
. test-cbb.sh warpx
```
#### Evaluation
```
cd $CBB_HOME/out
. analyse.sh cbb
```

## 3. the whole Evaluation
All evaluations are divided into 3 parts:

- test1 for overall performance with different BB size under three conditions(no-compress BB, software compression BB and CBB).
- test2 for CPU utilization under three conditions.
- test3 for cache hit rate under three conditions.

If you want more realistic results, set the BB path (on the SSD) and the PFS path (on the HDD) correctly.

tes1: overall performance for CBB (10 compute-hours).

You can edit the script to reduce the number of loops, which will bring the time down to 3~4 compute-hours
```
cd $CBB_HOME/test
. test1.sh nocom 8 
. test1.sh com 8
. test1.sh cbb 8
```


test2: the CPU utilization of CBB (20 compute-minutes)
```
cd $CBB_HOME/test
. test2.sh
```

test3: cache hit rate evalution (10 compute-minutes)
```
cd $CBB_HOME/test
. test3.sh
```

Draw: After done, you can execute python scripts to draw the figure.
```
cd figure
. draw.sh
```