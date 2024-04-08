# CBB

## 1. Install

### 1.1 Set environment

```
. environment.sh
```

### 1.2 Install dependent libraries and packages
```
. requirements.sh
```

### 1.3 Load or install MPICH

```
. mpi.sh
```

### 1.4 Initial the BB config
```
cd DME
. testBBconfig.sh 
. cJson.sh
. BB.sh
```

### 1.5 Download and install the HDF5 library 

```
cd $CBB_HOME
. hdf5.sh
```

### 1.6 Download and install the netcdf

```
. netcdf.sh
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
### 2.1 Init Burst Buffer
```
cd DME
. testBB-nocom.sh
. init.sh
. BB.sh
```
### 2.2 Run WRF
#### Download the no-compress dateset  
```
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

#### run wrf with software no-compress format
```
cd $CBB_HOME/DME
. testBB-nocom.sh
. init.sh #init the BB metadata
. BB.sh
cd $CBB_HOME/nocompress_wrf/test/em_real/
cp nocomname namelist.input
time mpirun -np 16 ./wrf.exe
cd $CBB_HOME/scripts
python3 dlwrf-no.py $CBB_HOME/nocompress_wrf/test/em_real/rsl.error.0000
```

#### run wrf with software compress format
```
cd $CBB_HOME/DME
. testBB-com.sh
. init.sh #init the BB metadata
. BB.sh
cd $CBB_HOME/compress_wrf/test/em_real/
cp comname namelist.input
time mpirun -np 16 ./wrf.exe
python3 dlwrf-com.py $CBB_HOME/compress_wrf/test/em_real/rsl.error.0000
```

#### Simulate the CBB files
note: CBB is based on Real Computational Storage Drive(CSD). If you can apply CSD to BB, you don't use scripts to simulate the CSD files. 
please move all files fo wrf (both input and output) to the directory ($CBB_HOME/tmp/) 
```
cd  $CBB_HOME
mkdir sim_files
cd  $CBB_HOME/sim_bb
git clone https://github.com/taovcu/DPZipSim.git
mv DPZipSim/dpzip_sim.py . 
python3 sim_file.py $CBB_HOME/tmp/
python3 dlwrf-no.py $CBB_HOME/nocompress_wrf/test/em_real/rsl.error.0000
```
Although the metadata json file is created in advance, you can still create metadata json files as needed

#### run wrf with cbb
```
cd $CBB_HOME/DME
. testBB-cbb.sh
. init.sh #init the BB metadata
. initcbb.sh
. BB.sh

cd $CBB_HOME/nocompress_wrf/test/em_real/
cp cbbname namelist.input
time mpirun -np 16 ./wrf.exe
cd $CBB_HOME/scripts
python3 dlwrf-no.py $CBB_HOME/nocompress_wrf/test/em_real/rsl.error.0000
```

### 2.3 Run NYX 
```
cd $CBB_HOME/DME
. testBB-nocom.sh
. init.sh #init the BB metadata
. BB.sh
cd $CBB_HOME/Nyx/Exec/AMR-density
(time mpirun -np 16 ./nocomp input_nocom-nyx) >& nocomp-nyx.txt
cd $CBB_HOME/scripts
python3 dlwrf-no.py $CBB_HOME/nocompress_wrf/test/em_real/rsl.error.0000

```
