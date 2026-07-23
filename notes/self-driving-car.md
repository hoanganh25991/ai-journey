# Self-Driving Car — Sensors, Brains, Maps

> A toy classification demo stops at “3 numbers → 4 labels.” A self-driving car keeps going: ray sensors read the world, a small neural net decides controls every frame, dozens of mutated clones race, and the best brain is saved — then the same loop runs on a hand-built or OSM-derived map.

## Why it matters

[Classification](./classification.md) teaches discrete decisions. Closed-loop driving teaches the rest of the AI stack you actually feel:

- **Perception → action in a loop** (not a one-shot label).
- **Search over policies** (mutate N brains, keep the survivor) instead of only gradient descent.
- **World model first** — borders, traffic, corridors — then learning.

That is why this topic sits in the Demo stage: you watch fitness emerge on a road, not only read softmax math.

## Key ideas

- **Geometry before layers:** a line / plane / hyperplane is a decision boundary. Early “brain” layers are just stacked weighted sums + thresholds — the same idea as separating classes, now separating “turn left” from “go forward” given sensor offsets.
- **Feed-forward network (levels):** sensors → hidden → controls. In the lab demo each level does `sum(w·x) > bias → 1 else 0` (hard threshold). Later you can swap that for continuous activations or a TensorFlow “brain library”; the control wiring stays the same.
- **Ray sensors:** cast several rays from the car; each hit against road borders or traffic yields an offset in `[0,1]`. Clear path → low threat; near obstacle → high. Those offsets (plus speed) are the network inputs — richer than three hand-tuned sliders.
- **Virtual world:** a graph of points/segments becomes roads, borders, markings (start, target, lights…). The car does not need pixels; it needs **borders** (and optional corridor to a target). Map editor → `.world` file → drive.
- **Evolutionary training:** spawn **N** AI cars with the same (or saved) brain; mutate copies slightly; keep the one that travels farthest / stays undamaged longest (`bestBrain` in `localStorage`). Save → reload → mutate again. No labeled dataset required for the first “it drives” win.
- **Real maps:** overlay OpenStreetMap rules → extract roads → drop into the virtual world (e.g. an office campus). Same sensors + brain, harder geometry and longer corridors.

Architecture (lab demo):

```
ray sensors (+ speed)  →  NN levels  →  {forward, left, right, reverse}
                ↑ mutate N clones, keep bestBrain
road borders + traffic
```

## Pipeline

```
math boundaries → NN levels → ray sensors on a road
        → mutate N cars / save best brain
        → (optional) virtual-world editor / OSM map → evaluate again
```

Train vs infer still applies ([06-train-infer.md](./06-train-infer.md)): evolution *is* training; the browser loop with a frozen `bestBrain` is inference.

## Slides & demo

| | Link |
|--|------|
| Slides | [slides/self-driving-car](../slides/self-driving-car/index.html) |
| App | [demos/self-driving-car/app](../demos/self-driving-car/app/index.html) |

The hub demo is the **training road** slice (lanes + traffic + mutate/save). Full map editor / OSM / office `.world` lives in the longer sample project (see References).

## References

- [gniziemazity/self-driving-car](https://github.com/gniziemazity/self-driving-car) — Radu Mariescu-Istodor course code (no libraries)
- Local deeper sample: `adc-pts/pts-sample-self-driving-car` (virtual world, ttek-office map, training + editor)

## Related

- [softmax.md](./softmax.md), [classification.md](./classification.md) — discrete decisions and heads
- [curve-fitting.md](./curve-fitting.md), [neural-networks.md](./neural-networks.md) — knobs → layers → brain
- [06-train-infer.md](./06-train-infer.md), [train-gpu.md](./train-gpu.md) — train once, run light
- [tensorflow-training.md](./tensorflow-training.md) — when you graduate the “brain” out of pure JS
