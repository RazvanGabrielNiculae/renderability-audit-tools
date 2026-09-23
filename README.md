# Renderability Audit Tools

Dependency-free audit of what remains usable in the raw HTML response before JavaScript execution.

It measures visible raw-HTML words and checks server-delivered title, canonical, hreflang, JSON-LD and semantic content landmarks. It does **not** claim to emulate Google, ChatGPT, Claude, Perplexity, or a browser renderer.

```bash
python3 tools/audit_renderability.py https://example.com/
python3 -m unittest discover -s tests -v
```

A PASS means the configured raw-HTML invariants were present in the fetched response. It does not guarantee indexing, ranking, citation, or rendering parity.
