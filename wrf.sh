cd $CBB_HOME
cd compress_wrf
export NETCDF_classic=0
echo -e "34\n1" | ./configure
sed -i '121s/$/ -lbb/' configure.wrf
./compile em_real -j 8

cd $CBB_HOME
cd nocompress_wrf
export NETCDF_classic=1
echo -e "34\n1" | ./configure
sed -i '121s/$/ -lbb/' configure.wrf
./compile em_real -j 8
cd $CBB_HOME