# Architecture

MaxFlexSim models a 2D grid of tiles partitioned into islands. A compiler pipeline
normalizes DSL programs, selects implementations, places nodes, routes edges, and
emits config/certificate artifacts.

```
DSL -> IR -> Normalize -> Impl Select -> Place -> Route -> Emit
```
