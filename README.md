# CBB
This projetc is the simulation of the computational Burst Buffer(CBB) based on computational storage drive (CSD).
While preparing the artifacts, we deploy a 12-node virtual cluster on data center servers with two Intel Xeon Gold 6330 2.0 GHz CPUs and 128GB DDR4 memory to simulate the HPC storage infrastructure. Each compute node is deployed with 8 vCPUs and 8GB DRAM. The CBB node has a PCIe Gen5 x4 CSD directly attached via vfio passthrough. 

## Minimum system requirements
OS: Ubuntu (20.04 is recommended)


Memory: >= 16 GB RAM

Processor: >= 8 cores (>=16 is recommended)

Storage: a SSD >= 64 GBs, a HDD >= 64GBs

gcc/9.5.0

## 1. Install

please make sure your installation directory is in the SSD.
### 1.1 Set environment

```
. environment.sh
```

### 1.2 Install dependent libraries and packages
```
sudo apt install libtool automake autoconf make m4 grads default-jre csh time
. requirements.sh
```

### 1.3 Load or install MPICH

```
. mpi.sh
```

### 1.4 Initial the BB config
```
cd DME
. testBB-nocom.sh 
. cJson.sh
. BB.sh
```

### 1.5 Download and install the HDF5 and netcdf library 

```
cd $CBB_HOME
. hdf5.sh
. netcdf.sh
```

### 1.6 Intsall the SZ compressor
```
. compressor.sh
```

### 1.7 Install the WRF with compress and no-compress mode

```
. wrf.sh
```

### 1.8 Install the Nyx with compress and no-compress mode

```
. nyx.sh
```

### 1.9 Install the WarpX with compress and no-compress mode

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
note: CBB is based on Real Computational Storage Drive(CSD). If you can apply CSD to BB, you don't use scripts to simulate the CSD files. 
```
# please move all files of wrf (both input and output) to the directory ($CBB_HOME/tmp/) 
cd  $CBB_HOME
mkdir sim_files
cd  $CBB_HOME/sim_bb
git clone https://github.com/taovcu/DPZipSim.git
mv DPZipSim/dpzip_sim.py . 
python3 sim_file.py $CBB_HOME/tmp/
python3 dlwrf-no.py $CBB_HOME/nocompress_wrf/test/em_real/rsl.error.0000
```
Although the metadata json file is created in advance, you can still create metadata json files as needed.

#### Initial the BB with CBB
```
cd $CBB_HOME/DME
. testBB-cbb.sh
. BB.sh
```

#### run wrf with CBB
```
cd $CBB_HOME/DME
. init.sh
. initcbb.sh
cd $CBB_HOME/compress_wrf/test/em_real/
cp comname namelist.input
time mpirun -np 16 ./wrf.exe
python3 dlwrf-com.py $CBB_HOME/compress_wrf/test/em_real/rsl.error.0000
```

#### Run NYX with CBB
```
cd $CBB_HOME/DME
. init.sh 
cd $CBB_HOME/Nyx/Exec/AMR-density
. base.sh
(time mpirun -np 16 ./comp input_com-nyx) >& com-nyx.txt
cd $CBB_HOME/scripts
python3 dlwrf-no.py $CBB_HOME/nocompress_wrf/test/em_real/rsl.error.0000
```
#### Run Warpx with CBB
```
cd $CBB_HOME/DME
. init.sh #init the BB metadata
cd $CBB_HOME/warpx_directory/WarpX
. base.sh
(time mpirun -np 16 ./comp input_com-warpx) >& com-warpx.txt
cd $CBB_HOME/scripts
python3 dlwrf-no.py $CBB_HOME/nocompress_wrf/test/em_real/rsl.error.0000
```

