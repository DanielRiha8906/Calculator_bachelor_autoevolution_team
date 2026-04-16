# CLAUDE.md

Bachelor thesis project: **self-evolving software** — a system capable of autonomously modifying its own source code.

This repository serves as an experimental research environment for the practical part of the thesis. Development may occur across multiple isolated git worktrees and branches, where each worktree represents a separate experimental line and must be treated as an independent context.

Because of that, safety, traceability, and reproducibility are critical: careless changes here are not just bugs, they are research invalidation.

---

## Project overview

- Language: Python 3.12
- Virtual environment: `.venv/` (managed via pip/venv)
- Goal: implement and document a self-evolving software prototype as part of a bachelor thesis

---

## Safe change rules

These rules exist because the subject of this project is code that modifies itself. Any unsafe practice here undermines both the research integrity and reproducibility.

- **Never modify code without reading it first.** Understand what a function does before changing it.
- **One concern per change.** Do not mix refactoring with feature work, or feature work with bug fixes. Each commit should be explainable in a single sentence.
- **Do not modify the self-modification engine and its tests in the same commit.** These must be independently verifiable.
- **No speculative changes.** Do not add abstractions, generalization, or "future-proofing" unless the thesis explicitly requires it.
- **Prefer reversible operations.** When in doubt, write to a new file/branch before overwriting.
- **No destructive file operations** (`rm -rf`, overwriting output files without backup) without explicit confirmation.
- **Sandboxing requirement:** any code the self-evolving system generates or modifies must be executed in an isolated subprocess or sandbox — never `exec()`/`eval()` on untrusted strings in the main process.
- **Do not auto-apply AI-generated patches to the running codebase** without a human review step in the loop.
- **Do not add, remove, or upgrade dependencies unless the task explicitly requires it.**
- **Any dependency change must be logged and justified** because it affects experiment reproducibility.

---

## Testing

- Run tests before and after every non-trivial change: `python -m pytest`
- All self-modification outputs (generated code, patches) must have a corresponding test asserting the output is syntactically valid Python before it is written to disk.
- Tests live alongside source code; do not delete tests to make a failing suite pass.
- Coverage is not the goal — correctness of the self-evolution loop is. Prioritize integration tests over unit tests for the core mutation/patch pipeline.
- If a test is skipped, it must have a comment explaining why with a TODO referencing what needs to change for it to be re-enabled.

---

## Git hygiene

- **Branch per experiment.** Each self-evolution run or hypothesis gets its own branch: `experiment/<description>`.
- **Commit messages:** imperative mood, present tense, ≤72 chars subject. Body explains *why*, not *what*.
- **Never commit to `main` directly.** Always work through an experiment branch or worktree branch and review.
- **Never amend published commits.** If a fix is needed, make a new commit.
- **Tag reproducible baselines.** When a stable state is reached that will be referenced in the thesis, tag it: `git tag -a v0.x -m "description"`.
- **Prefer separating generator changes from generated outputs.** This rule may be ignored when generating artifacts is required to reproduce or evaluate the experiment.  
- **Keep commits atomic.** `git add -p` is preferred over `git add .` to avoid accidentally staging debug output, logs, or temporary files.
- **When operating inside a worktree, treat that worktree branch as the primary target branch.**
- **Do not assume the repository default branch is the correct integration target.**

---

## Worktree isolation and branch scope

This project may use multiple git worktrees for parallel experimental development.
Each worktree branch must be treated as an isolated experiment context.

- **Treat the currently checked out branch as the only valid working context.**
- **Do not inspect, compare against, depend on, or modify files from other worktrees or experiment branches** unless those changes already exist in the current branch.
- **Do not assume other branches contain authoritative, approved, or compatible implementations.**
- **Default merge target is the current worktree branch or its explicitly designated parent branch — never assume `main`.**
- **Do not propose, perform, or automate cross-branch synchronization, cleanup, or consolidation** unless explicitly requested.
- **Do not open pull requests targeting `main` from experimental worktree branches** unless explicitly instructed.
- **Before making changes, confirm the current branch and treat it as the experiment boundary.**
- **Do not create, switch, or retarget branches during autonomous operation** unless the workflow explicitly instructs it.

These rules exist to preserve experiment isolation, reproducibility, and valid thesis evaluation.

## Secrets and credentials

- **Never commit API keys, tokens, or passwords.** Use environment variables loaded via `.env` (already in `.gitignore`).
- **Never hardcode model names, endpoints, or API base URLs** as string literals in source — use config files or environment variables so the thesis experiments are reproducible with different providers.
- **Audit before committing:** if a file contains anything that looks like a key (`sk-`, `Bearer`, `token=`, long random strings), do not commit it.
- `.env` and `.envrc` are already in `.gitignore` — keep them there. Never rename them to bypass the ignore rule.
- If secrets are accidentally committed, treat the secret as compromised immediately and rotate it before doing anything else.

---

## Self-evolving system specific rules

