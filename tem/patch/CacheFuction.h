#include <stdio.h>
#include <stdlib.h>
#include <cjson/cJSON.h>
#include <sys/time.h>


int Prefect_cache(const char *filename);

int Prefect_compress_cache(const char *filename);

int Read_file_cache(const char *filename);