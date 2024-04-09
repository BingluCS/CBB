if [ "$1" = "cbb" ]; then
    echo "WRF:   -----------------------------------"
    python3 dlwrf-nocom.py cbb-wrf cbb-rsl f
    echo "NYX:   -----------------------------------"
    python3 dltime-nocom.py cbb-nyx f
    echo "WarpX: -----------------------------------"
    python3 dltime-nocom.py cbb-warpx f
else
    echo "WRF:   -----------------------------------"
    python3 dlwrf-$1.py $1-wrf $1-rsl f
    echo "NYX:   -----------------------------------"
    python3 dltime-$1.py $1-nyx f
    echo "WarpX: -----------------------------------"
    python3 dltime-$1.py $1-warpx f
fi