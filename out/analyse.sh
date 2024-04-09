echo "WRF:   -----------------------------------"
python3 dlwrf-com.py comp-rsl comp-wrf.txt 
echo "NYX:   -----------------------------------"
python3 dltime-com.py comp-nyx.txt 
echo "WarpX: -----------------------------------"
python3 dltime-com.py comp-warpx.txt