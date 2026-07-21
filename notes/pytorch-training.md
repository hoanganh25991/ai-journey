# Train với PyTorch

> Một bài "chạy thật": dùng PyTorch để train một classifier — vòng lặp epoch, tính loss, backprop, cập nhật trọng số cho tới khi model đủ tốt.

## Vì sao quan trọng

PyTorch là framework linh hoạt và phổ biến nhất để tự tay dựng và train model. Hiểu vòng lặp training trong PyTorch là hiểu *cơ chế học* thật sự diễn ra thế nào — thứ mà mọi thư viện cấp cao ([Hugging Face](./huggingface.md), sentence-transformers) đều gói lại bên dưới.

## Vòng lặp training (khung xương)

```python
model = MyClassifier()
opt = torch.optim.Adam(model.parameters(), lr=1e-3)
loss_fn = nn.CrossEntropyLoss()

for epoch in range(EPOCHS):
    for x, y in dataloader:          # từng batch
        opt.zero_grad()              # xóa gradient cũ
        logits = model(x)            # forward
        loss = loss_fn(logits, y)    # so với đáp án
        loss.backward()              # backprop: tính gradient
        opt.step()                   # cập nhật trọng số
```

## Ý chính

- **Epoch vs batch:** *epoch* = một lần đi hết dữ liệu; *batch* = một nhóm nhỏ xử lý mỗi bước. Nhiều epoch để model học dần.
- **4 bước lặp lại:** forward → loss → `backward()` (gradient) → `step()` (cập nhật). Nhớ `zero_grad()` để gradient không cộng dồn.
- **Optimizer & learning rate:** Adam/SGD quyết định *đi bao xa* mỗi bước; lr quá lớn → nhảy loạn, quá nhỏ → học chậm.
- **Train/val split:** theo dõi loss trên tập validation để phát hiện *overfitting* (thuộc lòng train, kém trên dữ liệu mới).
- **GPU:** `.to("cuda")` cho model và batch → train nhanh hơn nhiều; xem [train-gpu.md](./train-gpu.md).
- **Xong thì lưu:** `torch.save(model.state_dict())` → checkpoint để [inference](./06-train-infer.md).

## Trong pipeline

```
dataset → DataLoader → [vòng lặp epoch: forward → loss → backward → step] → checkpoint
```

Đây là cách hiện thực việc train cho [classification.md](./classification.md); phiên bản TensorFlow ở [tensorflow-training.md](./tensorflow-training.md).

## Tham khảo

- [PyTorch — Training a classifier](https://pytorch.org/tutorials/beginner/blitz/cifar10_tutorial.html)
- [torch.optim](https://pytorch.org/docs/stable/optim.html)

## Related

- [classification.md](./classification.md), [tensorflow-training.md](./tensorflow-training.md)
- [train-gpu.md](./train-gpu.md), [huggingface.md](./huggingface.md)
