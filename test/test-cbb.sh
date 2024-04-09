if [ "$1" = "wrf" ]; then
    cd $CBB_HOME/DME
    . init.sh #init the BB metadata
    . initcbb.sh
    cd $CBB_HOME/nocompress_wrf/test/em_real/
    cp cbbname namelist.input
    (time mpirun -np 8 ./wrf.exe) >& $CBB_HOME/out/cbb-wrf
    cp rsl.error.0000 $CBB_HOME/out/cbb-rsl
    cd $CBB_HOME/DME
    python3 flush.py >& $CBB_HOME/out/cbb-wrff # 
elif [ "$1" = "nyx" ]; then
    cd $CBB_HOME/DME
    . init.sh #init the BB metadata
    . initcbb.sh
    cd $CBB_HOME/Nyx/Exec/AMR-density
    (time mpirun -np 8 ./nocomp input_cbb-nyx) >& $CBB_HOME/out/cbb-nyx
    cd $CBB_HOME/DME
    python3 flush.py >& $CBB_HOME/out/cbb-nyxf
elif [ "$1" = "warpx" ]; then
    cd $CBB_HOME/DME
    . init.sh #init the BB metadata
    cd $CBB_HOME/warpx_directory/WarpX
    (time mpirun -np 8 ./nocomp input_cbb-warpx) >& $CBB_HOME/out/cbb-warpx
    cd $CBB_HOME/DME
    python3 flush.py >& $CBB_HOME/out/cbb-warpxf
fi