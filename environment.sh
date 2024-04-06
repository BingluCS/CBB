echo "# start of WRF" >> ~/.bashrc
echo export DIR=/home/ubutnu/hardDisk/CBB/Libs   >> ~/.bashrc
echo export JASPERLIB=$DIR/grib2/lib             >> ~/.bashrc
echo export JASPERINC=$DIR/grib2/include         >> ~/.bashrc
echo export LDFLAGS=-L$DIR/grib2/lib             >> ~/.bashrc
echo export CPPFLAGS=-I$DIR/grib2/include        >> ~/.bashrc
echo export PATH=$DIR/netcdf/bin:$PATH           >> ~/.bashrc
echo export PATH=$DIR/mpich/bin:$PATH            >> ~/.bashrc
echo export NETCDF=$DIR/netcdf                   >> ~/.bashrc
echo export HDF5=$DIR/hdf5                       >> ~/.bashrc
echo export LD_LIBRARY_PATH=$DIR/netcdf/lib:$LD_LIBRARY_PATH >> ~/.bashrc

wget -c -4 https://github.com/madler/zlib/archive/refs/tags/v1.2.12.tar.gz
tar -xvzf v1.2.12.tar.gz
cd zlib-1.2.12/
./configure --prefix=$DIR/grib2
make -j 8
make install
cd ..

wget https://www2.mmm.ucar.edu/wrf/OnLineTutorial/compile_tutorial/tar_files/libpng-1.2.50.tar.gz
tar xzvf libpng-1.2.50.tar.gz     #or just .tar if no .gz present
cd libpng-1.2.50
./configure --prefix=$DIR/grib2
make
make install
cd ..

wget https://www2.mmm.ucar.edu/wrf/OnLineTutorial/compile_tutorial/tar_files/jasper-1.900.1.tar.gz
tar xzvf jasper-1.900.1.tar.gz  
cd jasper-1.900.1
./configure --prefix=$DIR/grib2
make -j 8
make install
cd ..