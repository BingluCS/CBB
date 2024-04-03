#include <stdio.h>
#include <mpi.h>

int main(int argc, char** argv){
	//MPI_Init(&argc, &argv);
	int rank = 0, size;
//	MPI_Comm_rank(MPI_COMM_WORLD, &rank);
	char *seconds = argv[1];
	char command[100];
	sprintf(command,"python3 monitor.py %s %d",seconds,rank);
	system(command);
return 0;
}
