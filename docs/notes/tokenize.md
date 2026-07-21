# Tokenize

> Text → tokens → IDs. Model không đọc chữ — nó đọc số.

## Slides & demo

| | Link |
|--|------|
| Slides | [slides/tokenize](../slides/tokenize/index.html) |
| Working app | [demos/tokenize/app](../demos/tokenize/app/index.html) |

## Ý chính
- Word / subword (BPE, WordPiece, SentencePiece) / char
- Vocabulary cố định → mỗi token một ID
- Sai tokenizer = sai input cho mọi bước sau

## Protonx
- `byte-pair-encoding-bpe.md`, `day-2-assignment-wordpiece-tokenizer.ipynb`
- Ảnh: `tokenizer-viz.jpg`, `bpe-vs-wordpiece.png`, `build-vocab.jpg`

## Related demos
- [embedding](../demos/embedding/), [sentiment](../demos/sentiment/)

