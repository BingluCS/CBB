echo "WRF:   -----------------------------------"
python3 dlwrf-$1.py $1-rsl $1-wrf.txt 
echo "NYX:   -----------------------------------"
python3 dltime-$1.py $1-nyx.txt 
echo "WarpX: -----------------------------------"
python3 dltime-$1.py $1-warpx.txt
