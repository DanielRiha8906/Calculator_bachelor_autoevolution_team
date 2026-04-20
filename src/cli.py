"""Backward-compatibility re-export — implementation lives in src.presentation.cli."""
from src.presentation.cli import _eval_node, parse_and_evaluate, run_cli

__all__ = ["_eval_node", "parse_and_evaluate", "run_cli"]
