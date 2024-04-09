echo "WRF:   -----------------------------------"
python3 dlwrf-$1.py $1-wrf $1-rsl f
echo "NYX:   -----------------------------------"
python3 dltime-$1.py $1-nyx
echo "WarpX: -----------------------------------"
python3 dltime-$1.py $1-warpx
