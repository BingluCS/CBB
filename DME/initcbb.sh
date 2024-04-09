cp $CBB_HOME/run/PFS/cbb/* $CBB_HOME/run/BB/sim_bb/ -r

directory="$CBB_HOME/run/BB/sim_bb/"  
prefix="bk_"
cd "$directory" 

for filename in *; do
    if [[ ! "$filename" =~ ^bk_ ]]; then
        new_filename="$prefix$filename"
        mv "$filename" "$new_filename"
        # echo "Renamed $filename to $new_filename"
    fi
done
cd $CBB_HOME/DME