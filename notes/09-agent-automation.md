# Agent automation — OpenClaw · Hermess

> Câu chuyện cá nhân về làn sóng "AI agent tự chạy việc": từ chatbot trả lời → agent **cầm tay làm** (chạy lệnh, đụng file, điều khiển máy). Hai con mình dùng qua: **OpenClaw** và **Hermess**.

## Bối cảnh

Trước đây AI chỉ *trả lời*: hỏi — đáp, còn làm là việc của mình. Bước ngoặt là khi agent bắt đầu **tích hợp vào máy và control mọi thứ**: tự mở terminal, sửa file, gọi tool, chạy cả một chuỗi task mà không cần mình bấm từng bước.

## OpenClaw — con đầu tiên cho *cảm giác đó*

- Dùng **`pi`** làm harness: đơn giản, nhanh, gọn, nhẹ — cắm vào là chạy task ngay.
- Điểm khiến nó đáng nhớ: **nó là thằng đầu tiên cho người ta cảm giác "AI agent integrate sâu, control giúp mọi thứ".**
  - Không chỉ gợi ý — nó *thực sự làm*: đọc/ghi file, chạy shell, tự nối các bước.
  - Lần đầu thấy một agent "cầm lái" thay vì chỉ ngồi cạnh nhắc bài.
- Triết lý: harness mỏng, ít ma sát → thử nghiệm automation cực nhanh.

> Đây là phần cần **nổi bật**: OpenClaw = khoảnh khắc "à, agent có thể tự điều khiển cả cái máy này".

## Hermess — đến sau, làm tốt

- Sau OpenClaw, **Hermess** hoàn thiện trải nghiệm: mượt, chắc tay hơn khi chạy automation thật.
- Xem slide riêng: [demos/hermess/slides](../demos/hermess/slides/index.html).

## Rút ra

| | OpenClaw | Hermess |
|--|----------|---------|
| Harness | `pi` — mỏng, nhanh gọn nhẹ | hoàn thiện hơn |
| Vai trò | **mở màn** cảm giác agent control mọi thứ | **làm tốt**, dùng thật ổn |
| Khi nào | cảm nhận nhanh, prototype automation | chạy automation chỉn chu |

- Harness nhẹ (`pi` / OpenClaw) = đường ngắn nhất để *cảm* được sức mạnh agent automation.
- Con làm tốt (Hermess) = khi cần chạy thật, ổn định.

## Related

- [07-agents.md](./07-agents.md) — so sánh harness (Cursor, Claude Code, Pi…)
- [mcp.md](./mcp.md) — cách agent thực thi tool
- [skills-rules.md](./skills-rules.md), [08-model-notes.md](./08-model-notes.md)
