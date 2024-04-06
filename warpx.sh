cd warpx_directory
git clone https://github.com/ECP-WarpX/picsar.git
git clone https://github.com/ECP-WarpX/warpx-data.git

cd WarpX
make clean
cp $CBB_HOME/amrex/Src/Extern/HDF5/AMReX_PlotFileUtilHDF5.ori $CBB_HOME/amrex/Src/Extern/HDF5/AMReX_PlotFileUtilHDF5.cpp
make -j 8 USE_HDF5_SZ3=FALSE 
mv main3d* nocomp

make clean
cp $CBB_HOME/amrex/Src/Extern/HDF5/AMReX_PlotFileUtilHDF5.ori $CBB_HOME/amrex/Src/Extern/HDF5/AMReX_PlotFileUtilHDF5.cpp
make -j 8 USE_HDF5_SZ3=TRUE SZ3_HOME=$SZ3_HOME
mv main3d* comp

mv temp-chk001000 diags/chk001000 
mkdir meta
cd $CBB_HOME