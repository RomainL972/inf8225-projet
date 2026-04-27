# pushd .venv/lib/python3.13/site-packages/tensorflow
# ln -svf ../nvidia/*/lib/*.so* .
# popd
# ln -sf ../lib/python3.13/site-packages/nvidia/cuda_nvcc/bin/ptxas $VIRTUAL_ENV/bin/ptxas

# source me
export LD_LIBRARY_PATH=$PWD/.venv/lib/python3.13/site-packages/tensorflow