- **Immutable core principle:** the self-evolution loop must not directly modify `CLAUDE.md`, `.gitignore`, thesis documentation, or branch-policy files during normal operation.
- **Project level behavioral changes:** If project-level behavioral changes are needed, they must be proposed in `suggestions/update_claude.md` instead of being applied automatically.
- **All patches produced by the system must be diff-format artifacts** stored under `patches/` or `output/` — not silently applied.
- **Every evolution cycle must be logged** (inputs, outputs, diffs, timestamps) so experiments can be reproduced and cited in the thesis.
- **No network calls from generated code** unless explicitly scoped and authorized. Generated code must not exfiltrate data.
- **Exit conditions matter.** The system must have a hard stop condition that does not depend on the evolving code itself — implement this in a part of the codebase that is never touched by the self-modifier.
- **Do not modify external systems, databases, remote services, or persistent shared resources** unless explicitly authorized by the workflow or task.


---

## Claude as the auto-evolution engine

In this project, Claude (this instance) **is** the self-evolution engine. It is invoked automatically by a GitHub Actions workflow — not by a human typing in a terminal. This section defines what that means and what constraints apply in that context.

### How it works

1. A GitHub Actions workflow triggers Claude Code on a schedule or on a specific event (e.g., a push, a label on an issue, or a manual dispatch).
2. Claude receives a task — a mutation goal, a failing test, a performance target, or a research hypothesis — and autonomously produces code changes.
3. Those changes are committed only within the currently active branch/worktree context. If the workflow includes pull request creation, a pull request may be opened for human review only against the correct non-`main` target branch unless explicitly instructed otherwise. Claude does **not** merge its own PRs.

### Responsibilities in autonomous mode

- **Read the task carefully before acting.** The workflow will pass a task description; treat it as the sole source of truth for what needs to change.
- **Produce the smallest change that satisfies the task.** Avoid touching files outside the task scope.
- **Always run tests before committing.** A cycle that breaks tests must not produce a commit — it must log the failure and stop.
- **Write a summary to `progress.md`** at the end of every run (files changed, purpose, risks, test results, number of tokens used, cost in USD, number of turns). This is required for thesis reproducibility.
- **Open a PR, never merge.** The PR description must include: what changed, why, which tests passed, and any risks or open questions.
- **If the task is ambiguous or unsafe, do nothing and leave a comment** on the triggering issue/PR explaining what clarification is needed.
- **Treat the current worktree branch as the full scope of the task.** Do not inspect or reason across sibling experiment branches.
- **If running inside a worktree-based experiment branch, preserve branch isolation.** Do not retarget work toward `main` by default.
- **When opening a PR, target the current experiment lineage branch, not `main`, unless explicitly instructed otherwise.**


### Hard limits that apply even in autonomous mode

- Never directly modify: `CLAUDE.md`, `.gitignore`, `.github/workflows/`, or thesis documentation during autonomous runs.
- If changes to project-level behavior are needed, propose them via `suggestions/update_claude.md` instead.
- Never commit secrets, credentials, or `.env` files.
- Never merge an experiment worktree branch into `main` unless explicitly instructed by the user.
- Never inspect or use sibling worktree branches as implementation context.
- Never treat another experiment branch as a fallback source of truth.
- Never push directly to `main`.
- Never apply a self-generated patch to the live codebase without it first being written as a diff artifact under `patches/` or `output/`.
- Never make network calls from within generated or evolved code unless the workflow explicitly authorizes it via an environment variable (`ALLOW_NETWORK=1`).
- If the workflow provides no clear stopping condition, stop after one iteration and report.

---


## Allowed changes without extra discussion

- Add or improve tests
- Refactor small internal code paths without changing behavior
- Improve docstrings and inline comments
- Add logging related to experiment reproducibility
- Suggest branch names and commit messages

---

## Code style

- Prefer explicit, readable Python over compact clever code
- Use type hints for new public functions
- Keep functions small and single-purpose
- Add docstrings to modules involved in the self-evolution loop

---

## Logging

Before any commit, append a run summary to `progress.md` including:

- files changed
- purpose of the change
- risks
- how it was tested
- whether all tests passed
- number of tokens used
- estimated cost in USD
- number of turns
- current branch/worktree name
- intended merge or PR target

---

## Artifacts

- Diagrams should be written in plant uml language and should be placed in folder 'artifacts/'
- Development should be logged using these diagrams:
    - Class diagram files for core classes
    - Activity diagram
    - Sequence Diagram


---

## File placement

- New source files go in `src/`
- New test files go in `tests/`
- Development artifacts go in `artifacts/`
- Suggested policy or workflow changes go in `suggestions/`
- Keep source code, tests, and generated artifacts separate

---

## CLAUDE.md change proposals

Project-level behavior, safety policy, workflow rules, or experiment-governance changes must not be applied directly during autonomous operation.

If such a change is needed:

- Create a proposal file in `suggestions/update_claude.md`
- The proposal must clearly describe:
  - what should be **added**
  - what should be **changed**
  - what should be **removed**
  - why the change is necessary
  - what risk or ambiguity the change resolves
- Treat this proposal as a human-review artifact, not an automatically applied change