# Curve Fitting — Guess, Measure Loss, Tune

> Learning is curve fitting: you invent a guess function with knobs (parameters), measure how far it is from reality (loss), then turn the knobs so the guess gets closer. Everyday metaphor: adjusting the thermostat until the room matches the setpoint.

## Why it matters

Before PyTorch loops and GPU notebooks, this is the whole game in miniature. Every training step you will write later is the same three moves: **forward** (predict), **loss** (compare), **backward** (nudge knobs using derivatives / gradients). If curve fitting clicks, [pytorch-training.md](./pytorch-training.md) feels like syntax around an idea you already own.

## Key ideas

- **Reality vs guess:** data points are the truth you care about; your model is a family of curves (lines, polynomials, networks) controlled by knobs.
- **Loss:** a single number for “how wrong.” Squared error for regression is common: average `(y − ŷ)²`. High loss → bad fit.
- **Tune the knobs:** change parameters a little, see if loss drops. Hand-tuning works for 1–2 knobs; beyond that you need calculus.
- **Derivative / gradient:** the slope of loss w.r.t. each knob. Negative gradient direction = “turn this way to reduce loss.” In many dimensions the gradient is a vector.
- **Forward then backward:** forward computes ŷ and loss; backward uses the chain rule so each building-block derivative combines into updates for every knob. Loop until loss plateaus.

## Pipeline

```
data → guess(θ) → ŷ → loss(y, ŷ) → ∇θ loss → update θ → repeat
```

## Slides & demo

| | Link |
|--|------|
| Slides | [slides/curve-fitting](../slides/curve-fitting/index.html) |
| App | [demos/curve-fitting/app](../demos/curve-fitting/app/index.html) |

## Related

- [neural-networks.md](./neural-networks.md) — many knobs stacked as layers
- [pytorch-training.md](./pytorch-training.md), [tensorflow-training.md](./tensorflow-training.md) — the same loop in frameworks
- [06-train-infer.md](./06-train-infer.md) — after fitting, freeze knobs and only run forward
