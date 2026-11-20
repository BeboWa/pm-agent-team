"""Thin wrapper around the Anthropic API that records time, tokens and cost per run.

If the model hits max_tokens mid-answer, the wrapper automatically asks it to continue
(up to MAX_CONTINUATIONS times) and stitches the pieces together, so a long report is not cut off.
"""
import os
import time
from dataclasses import dataclass

import anthropic

MODEL = os.environ.get("PM_AGENT_MODEL", "claude-sonnet-4-6")
MAX_CONTINUATIONS = 2
# USD per million tokens (input, output). Update if pricing changes.
PRICING = {"claude-sonnet-4-6": (3.0, 15.0)}

RUN_LOG: list = []  # every call's metrics, in order; the Orchestrator reads this

CONTINUE_PROMPT = (
    "Your previous response was cut off by the length limit. Continue exactly where you stopped. "
    "Do not repeat anything and do not add a preamble."
)


@dataclass
class RunMetrics:
    seconds: float
    input_tokens: int
    output_tokens: int
    cost_usd: float
    truncated: bool = False   # True only if the output is STILL cut off after any continuations
    continuations: int = 0    # how many times the wrapper had to ask the model to continue


def call_llm(system: str, user: str, max_tokens: int = 4000):
    client = anthropic.Anthropic()
    start = time.time()
    messages = [{"role": "user", "content": user}]
    parts, in_tok, out_tok, continuations, truncated = [], 0, 0, 0, False

    for attempt in range(MAX_CONTINUATIONS + 1):
        resp = client.messages.create(model=MODEL, max_tokens=max_tokens, system=system, messages=messages)
        part = "".join(b.text for b in resp.content if b.type == "text")
        parts.append(part)
        in_tok += resp.usage.input_tokens
        out_tok += resp.usage.output_tokens
        truncated = getattr(resp, "stop_reason", None) == "max_tokens"
        if not truncated or attempt == MAX_CONTINUATIONS:
            break
        continuations += 1
        messages = messages + [
            {"role": "assistant", "content": part},
            {"role": "user", "content": CONTINUE_PROMPT},
        ]

    elapsed = time.time() - start
    in_p, out_p = PRICING.get(MODEL, (0.0, 0.0))
    cost = (in_tok * in_p + out_tok * out_p) / 1_000_000
    metrics = RunMetrics(elapsed, in_tok, out_tok, round(cost, 4), truncated, continuations)
    RUN_LOG.append(metrics)
    return "".join(parts), metrics
