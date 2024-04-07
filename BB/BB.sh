python3 check.py
gcc -shared -fPIC BurstBuffer.c cJSON/cJSON.c -o libbb.so
cp libbb.so /usr/lib/libbb.so