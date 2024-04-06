cd $CBB_HOME
cd orisz3
mkdir install
mkdir build
cd build
cmake -DCMAKE_INSTALL_PREFIX:PATH=$CBB_HOME/orisz3/install -DBUILD_H5Z_FILTER=ON ..
export SZ3_HOME=$CBB_HOME/orisz3/install 
make -j 8
make install
cd $CBB_HOME 

echo export SZ3_HOME=$CBB_HOME/orisz3/install >> ~/.bashrc