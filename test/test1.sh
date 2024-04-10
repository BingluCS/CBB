
if [ "$1" = "nocom" ]; then
    for ((i=10; i<=50; i+=5)); do
    cd $CBB_HOME/DME
    echo -en '\tPFS = "'"$CBB_HOME"'/run/PFS/nocompress/",\n\tBB0 = "'"$CBB_HOME"'/run/BB/nocompress/",\n\tBB1 = "'"$CBB_HOME"'/run/BB/nocompress/",
     \tjson_file = "'"$CBB_HOME"'/DME/file_cache_nocompress.json",\n\tthreshold = 1024.0*1024*1024*'"$i"'' > BBconfig
    sudo bash BB.sh
    . init.sh #init the BB metadata
    cd $CBB_HOME/nocompress_wrf/test/em_real/
    cp nocomname namelist.input
    (time mpirun -np 8 ./wrf.exe) >& $CBB_HOME/out/test1/nocom-wrf-$i
    cp rsl.error.0000 $CBB_HOME/out/test1/nocom-rsl-$i
    cd $CBB_HOME/Nyx/Exec/AMR-density
    (time mpirun -np 8 ./nocomp input_nocom-nyx) >& $CBB_HOME/out/test1/nocom-nyx-$i
    cd $CBB_HOME/warpx_directory/WarpX
    (time mpirun -np 8 ./nocomp input_nocom-warpx) >& $CBB_HOME/out/test1/nocom-warpx-$i
    cd $CBB_HOME
    done
elif [ "$1" = "com" ]; then
    for ((i=10; i<=18; i+=2)); do
    cd $CBB_HOME/DME
    echo -en '\tPFS = "'"$CBB_HOME"'/run/PFS/compress/",\n\tBB0 = "'"$CBB_HOME"'/run/BB/compress/",\n\tBB1 = "'"$CBB_HOME"'/run/BB/compress/",
     \tjson_file = "'"$CBB_HOME"'/DME/file_cache_compress.json",\n\tthreshold = 1024.0*1024*1024*'"$i"'' > BBconfig
    sudo bash BB.sh
    . init.sh #init the BB metadata
    cd $CBB_HOME/compress_wrf/test/em_real/
    cp comname namelist.input
    (time mpirun -np 8 ./wrf.exe) >& $CBB_HOME/out/test1/com-wrf-$i
    cp rsl.error.0000 $CBB_HOME/out/test1/com-rsl-$i
    cd $CBB_HOME/Nyx/Exec/AMR-density
    echo "0.005" > eb.txt
    (time mpirun -np 8 ./comp input_com-nyx) >& $CBB_HOME/out/test1/com-nyx-$i
    cd $CBB_HOME/warpx_directory/WarpX
    echo "0.001" > eb.txt
    (time mpirun -np 8 ./comp input_com-warpx) >& $CBB_HOME/out/test1/com-warpx-$i
    cd $CBB_HOME
    done
elif [ "$1" = "cbb" ]; then
    for ((i=10; i<=18; i+=2)); do
    cd $CBB_HOME/DME
    echo -en '\tPFS = "'"$CBB_HOME"'/run/PFS/nocompress/",\n\tBB0 = "'"$CBB_HOME"'/run/BB/cbb/",\n\tBB1 = "'"$CBB_HOME"'/run/BB/sim_bb/",
    \tjson_file = "'"$CBB_HOME"'/DME/file_cache_cbb.json",\n\tthreshold = 1024.0*1024*1024*'"$i"'' > BBconfig
    sudo bash BB.sh
    . init.sh #init the BB metadata
    . initcbb.sh
    cd $CBB_HOME/nocompress_wrf/test/em_real/
    cp cbbname namelist.input
    (time mpirun -np 8 ./wrf.exe) >& $CBB_HOME/out/cbb-wrf
    cp rsl.error.0000 $CBB_HOME/out/cbb-rsl
    cd $CBB_HOME/Nyx/Exec/AMR-density
    (time mpirun -np 8 ./nocomp input_cbb-nyx) >& $CBB_HOME/out/cbb-nyx
    cd $CBB_HOME/warpx_directory/WarpX
    (time mpirun -np 8 ./nocomp input_cbb-warpx) >& $CBB_HOME/out/cbb-warpx
    cd $CBB_HOME
    done
fi
