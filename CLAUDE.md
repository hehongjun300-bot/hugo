# Claude

先读 [AGENTS.md](AGENTS.md)。协作规则只维护在那一个文件里，这里不重复。

进度不要手改 `PROJECT_STATUS.md`，用 `python tools/board.py`：

```bash
python tools/board.py pick
python tools/board.py claim P-00X --agent Claude
python tools/board.py finish P-00X --agent Claude --evidence <路径> --next "<下一步>"
```
