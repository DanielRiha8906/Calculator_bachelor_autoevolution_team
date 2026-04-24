# RAG Index

Master index for the self-maintained knowledge base. Read this file first; then load only the sections relevant to your current task.

## Files

| File | Purpose |
|---|---|
| `rag/codebase_map.md` | Per-file summaries of `src/` — what each module does, its public interface |
| `rag/evolution_log.md` | Per-cycle log — what changed, why, and what tests were affected |
| `rag/patterns.md` | Patterns and anti-patterns discovered across evolution cycles |
| `rag/agent_handoffs.md` | Inter-agent handoff context — what one agent passed to the next |
| `rag/agents/github-task-analyst.md` | Per-agent RAG for the analyst |
| `rag/agents/system-architect.md` | Per-agent RAG for the architect |
| `rag/agents/python-code-implementer.md` | Per-agent RAG for the implementer |
| `rag/agents/pytest-edge-tester.md` | Per-agent RAG for the tester |

## Staleness rule

A RAG entry is stale if its `last-updated` cycle is older than the corresponding file's last git modification. Re-read the source file and refresh the entry before relying on it.
