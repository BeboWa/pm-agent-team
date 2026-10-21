"""Thin wrapper around the Anthropic API that records time, tokens and cost per run."""
import os
import time
from dataclasses import dataclass

import anthropic

MODEL = os.environ.get("PM_AGENT_MODEL", "claude-sonnet-4-6")
# USD per million tokens (input, output). Update if pricing changes.
PRICING = {"claude-sonnet-4-6": (3.0, 15.0)}


@dataclass
class RunMetrics:
    seconds: float
    input_tokens: int
    output_tokens: int
    cost_usd: float


def call_llm(system: str, user: str, max_tokens: int = 4000):
    client = anthropic.Anthropic()
    start = time.time()
    resp = client.messages.create(
        model=MODEL,
        max_tokens=max_tokens,
        system=system,
        messages=[{"role": "user", "content": user}],
    )
    elapsed = time.time() - start
    text = "".join(b.text for b in resp.content if b.type == "text")
    in_p, out_p = PRICING.get(MODEL, (0.0, 0.0))
    cost = (resp.usage.input_tokens * in_p + resp.usage.output_tokens * out_p) / 1_000_000
    return text, RunMetrics(elapsed, resp.usage.input_tokens, resp.usage.output_tokens, round(cost, 4))
