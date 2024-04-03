rm ~/HPC/BB/nocompress/wrf* -rf
rm ~/HPC/BB/nocompress/chk* -rf
rm ~/HPC/BB/nocompress/plt* -rf
rm ~/HPC/BB/compress/wrf* -rf
rm ~/HPC/BB/compress/chk* -rf
rm ~/HPC/BB/compress/plt* -rf
rm ~/HPC/BB/cbb/wrf* -rf
rm ~/HPC/BB/cbb/chk* -rf
rm ~/HPC/BB/cbb/plt* -rf
rm ~/CSD/BBcsd/*old* -rf
#rm ~/CSD/BBcsd/*wrf* -rf
rm ~/PFS/test/wrf* -rf
#cp -r ~/HPC/BB/bk_cbb_* ~/HPC/BB/cbb/
python3 initbb.py
