# Neural Networks — Layers, Width, Depth

> A neural net is stacked curve-fitting: each layer transforms numbers; depth and width are hyperparameters you choose; weights are knobs you can even edit by hand to feel the decision boundary. Everyday metaphor: a relay of specialists — each stage reshapes the signal before the next.

## Why it matters

[curve-fitting.md](./curve-fitting.md) explains one function with knobs. Networks compose many such functions so they can carve complex regions (drive left vs forward, multilabel outputs, etc.). This note is the bridge into [self-driving-car.md](./self-driving-car.md) and into framework training.

## Key ideas

- **Layers = input → hidden → output.** Hidden layers add capacity; the last layer often becomes class scores or control bits.
- **Depth vs width:** deeper = more successive transforms; wider = more parallel units per layer. Efficiency is a trade — too deep/wide wastes compute, too small underfits.
- **Hyperparameters:** depth, width, learning rate, mutation amount — chosen by you, not learned as weights. Auto-tune = try many instances and keep winners.
- **Manual weight edit:** dragging a weight and watching the car / boundary move builds intuition before blind `optimizer.step()`.
- **Composing nets:** a “brain” can be swapped (JS levels today, TensorFlow library tomorrow) if the I/O contract (sensors → controls) stays stable.

## Illustrations

![Tune a neural network live while a car drives](assets/neural-networks/tune-nn.jpg)

![Auto-tune by generating many network instances](assets/neural-networks/auto-tune.jpg)

## Pipeline

```
sensors / features → layer₁ → … → layerₖ → outputs / actions
                 ↑ choose depth·width · tune or mutate weights
```

## Slides & demo

| | Link |
|--|------|
| Slides | [slides/neural-networks](../slides/neural-networks/index.html) |
| App | [demos/neural-networks/app](../demos/neural-networks/app/index.html) |

## References

- Radu Mariescu-Istodor — Understanding AI / Self-driving car series (layers, multilabel, pathfinding)

## Related

- [curve-fitting.md](./curve-fitting.md), [softmax.md](./softmax.md), [classification.md](./classification.md)
- [self-driving-car.md](./self-driving-car.md) — closed-loop use of a small net
- [pytorch-training.md](./pytorch-training.md)
