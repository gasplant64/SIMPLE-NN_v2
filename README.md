# SIMPLE-NN_v2
<p align="center">
<img src="./docs/logo.png", width="500"/>
</p>
SIMPLE-NN_v2(SNU Interatomic Machine-learning PotentiaL packagE – version Neural Network)

If you use SIMPLE-NN_v2, please cite this article: 

K. Lee, D. Yoo, W. Jeong, S. Han, SIMPLE-NN: An efficient package for training and executing neural-network interatomic potentials, *Computer Physics Communications* (2019), https://doi.org/10.1016/j.cpc.2019.04.014.

Here do we describe minimal instruction to run the example of SIMPLE-NN
If you want more information such as tuning parameters, please visit our online manual(https://simple-nn.readthedocs.io)

## Requirement
- Python >= 3.6
- LAMMPS >= 29Oct2020
We can handle the output file of various quantum calculation code such as `ABINIT`, `CASTEP`, `CP2K`, `Quantum espresso`, `Gaussian`, and `VASP` as dataset via atomic simulation environment module [ASE](https://wiki.fysik.dtu.dk/ase/index.html).

Please check whether ASE module can read the output of your quantum calculation or not. [link](https://wiki.fysik.dtu.dk/ase/ase/io/io.html)

## Installation
1. Pytorch
Install PyTorch: https://pytorch.org/get-started/locally

Choose the PyTorch of stable release for `Python`. If you have CUDA-capable system, please the PyTorch with CUDA. It boosts the training speed.

To theck if your GPU driver and CUDA is enabled by PyTorch, run the following commands in python interpretor to return whether or not the CUDA driver is enabled: 
```python
import torch.cuda
torch.cuda.is_available()
```

2. SIMPLE-NN
We encourage you to use `virtualenv` or `conda` for convenient module managenement.
```bash
git clone https://github.com/MDIL-SNU/SIMPLE-NN_v2.git
cd SIMPLE-NN_v2
python setup.py install
```
If you run into permission issues, add a `--user` tag after the last command.

3. LAMMPS
Currently, we support the module for symmetry_function - Neural_network model.

Download LAMMPS: https://github.com/lammps/lammps

Only LAMMPS whose version is `29Oct2020` or later is supported.

Copy the source code to LAMMPS src directory.
```
cp /path/to/SIMPLE-NN_v2/simple-nn_v2/features/symmetry_function/pair_nn.* /path/to/lammps/src/
cp /path/to/SIMPLE-NN_v2/simple-nn_v2/features/symmetry_function/symmetry_function.h /path/to/lammps/src/
```
Compile LAMMPS code.
```bash
cd /path/to/lammps/src/
make mpi
```

4. mpi4py (optional)
SIMPLE-NN supports the parallelized calculation in dataset generation and preprocessing.

Install mpi4py:
```bash
pip install mpi4py
```

## Usage
To use SIMPLE-NN_v2, 3 types of files (input.yaml, params_XX, structure_list) are required.

### input.yaml
Parameter list to control SIMPLE-NN code is listed in input.yaml. 
The simple example of input.yaml is described below:
```YAML
# input.yaml
generate_features: true
preprocess: true
train_model: true
params:
    Si: params_Si
    O: params_O

symmetry_function:
    type: symmetry_function
  
neural_network:
    optimizer:
        method: Adam
    nodes: 30-30
```

### params_XX
params_XX (XX means atom type that is included your target system) indicates the coefficients of symmetry functions.
Each line contains coefficients for one symmetry function. detailed format is described below:

```text
2 1 0 6.0 0.003214 0.0 0.0
2 1 0 6.0 0.035711 0.0 0.0
4 1 1 6.0 0.000357 1.0 -1.0
4 1 1 6.0 0.028569 1.0 -1.0
4 1 1 6.0 0.089277 1.0 -1.0
```

First one indicates the type of symmetry function. Currently G2, G4 and G5 is available.

Second and third indicates the type index of neighbor atoms which starts from 1. For radial symmetry function, 1 neighbor atom is need to calculate the symmetry function value. Thus, third parameter is set to zero. For angular symmtery function, 2 neighbor atom is needed. The order of second and third do not affect to the calculation result.

Fourth one means the cutoff radius for cutoff function.

The remaining parameters are the coefficients applied to each symmetry function.

### structure_list
structure_list contains the path of reference data. The format is described below:

```
/path/to/output_file :
/path/to/output_file 100:2000:20
/path/to/{1..10}/output_file :
``` 
The first and second columns stand for the path of reference data and index, repsecitvely.

### Script for running SIMPLE-NN
After preparing input.yaml, params_XX and structure_list, one can run SIMPLE-NN using the script below:

```python
"""
Run the code below:
    python run.py
    or
    mpirun -np numproc run.py # if you install mpi4py

run.py:
"""

from simple_nn_v2 import run
run('input.yaml')
```

## Example
In examples folder, one can find MD trajectories of bulk SiO<sub>2</sub>, corresponding input files (input.yaml, params_Si, params_O and structure_list) and python script run.py. To use this example, one simply change the location in the 'structure_list' file and run 'python run.py' command.

