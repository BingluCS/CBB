#for ((i=5; i<=30; i+=5)); do
#	echo "BB size: $i"
#	python3 readModel.py ori_info.json $i $1 100000
#	python3 readModel.py zip1_info.json $i $1 100000
#	python3 readModel.py zip_info.json $i $1 100000
#	python3 readModel.py dpzip_info.json $i $1 100000
#
#done

for ((i=5; i<=300; i+=5)); do
	echo "BB size: $i"
	python3 readModel.py 2_info.json $i $1 10000 $2
	python3 readModel.py 2zip1_info.json $i $1 10000 $2
	python3 readModel.py 2zip_info.json $i $1 10000 $2
	python3 readModel.py 2dpzip_info.json $i $1 10000 $2
done
