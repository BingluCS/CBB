git clone https://github.com/DaveGamble/cJSON.git
cd cJSON
mkdir build
cd build
cmake ..
make -j 8
# make install
gcc -shared -fPIC BurstBuffer.c cJSON/cJSON.c -o libbb.so