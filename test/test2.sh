 cd $CBB_HOME/DME
. testBB-nocom.sh
sudo bash BB.sh
. init.sh #init the BB metadata
cd $CBB_HOME/Nyx/Exec/AMR-density
mpirun -np $1 $2 $3 ./nocomp input_nocom-nyx & python3 $CBB_HOME/figure/monitor.py $CBB_HOME/figure/cpu_nyx-no.txt

. init.sh #init the BB metadata
cd $CBB_HOME/warpx_directory/WarpX
time mpirun -np  $1 $2 $3 ./nocomp input_nocom-warpx  & python3 $CBB_HOME/figure/monitor.py $CBB_HOME/figure/cpu_warpx-no.txt

 cd $CBB_HOME/DME
. testBB-com.sh
sudo bash BB.sh
. init.sh #init the BB metadata
cd $CBB_HOME/Nyx/Exec/AMR-density
mpirun -np $1 $2 $3 ./comp input_com-nyx & python3 $CBB_HOME/figure/monitor.py $CBB_HOME/figure/cpu_nyx-com.txt

. init.sh #init the BB metadata
cd $CBB_HOME/warpx_directory/WarpX
mpirun -np  $1 $2 $3 ./comp input_com-warpx  & python3 $CBB_HOME/figure/monitor.py $CBB_HOME/figure/cpu_warpx-com.txt