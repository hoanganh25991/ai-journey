# Train with PyTorch

> A hands-on lesson: use PyTorch to train a classifier — epoch loop, compute loss, backprop, update weights until the model is good enough.

## Why it matters

PyTorch is the most popular flexible framework for building and training models yourself. Understanding its training loop means understanding how learning actually happens — the same mechanism every high-level library ([Hugging Face](./huggingface.md), sentence-transformers) wraps underneath.

## Key ideas

- **Epoch vs batch:** an *epoch* is one pass over all data; a *batch* is a small chunk processed per step. Many epochs let the model learn gradually.
- **Four steps per batch:** forward → loss → `backward()` (gradients) → `step()` (weight update). Call `zero_grad()` so gradients do not accumulate.
- **Optimizer and learning rate:** Adam/SGD decides how far to move each step; learning rate too high → unstable jumps, too low → slow learning.
- **Train/val split:** track validation loss to catch *overfitting* (memorizes training data, fails on new data).
- **GPU:** `.to("cuda")` for model and batch → much faster training; see [train-gpu.md](./train-gpu.md).
- **When done, save:** `torch.save(model.state_dict())` → checkpoint for [inference](./06-train-infer.md).

Training loop (skeleton):

```python
model = MyClassifier()
opt = torch.optim.Adam(model.parameters(), lr=1e-3)
loss_fn = nn.CrossEntropyLoss()

for epoch in range(EPOCHS):
    for x, y in dataloader:          # each batch
        opt.zero_grad()              # clear old gradients
        logits = model(x)            # forward
        loss = loss_fn(logits, y)    # compare to labels
        loss.backward()              # backprop: compute gradients
        opt.step()                   # update weights
```

## Pipeline

```
dataset → DataLoader → [epoch loop: forward → loss → backward → step] → checkpoint
```

This is how to implement training for [classification.md](./classification.md); the TensorFlow version is at [tensorflow-training.md](./tensorflow-training.md).

## References

- [PyTorch — Training a classifier](https://pytorch.org/tutorials/beginner/blitz/cifar10_tutorial.html)
- [torch.optim](https://pytorch.org/docs/stable/optim.html)

## Related

- [classification.md](./classification.md), [tensorflow-training.md](./tensorflow-training.md)
- [train-gpu.md](./train-gpu.md), [huggingface.md](./huggingface.md)
