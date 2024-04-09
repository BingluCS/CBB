if [ "$1" = "wrf" ]; then
    cd $CBB_HOME/DME
    . init.sh
    cd $CBB_HOME/compress_wrf/test/em_real/
    cp comname namelist.input
    (time mpirun -np 8 ./wrf.exe) >& $CBB_HOME/out/com-wrf
    cp rsl.error.0000 $CBB_HOME/out/com-rsl
    cd $CBB_HOME/DME
    python3 flush.py >& $CBB_HOME/out/com-wrff
elif [ "$1" = "nyx" ]; then
    cd $CBB_HOME/DME
    . init.sh 
    cd $CBB_HOME/Nyx/Exec/AMR-density
    . base.sh
    (time mpirun -np 8 ./comp input_com-nyx) >& $CBB_HOME/out/com-nyx
    cd $CBB_HOME/DME
    python3 flush.py >& $CBB_HOME/out/com-nyxf
elif [ "$1" = "warpx" ]; then
    cd $CBB_HOME/DME
    . init.sh #init the BB metadata
    cd $CBB_HOME/warpx_directory/WarpX
    . base.sh
    (time mpirun -np 8 ./comp input_com-warpx) >& $CBB_HOME/out/com-warpx
    cd $CBB_HOME/DME
    python3 flush.py >& $CBB_HOME/out/com-warpxf
fi