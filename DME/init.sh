rm $CBB_HOME/run/BB/nocompress/wrf* -rf
rm $CBB_HOME/run/BB/nocompress/chk* -rf
rm $CBB_HOME/run/BB/nocompress/plt* -rf
rm $CBB_HOME/run/BB/compress/wrf* -rf
rm $CBB_HOME/run/BB/compress/chk* -rf
rm $CBB_HOME/run/BB/compress/plt* -rf
rm $CBB_HOME/run/BB/sim_bb/wrf* -rf
rm $CBB_HOME/run/BB/sim_bb/chk* -rf
rm $CBB_HOME/run/BB/sim_bb/plt* -rf
# rm $CBB_HOME/run/BB/cbb/*old* -rf
#rm ~/CSD/BBcsd/*wrf* -rf
# rm ~/PFS/test/wrf* -rf
#cp -r $CBB_HOME/run/BB/bk_cbb_* $CBB_HOME/run/BB/cbb/
python3 initbb.py 
