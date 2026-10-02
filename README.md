# Deep Research over Wikipedia — minimal traceable MVP

A minimal Deep Research agent that answers questions by investigating Wikipedia
step by step in a ReAct loop, with an explicit stopping criterion and a full
reasoning trace + provenance written to a Markdown report.

The agent takes information **only from Wikipedia**, through four tools:
`search`, `get_sections`, `read_section` (by section), `finish`.

## Install

```bash
pip install -r requirements.txt
cp .env.example .env      # then put your keys in .env
```

Free backends supported: **Groq** (`GROQ_API_KEY`) and **Gemini** (`GEMINI_API_KEY`).

Model names change over time — override them if a default is retired:
- Groq: `--groq-model llama-3.3-70b-versatile`
- Gemini: `--gemini-model gemini-2.5-flash`

## Run

Single question:

```bash
python run.py --backend groq \
  --question "In which city was the person with a famous test named after him, who founded the theory of computation, born?"
```

With an explicit (human-defined) stopping criterion:

```bash
python run.py --backend gemini \
  --question "Who was the doctoral advisor of the physicist who formulated the uncertainty principle?" \
  --stop-criterion "The physicist is identified AND their doctoral advisor is confirmed by a read Wikipedia section."
```

Batch (multi-hop set, writes a summary table):

```bash
python run.py --backend groq --batch questions.example.json
```

Reports land in `./reports/`: one `NN_question.md` (trace + provenance) and
`NN_question.json` per question, plus `summary.md`.

Useful flags: `--language en|ru`, `--max-steps 8`, `--temperature 0.2`.

## What each report shows

- The stopping criterion and whether it was set by the user or proposed by the agent.
- The plan and sub-questions.
- Every ReAct step: Thought, a sufficiency note, the Action + input, the Observation.
- The final answer, the agent's sufficiency judgment (met / confidence / justification).
- Sources actually read (article + section + URL) for provenance.

## Tests (offline, no network / no keys)

```bash
pip install pytest
pytest -q
```

The tests mock the LLM and Wikipedia, so they verify the loop, the stopping
logic, provenance, and rendering without any API calls.

## Layout

```
config.py             configuration + .env loader
llm.py                Groq / Gemini clients (via requests)
wikipedia_tools.py    MediaWiki API tools + HTML-to-text
prompts.py            planning + ReAct prompt templates
trace.py              trace data model + markdown/json rendering
agent.py              planning, ReAct loop, stopping, provenance
run.py                CLI (single / batch) + summary table
questions.example.json  sample multi-hop questions
tests/                offline mock tests
```

## Notes for the write-up

- The stopping criterion is a first-class, logged object — each run states it
  and the agent judges sufficiency before finishing; when the step budget is hit
  first, the run is marked stopped-at-budget with `met: false`.
- Live Wikipedia responses are not deterministic; record the access date
  (the report timestamps every run in UTC) or pin an offline dump for exact
  reproducibility.
