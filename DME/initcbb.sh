

source_dir=$CBB_HOME/run/PFS/cbb/
dest_dir=$CBB_HOME/run/BB/sim_bb/

# mkdir -p "$dest_dir"

for file in "$source_dir"/*; do
    filename=$(basename "$file")
    if [ ! -e "$dest_dir/$filename" ] && [ ! -e "$dest_dir/bk_$filename" ]; then
        cp "$file" "$dest_dir/bk_$filename"
        # echo "Copied $filename to $dest_dir"
    # else
    #     echo "Skipped $filename"
    fi
done
cd $CBB_HOME/DME

# directory="$CBB_HOME/run/BB/sim_bb/"  
# prefix="bk_"
# cd "$directory" 

# for filename in *; do
#     if [[ ! "$filename" =~ ^bk_ ]]; then
#         new_filename="$prefix$filename"
#         mv "$filename" "$new_filename"
#         # echo "Renamed $filename to $new_filename"
#     fi
# done
# cd $CBB_HOME/DME