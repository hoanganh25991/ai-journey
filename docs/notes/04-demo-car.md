# Demo: Car NN — from sensors to action

> A toy car with three distance sensors. A small fully connected network reads those three numbers and picks an action: forward, backward, turn left, or turn right. A visible example of classification.

## Why it matters

Concept notes (embedding, softmax) stay abstract. This demo boils them down: input is three numbers, output is one of four actions, and you watch the decision change as obstacles move. You get a concrete feel for *fully connected layer + softmax*.

## Key ideas

- **Input:** left / center / right sensors, each a number in `[0,1]`. Clear path → near 1; obstacle nearby → drops toward 0.
- **Network:** one or more fully connected layers map three inputs to four scores — one per action.
- **Decision:** [softmax.md](./softmax.md) turns four scores into probabilities; pick the highest → `{forward, back, left, right}`.
- **Learning intuition:** training adjusts the fully connected weights so sensor patterns map to the right action.

Architecture:

```
sensors [L, M, R] ∈ [0,1]  →  hidden (fully connected)  →  softmax  →  {forward, back, left, right}
```

## Pipeline

```
sensor readings → neural net → softmax → driving action
```

## Slides & demo

| | Link |
|--|------|
| Slides | [slides/car-nn](../slides/car-nn/index.html) |
| App | [demos/car-nn/app](../demos/car-nn/app/index.html) |

## Related

- [softmax.md](./softmax.md) — action selection step
- [06-train-infer.md](./06-train-infer.md), [train-gpu.md](./train-gpu.md) — training the weights
