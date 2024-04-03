
#include <CacheFuction.h>


int Prefect_cache(const char *filename) {
    struct timeval start;
    struct timeval end;
    gettimeofday(&start,NULL);
    char source_path[100];
    char destination_path[100];

    sprintf(source_path,"/root/HPC/PFS/nocompress/%s",filename);
    sprintf(destination_path,"./%s",filename);

    char command[220];
    sprintf(command, "cp -rf %s %s", source_path, destination_path);
    
    // 调用system函数执行cp命令
    int status = system(command);
    
    if (status == 0) {
        printf("File copied successfully.\n");
    } else {
        printf("Error copying file.\n");
    }
    gettimeofday(&end,NULL);
    float time_use=(end.tv_sec-start.tv_sec)*1000000+(end.tv_usec-start.tv_usec);//微秒
    printf("time_use is %.10f us\n",time_use);
    return 0;
}
int Prefect_compress_cache(const char *filename) {
    struct timeval start;
    struct timeval end;
    gettimeofday(&start,NULL);
    char source_path[100];
    char destination_path[100];

    sprintf(source_path,"/root/HPC/PFS/compress/%s",filename);
    sprintf(destination_path,"./%s",filename);

    char command[220];
    sprintf(command, "cp -r %s %s", source_path, destination_path);
    
    // 调用system函数执行cp命令
    int status = system(command);
    
    if (status == 0) {
        printf("File copied successfully.\n");
    } else {
        printf("Error copying file.\n");
    }
    gettimeofday(&end,NULL);
    float time_use=(end.tv_sec-start.tv_sec)*1000000+(end.tv_usec-start.tv_usec);//微秒
    printf("time_use is %.10f us\n",time_use);
    return 0;

}
int Read_file_cache(const char *filename) {
    char *json_file = "/root/HPC/PFS/nocompress/file_cache.json";
    FILE *F = fopen(json_file, "r");
    if (F == NULL) {
        printf("Error opening file!\n");
        return 0;
    }
    fseek(F, 0, SEEK_END);
    int length = ftell(F);
    fseek(F, 0, SEEK_SET);
    char *buffer = (char*)malloc(length + 1);

    fread(buffer, 1, length, F);
    fclose(F);
    // const char *json_string = "{\"name\": \"John\", \"age\": 30, \"city\": \"New York\"}";


    cJSON *root = NULL;
    root = cJSON_Parse(buffer);
    free(buffer);

    cJSON *state = cJSON_GetObjectItemCaseSensitive(root,filename);

    if(state->valueint == 1){
        Prefect_cache(filename);
        cJSON_SetNumberValue(state, 0);
        F = fopen(json_file, "w");
        if (F == NULL) {
            printf("Error opening file!\n");
            return 1;
        }

        char *json_string = cJSON_Print(root);
        fputs(json_string, F);
        fclose(F);

        printf("Prefect success\n");
    }
    return 0;
}
// int main() {
//     Read_file("wrfinput_d01");
//     // cJSON *root = cJSON_CreateObject();
//     // cJSON_AddNumberToObject(root, "wrfinput_d01", 1);
//     // cJSON_AddNumberToObject(root, "wrfbdy_d01", 1);
//     // cJSON_AddNumberToObject(root, "wrfout_d01_2019-11-26_18:00:00", 0);

//     // // 序列化 JSON 对象成 JSON 字符串
//     // char *json_string = cJSON_Print(root);

//     // // 写入 JSON 字符串到文件
//     // FILE *file = fopen("file_cache.json", "w");
//     // if (file == NULL) {
//     //     printf("Error opening file!\n");
//     //     return 1;
//     // }

//     // fputs(json_string, file);
//     // fclose(file);

//     // // 释放 cJSON 对象和 JSON 字符串
//     // cJSON_Delete(root);
//     // free(json_string);

//     return 0;
// }
