#include<stdio.h>
int main() {
    char command[1024];
    sprintf(command, "ls ../out");

    // Execute command and capture output
    FILE *fp = popen(command, "r");
    if (fp == NULL) {
        perror("Failed to run command");
        return NULL;
    }
    return 0;
}