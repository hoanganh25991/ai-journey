# Personal Knowledge-base — videos · docs · GitHub

> **Đã tách repo:** [`~/work-station/personal-kb`](../../personal-kb)  
> Sẽ gắn vào ai-lab như **git submodule** (chưa add — chạy tooling từ sibling path).

Trang root `index.html` chỉ search **notes**. Personal Knowledge-base search video / GitHub / work-station + **Graph RAG** (keywords liên kết).

## Chạy

```bash
cd ~/work-station/personal-kb
python3 scripts/build-kb-index.py
python3 scripts/build-keyword-graph.py
python3 scripts/kb-search.py "first mate"
python3 ui/server.py
# → http://127.0.0.1:8765/      search
# → http://127.0.0.1:8765/graph Graph RAG (nodes tròn, zoom, click)
```

## Tài liệu trong repo Knowledge-base

- [README](../../personal-kb/README.md)
- [Sources](../../personal-kb/data/SOURCES.md)
- [Plan](../../personal-kb/plans/knowledge-base.md)

## Related notes

- [rag.md](./rag.md)
- [embedding.md](./embedding.md)
- [agents.md](./07-agents.md)
