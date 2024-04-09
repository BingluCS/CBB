if [ "$1" = "wrf" ]; then
    cd $CBB_HOME/DME
    . init.sh #init the BB metadata
    cd $CBB_HOME/nocompress_wrf/test/em_real/
    cp nocomname namelist.input
    (time mpirun -np 8 ./wrf.exe) >& $CBB_HOME/out/nocom-wrf
    cp rsl.error.0000 $CBB_HOME/out/nocom-rsl
    cd $CBB_HOME/DME
    python3 flush.py >& $CBB_HOME/out/nocom-wrff # 
elif [ "$1" = "nyx" ]; then
    cd $CBB_HOME/DME
    . init.sh #init the BB metadata
    cd $CBB_HOME/Nyx/Exec/AMR-density
    (time mpirun -np 8 ./nocomp input_nocom-nyx) >& $CBB_HOME/out/nocom-nyx
    cd $CBB_HOME/DME
    python3 flush.py >& $CBB_HOME/out/nocom-nyxf
elif [ "$1" = "warpx" ]; then
    cd $CBB_HOME/DME
    . init.sh #init the BB metadata
    cd $CBB_HOME/warpx_directory/WarpX
    (time mpirun -np 8 ./nocomp input_nocom-warpx) >& $CBB_HOME/out/nocom-warpx
    cd $CBB_HOME/DME
    python3 flush.py >& $CBB_HOME/out/nocom-warpxf
fi