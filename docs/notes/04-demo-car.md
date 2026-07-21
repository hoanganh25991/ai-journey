# Demo: Car NN — Fully Connected

## Slides & app

| | Link |
|--|------|
| Slides | [slides/car-nn](../slides/car-nn/index.html) |
| App | [demos/car-nn/app](../demos/car-nn/app/index.html) |

## Architecture

```
sensors [L, M, R] in [0,1]  →  hidden FC  →  {forward, back, left, right}
```

Obstacle → sensor < 1.

## Related

- [softmax.md](./softmax.md), [train-gpu.md](./train-gpu.md)
