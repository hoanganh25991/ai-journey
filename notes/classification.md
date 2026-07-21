# Classification — dán nhãn cho đầu vào

> Cho một đầu vào (câu chữ, ảnh, vài con số), model chọn một nhãn trong tập nhãn cho trước. Đây là bài toán "build model" phổ biến nhất, đứng ngay sau [softmax](./softmax.md).

## Vì sao quan trọng

Rất nhiều việc thực tế quy về phân loại: câu này tích cực hay tiêu cực, email có phải spam, ảnh là chó hay mèo, câu hỏi dễ hay khó. Hiểu classification là hiểu cách một model "ra quyết định rời rạc" — và nó tái dùng đúng chuỗi tokenize → embedding → softmax mà lab đã đi qua.

## Ý chính

- **Classification head:** phần cuối của model biến biểu diễn (vector) thành một điểm số cho mỗi nhãn (logits), rồi [softmax](./softmax.md) đổi thành xác suất → chọn nhãn cao nhất.
- **Binary vs multi-class vs multi-label:**
  - *Binary*: 2 lớp (spam / không).
  - *Multi-class*: chọn 1 trong nhiều lớp (neg / neu / pos).
  - *Multi-label*: một đầu vào có thể mang nhiều nhãn cùng lúc.
- **Học bằng loss:** *cross-entropy* đo xác suất dự đoán lệch đáp án bao nhiêu; train là đẩy loss xuống ([06-train-infer.md](./06-train-infer.md)).
- **Đánh giá:** accuracy dễ hiểu nhưng gây hiểu lầm khi dữ liệu lệch lớp; nên xem thêm precision / recall / F1.
- **Cân bằng dữ liệu:** lớp hiếm dễ bị model bỏ qua — cần để ý phân bố nhãn.

## Hình minh họa

![Softmax regression: mô hình phân loại nhiều lớp](assets/protonx/softmax-regression.jpg)

![Softmax đổi điểm thô thành xác suất để chọn nhãn](assets/protonx/softmax.jpg)

## Trong pipeline

```
đầu vào → embedding → classification head → softmax → nhãn
                                           (train: cross-entropy)
```

Classification là "đích đến" của [softmax.md](./softmax.md); huấn luyện nó bằng [pytorch-training.md](./pytorch-training.md) hoặc [tensorflow-training.md](./tensorflow-training.md).

## Tham khảo

- [scikit-learn — classification](https://scikit-learn.org/stable/supervised_learning.html)
- Google — [Classification (ML Crash Course)](https://developers.google.com/machine-learning/crash-course/classification/video-lecture)

## Related

- [softmax.md](./softmax.md), [05-demo-text.md](./05-demo-text.md)
- [pytorch-training.md](./pytorch-training.md), [tensorflow-training.md](./tensorflow-training.md)
