import types

import shared.llm as llm


def _resp(text, stop, i=100, o=50):
    return types.SimpleNamespace(content=[types.SimpleNamespace(type="text", text=text)], stop_reason=stop,
                                 usage=types.SimpleNamespace(input_tokens=i, output_tokens=o))


def _client(responses):
    seen = []

    class C:
        def __init__(self, *a, **k):
            self.messages = types.SimpleNamespace(create=self.create)

        def create(self, **kw):
            seen.append(kw)
            return responses[min(len(seen) - 1, len(responses) - 1)]
    return C, seen


def test_cut_off_output_is_continued_and_stitched(monkeypatch):
    C, seen = _client([_resp("PART-ONE ", "max_tokens", 100, 50), _resp("PART-TWO", "end_turn", 160, 30)])
    monkeypatch.setattr(llm.anthropic, "Anthropic", C)
    text, m = llm.call_llm("sys", "user")
    assert text == "PART-ONE PART-TWO"
    assert (m.input_tokens, m.output_tokens, m.continuations, m.truncated) == (260, 80, 1, False)
    assert len(seen[1]["messages"]) == 3  # user, partial answer, continue request


def test_output_that_never_finishes_is_flagged(monkeypatch):
    C, seen = _client([_resp("x ", "max_tokens")])
    monkeypatch.setattr(llm.anthropic, "Anthropic", C)
    _, m = llm.call_llm("sys", "user")
    assert m.truncated is True and m.continuations == llm.MAX_CONTINUATIONS
    assert len(seen) == llm.MAX_CONTINUATIONS + 1


def test_normal_call_is_logged_once(monkeypatch):
    C, _ = _client([_resp("done", "end_turn")])
    monkeypatch.setattr(llm.anthropic, "Anthropic", C)
    llm.RUN_LOG.clear()
    llm.call_llm("sys", "user")
    assert len(llm.RUN_LOG) == 1 and llm.RUN_LOG[0].cost_usd > 0
