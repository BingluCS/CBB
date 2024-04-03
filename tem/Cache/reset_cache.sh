(head -n 15 CacheFunction.c && cat BBconfig && tail -n +21 CacheFunction.c) > tmp && mv CacheFunction.c oldcachefunction.c && mv tmp CacheFunction.c
gcc -shared -fPIC CacheFunction.c cJSON.c -o libbb.so
cp libbb.so /usr/lib/libbb.so
bash /root/copy_libbb.sh
