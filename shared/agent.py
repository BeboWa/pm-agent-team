"""Shared runner for agents: call the model, append run metrics, save the report."""
from __future__ import annotations
from pathlib import Path

from shared.llm import call_llm
from shared.paths import out_path


def run_agent(system_prompt: str, user_msg: str, out_file: str, max_tokens: int = 5000) -> str:
    text, m = call_llm(system_prompt, user_msg, max_tokens=max_tokens)
    text += (
        f"\n\n---\n_Run metrics: {m.seconds:.1f}s, "
        f"{m.input_tokens} in / {m.output_tokens} out tokens, ~${m.cost_usd}_\n"
    )
    path = out_path(out_file)
    path.write_text(text)
    print(text)
    print(f"\nSaved to {path}")
    return text


def read_optional(path):
    return Path(path).read_text() if path else None
