export MPI_DIR=$DIR/mpich
export MPI_VERSION=4.0.2
export PATH=$MPI_DIR/bin:$PATH
export LD_LIBRARY_PATH=$MPI_DIR/\
lib:$LD_LIBRARY_PATH
export MANPATH=$MPI_DIR/share/man:$MANPATH
export C_INCLUDE_PATH=$MPI_DIR/include\
:$C_INCLUDE_PATH
export CPLUS_INCLUDE_PATH=$MPI_DIR/\
include:$CPLUS_INCLUDE_PATH
