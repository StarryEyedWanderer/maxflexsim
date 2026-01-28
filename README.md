# MaxFlexSim

MaxFlexSim is a research-friendly compiler/runtime prototype for flexible accelerator fabrics.

## Quickstart

```bash
pip install -e .
maxflex compile --fabric fabric/examples/fabric_small.json --in examples/adder.mfs --out build/
```

## Examples

```bash
maxflex compile --fabric fabric/examples/fabric_small.json --in examples/mac.mfs --out build/
maxflex compile --fabric fabric/examples/fabric_default.json --in examples/wide_reduce.mfs --out build/
```

## Status

This repository is a work in progress and focuses on correctness, determinism, and clarity.
