# Demo: Car NN — từ cảm biến ra hành động

> Một chiếc xe đồ chơi có 3 cảm biến khoảng cách. Một mạng nơ-ron nhỏ (fully connected) nhìn 3 con số đó và quyết định: đi tới, lùi, rẽ trái hay rẽ phải. Đây là ví dụ *nhìn thấy được* của phân loại.

## Vì sao đáng xem

Các note khái niệm (embedding, softmax) khá trừu tượng. Demo này rút gọn tất cả về mức "thấy tận mắt": đầu vào là 3 số, đầu ra là 1 trong 4 hành động, và bạn quan sát mạng đổi quyết định ngay khi vật cản dịch chuyển. Nó cho cảm giác cụ thể về *một lớp fully connected + softmax* làm việc gì.

## Ý chính

- **Đầu vào:** ba cảm biến trái / giữa / phải, mỗi cái là số trong `[0,1]`. Không vật cản → gần 1; có vật cản → nhỏ dần.
- **Mạng:** một (hoặc vài) lớp fully connected biến 3 số đầu vào thành 4 điểm — mỗi điểm cho một hành động.
- **Ra quyết định:** [softmax.md](./softmax.md) đổi 4 điểm thành xác suất, chọn hành động cao nhất → `{forward, back, left, right}`.
- **Trực giác "học":** trọng số của lớp fully connected chính là thứ được điều chỉnh khi train, để bộ 3 cảm biến ánh xạ sang hành động hợp lý.

## Kiến trúc

```
sensors [L, M, R] ∈ [0,1]  →  hidden (fully connected)  →  softmax  →  {forward, back, left, right}
```

## Slides & app

| | Link |
|--|------|
| Slides | [slides/car-nn](../slides/car-nn/index.html) |
| App | [demos/car-nn/app](../demos/car-nn/app/index.html) |

## Related

- [softmax.md](./softmax.md) — bước chọn hành động
- [06-train-infer.md](./06-train-infer.md), [train-gpu.md](./train-gpu.md) — huấn luyện trọng số
