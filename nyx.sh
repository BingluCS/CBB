cd $CBB_HOME

#cd Nyx/subprojects
#. build-sun.sh

cd $CBB_HOME/Nyx/Exec/AMR-density

make clean
cp $CBB_HOME/amrex/Src/Extern/HDF5/AMReX_PlotFileUtilHDF5.ori $CBB_HOME/amrex/Src/Extern/HDF5/AMReX_PlotFileUtilHDF5.cpp
make -j 8 USE_HDF5_SZ3=FALSE 
mv Nyx3d* nocomp

make clean
cp $CBB_HOME/amrex/Src/Extern/HDF5/AMReX_PlotFileUtilHDF5.ori $CBB_HOME/amrex/Src/Extern/HDF5/AMReX_PlotFileUtilHDF5.cpp
make -j 8 USE_HDF5_SZ3=TRUE SZ3_HOME=$SZ3_HOME
mv Nyx3d* comp

cd $CBB_HOME
