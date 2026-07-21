# Train with TensorFlow / Keras

> Same classifier lesson, but with TensorFlow (Keras API): define the model, `compile`, then `fit` over many epochs. More concise than PyTorch thanks to the built-in training loop. Everyday metaphor: you write the recipe (`compile`); the kitchen runs it (`fit`).

## Why it matters

TensorFlow (via Keras) is **declarative** training: you describe the model and settings, the framework runs the epoch loop. Contrasting with [PyTorch](./pytorch-training.md) (where you write the loop yourself) shows the same learning idea in two API styles — pick the one that fits the project.

Keras is especially handy for quick softmax-regression experiments and for the Embedding Projector, which makes vector space visible in 3D while you train ([embedding.md](./embedding.md)).

## Key ideas

- **`compile` = declare how to learn:** pick optimizer, loss (softmax + cross-entropy for multi-class), and metrics to track (`accuracy`, etc.).
- **`fit` = run training:** the framework handles epoch/batch iteration and backprop — no manual `backward()`/`step()` like PyTorch.
- **Monitor with metrics:** `accuracy` and `val_loss` print each epoch; rising `val_loss` while train loss falls → overfitting.
- **Callbacks:** `EarlyStopping` stops when val stops improving; `ModelCheckpoint` saves the best weights automatically.
- **TensorBoard and Projector:** plot loss curves and project embeddings into 3D to inspect clusters and outliers.
- **Same math as PyTorch:** under the hood it is still forward → loss → gradients → weight update. Only the API shape differs.

## Skeleton

```python
model = keras.Sequential([
    keras.layers.Dense(64, activation="relu"),
    keras.layers.Dense(NUM_CLASSES, activation="softmax"),
])
model.compile(
    optimizer="adam",
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy"],
)
model.fit(
    x_train, y_train,
    epochs=EPOCHS,
    validation_data=(x_val, y_val),
    callbacks=[
        keras.callbacks.EarlyStopping(patience=3, restore_best_weights=True),
        keras.callbacks.ModelCheckpoint("best.keras", save_best_only=True),
    ],
)
```

## Worked example (intuition)

You stack a small dense net ending in `softmax` with `NUM_CLASSES` units. After `compile`, each `fit` epoch shuffles batches, computes cross-entropy against integer labels, and updates weights. When `val_loss` bottoms out, EarlyStopping restores that checkpoint — ready for inference.

## Common pitfalls

- **`categorical` vs `sparse_categorical`** — one-hot labels need `categorical_crossentropy`; integer labels need `sparse_*`. Mixing them silently fails or errors.
- **Forgot validation_data** — you only see train accuracy and miss overfitting.
- **No EarlyStopping** — you keep the last epoch, which may be worse than an earlier one.
- **Projector without labels** — hard to interpret; color points by class when possible.

## Illustrations

![Softmax regression — multi-class classification in TensorFlow](assets/protonx/softmax-regression.jpg)

![TensorFlow Embedding Projector: vectors projected into 3D](assets/protonx/tf-projector.jpg)

![Keras compile → fit flow](../slides/assets/tensorflow-keras.png)

## Pipeline

```
dataset → model (Keras) → compile → fit (epochs) → checkpoint
```

Same target as [pytorch-training.md](./pytorch-training.md), serving [classification.md](./classification.md).

## Slides & demo

| | Link |
|--|------|
| Slides | [slides/tensorflow-training](../slides/tensorflow-training/index.html) |

## References

- [TensorFlow — Basic classification](https://www.tensorflow.org/tutorials/keras/classification)
- [Keras API](https://keras.io/api/)

## Related

- [classification.md](./classification.md), [pytorch-training.md](./pytorch-training.md)
- [train-gpu.md](./train-gpu.md), [embedding.md](./embedding.md)
