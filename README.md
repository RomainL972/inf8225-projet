# INF8225 - GNN-based Register Allocation via Graph Coloring

This project uses a Graph Neural Network (GNN) to solve the register allocation problem by framing it as graph coloring on interference graphs extracted from LLVM.

## Structure

- **llvm-project/** — Fork of LLVM 22.1.4 with a custom `DumpInterferenceGraph` pass that exports register interference graphs in DIMACS format.
- **RUN-CSP/** — RUN-CSP: a GNN architecture for solving Constraint Satisfaction Problems, used here for graph coloring.

## Setup

```bash
# Clone with submodules
git clone --recurse-submodules <repo-url>

# Or initialize submodules after cloning
git submodule update --init --recursive
```

## Building LLVM

```bash
cd llvm-project
cmake -S llvm -B build -G Ninja \
  -DCMAKE_BUILD_TYPE=Release \
  -DLLVM_ENABLE_PROJECTS="clang" \
  -DLLVM_TARGETS_TO_BUILD="X86"
ninja -C build
```

## Extracting Interference Graphs

Compile any C/C++ file with the `-enable-dump-ig` flag to dump interference graphs:

```bash
./llvm-project/build/bin/clang -O2 -mllvm -enable-dump-ig -c input.c -o /dev/null
```

This creates DIMACS files in `./interference_graphs/`, one per (function, register class) pair. Each file includes a comment with `NumPhysRegs` (the number of colors k needed).

Example output:
```
c Function: fib, RegClass: GR32, NumPhysRegs: 32
p edge 4 4
e 1 2
e 1 3
e 2 4
e 3 4
```

## Training the GNN

```bash
cd RUN-CSP
pip install -r requirements.txt
python train_coloring.py -d ../interference_graphs/ --n_colors <k> -e 20 -t 25
```

Where `<k>` is the number of physical registers for the target register class (found in the DIMACS comment line).
