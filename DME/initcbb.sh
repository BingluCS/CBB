cp $CBB_HOME/tmp/* $CBB_HOME/run/BB/sim_bb/ -r
directory="$CBB_HOME/run/BB/sim_bb/"  # 替换为你的目录路径
prefix="bk_"
# 进入目录
cd "$directory" 

# 遍历目录下的所有文件
for filename in *; do
    # 构建新的文件名，添加前缀
    if [[ ! "$filename" =~ ^bk_ ]]; then
        new_filename="$prefix$filename"
        # 重命名文件，加上前缀
        mv "$filename" "$new_filename"
        # echo "Renamed $filename to $new_filename"
    fi
done
cd $CBB_HOME/DME