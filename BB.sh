git clone https://github.com/DaveGamble/cJSON.git
cd cJSON
mkdir build
cd build
cmake ..
make -j 8
gcc -shared -fPIC BurstBuffer.c cJSON/cJSON.c -o libbb.so
(head -n 15 CacheFunction.c && cat BBconfig && tail -n +21 CacheFunction.c) > tmp \
&& mv CacheFunction.c oldcachefunction.c && mv tmp CacheFunction.c
sudo cp libbb.so /usr/lib/libbb.so