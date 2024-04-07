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
. testBBconfig.sh
. init.sh
```
### 2.2 Run WRF
##### Download the no-compress dateset  
```
wget https://www2.mmm.ucar.edu/wrf/src/non_compressed_12km.tar.gz
tar xvf non_compressed_12km.tar.gz
cd non_compressed_12km
cp wrfinput_d01 $CBB_HOME/run/PFS/nocompress
cp wrfbdy_d01 $CBB_HOME/run/PFS/nocompress
cp wrfinput_d01 $CBB_HOME/run/PFS/cbb
cp wrfbdy_d01 $CBB_HOME/run/PFS/cbb
```
##### Download the compress dateset  
```
wget https://www2.mmm.ucar.edu/wrf/src/conus12km.tar.gz # The file is about 1.8GB including the output file
tar xvf conus12km.tar.gz
cp wrfinput_d01 $CBB_HOME/run/PFS/compress
cp wrfbdy_d01 $CBB_HOME/run/PFS/compress
```
##### run wrf with software no-compress format

##### run wrf with software compress format

##### run wrf with cbb
note: the cbb is based on Real Computational Storage Drive(CSD). If you can't use the CSD as BB, you only use metadata simulation. So, next is r 