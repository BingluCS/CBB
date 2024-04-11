for ((i=5; i<=300; i+=5)); do
	echo "BB size: $i GB"
	python3 readModel.py ori_info.json $1 $i  $2
	python3 readModel.py gzip1_info.json $1 $i $2
	python3 readModel.py gzip3_info.json $1 $i  $2
	python3 readModel.py cbbzip_info.json $1 $i $2
done
