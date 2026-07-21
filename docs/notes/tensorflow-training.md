# Train with TensorFlow / Keras

> Same classifier lesson, but with TensorFlow (Keras API): define the model, `compile`, then `fit` over many epochs. More concise than PyTorch thanks to the built-in training loop.

## Why it matters

TensorFlow (via Keras) is declarative training: you describe the model and settings, the framework runs the epoch loop. Contrasting with [PyTorch](./pytorch-training.md) (where you write the loop yourself) shows the same learning idea in two API styles — pick the one that fits the project.

## Key ideas

- **`compile` = declare how to learn:** pick optimizer, loss (softmax + cross-entropy for classification), and metrics to track.
- **`fit` = run training:** the framework handles epoch/batch iteration and backprop — no manual `backward()`/`step()` like PyTorch.
- **Monitor with metrics:** `accuracy` and `val_loss` print each epoch; rising `val_loss` while train loss falls → overfitting.
- **Callbacks:** `EarlyStopping`, `ModelCheckpoint` stop at the right time and save the best model.
- **TensorBoard and Projector:** plot loss curves and project embeddings into 3D to inspect ([embedding.md](./embedding.md)).

Skeleton:

```python
model = keras.Sequential([
    keras.layers.Dense(64, activation="relu"),
    keras.layers.Dense(NUM_CLASSES, activation="softmax"),
])
model.compile(optimizer="adam",
              loss="sparse_categorical_crossentropy",
              metrics=["accuracy"])
model.fit(x_train, y_train, epochs=EPOCHS, validation_data=(x_val, y_val))
```

## Illustrations

![Softmax regression — multi-class classification in TensorFlow](assets/protonx/softmax-regression.jpg)

![TensorFlow Embedding Projector: vectors projected into 3D](assets/protonx/tf-projector.jpg)

## Pipeline

```
dataset → model (Keras) → compile → fit (epochs) → checkpoint
```

Same target as [pytorch-training.md](./pytorch-training.md), serving [classification.md](./classification.md).

## References

- [TensorFlow — Basic classification](https://www.tensorflow.org/tutorials/keras/classification)
- [Keras API](https://keras.io/api/)

## Related

- [classification.md](./classification.md), [pytorch-training.md](./pytorch-training.md)
- [train-gpu.md](./train-gpu.md), [embedding.md](./embedding.md)
