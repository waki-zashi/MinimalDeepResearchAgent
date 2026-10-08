# Deep Research trace: Who created the Python programming language, and in what year was its first public release?

- Language: `en`  
- Backend / requested model: `gigachat` / `GigaChat-2-Max`  
- Model that actually answered: `GigaChat-2-Max:2.0.28.2` **(differs from the requested identifier — server-side redirect)**  
- JSON mode: native  
- Started (UTC): 2026-10-03 20:37:30Z  
- Elapsed: 17.7 s  
- Steps: 4  
- Run (repeat index): 3  
- Stopped: agent called finish  
- Voluntary finish: True  
- Grounding-gate rejections: 0  
- Relevance-checked: True  
- Relevance judge: **supported** over 1 read passage(s) — The passage explicitly states that 'Guido van Rossum' created Python and mentions that its first public release was in 1991.  
- LLM calls: 6 — tokens: 3795 total (3195 prompt / 600 completion)  
- Reference (gold): 1991  

## Stopping criterion
_provided by user_: Both the creator's name and the year of the first public release are confirmed by read Wikipedia sections.

## Sub-questions
- Who is the creator of the Python programming language?
- In which year did the first public release of Python occur?

## Initial plan
First, find the relevant Wikipedia page about Python. Then extract information regarding its creation and initial release date from reliable sources within the article.

## Reasoning trace
### Step 1 — action: `search`
**Thought:** To find out who created the Python programming language and when its first public release occurred, I need to look up the relevant Wikipedia page.
**Action input:** `{"query": "Python (programming language)", "lang": "en"}`
**Sufficiency note:** Current evidence is insufficient; we have no data yet.
**Observation:**

> - Python (programming language): and garbage collection. Python supports multiple programming paradigms but with an emphasis on object-oriented programming and dynamic typing. Guido
> - Outline of the Python programming language: functional programming. ABC (programming language) – precursor to Python Python was started by Guido van Rossum in 1989 and first released in 1991. Python 2 —
> - History of Python: The programming language Python was conceived in the late 1980s, and its implementation was started in December 1989 by Guido van Rossum at CWI in the
> - Mojo (programming language): Mojo is a programming language for Linux and macOS. It is a system programming language with semantics inspired by Rust such as static typing and a borrow
> - Python syntax and semantics: The syntax of the Python programming language is the set of rules that defines how a Python program will be written and interpreted (by both the runtime

### Step 2 — action: `get_sections`
**Thought:** The search results suggest that 'Guido van Rossum' might be the creator of Python. To confirm this and gather more details, including the year of the first public release, I'll retrieve the sections of the main Python programming language article.
**Action input:** `{"title": "Python (programming language)", "lang": "en"}`
**Sufficiency note:** Evidence suggests Guido's involvement, but confirmation and specific dates require reading the appropriate sections.
**Observation:**

> Sections of 'Python (programming language)':
> [0] (Lead / introduction)
> [1] History
> [2] Design philosophy and features
> [3] Enhancement Proposals
> [4] Syntax and semantics
> [5] Indentation
> [6] Statements and control flow
> [7] Expressions
> [8] Typing
> [9] Arithmetic operations
> [10] Function syntax
> [11] Code examples
> [12] Libraries
> [13] Development environments
> [14] Implementations
> [15] Reference implementation
> [16] Limitations of the reference implementation
> [17] Other implementations
> [18] Unsupported implementations
> [19] Transpilers to other languages
> [20] Performance
> [21] Language development
> [22] Naming
> [23] Languages influenced by Python
> [24] See also
> [25] Notes
> [26] References
> [27] Sources
> [28] Further reading
> [29] External links

### Step 3 — action: `read_section`
**Thought:** The most likely place to find detailed historical information would be under the 'History' section. Reading this should provide us with the necessary details regarding the creation and initial release date of Python.
**Action input:** `{"title": "Python (programming language)", "section": "1", "lang": "en"}`
**Sufficiency note:** We expect to obtain sufficient evidence after reading the history section.
**Observation:**

> Python (programming language) — section 1 [truncated]:
> History
> 
> Main article: History of Python
> 
> The designer of Python, Guido van Rossum, at PyCon US 2024
> 
> Python was conceived in the late 1980s by Guido van Rossum at Centrum Wiskunde & Informatica (CWI) in the Netherlands. It was designed as a successor to the ABC programming language, which was inspired by SETL, capable of exception handling and interfacing with the Amoeba operating system. Python implementation began in December 1989. Van Rossum first released it in 1991 as Python 0.9.0. Van Rossum assumed sole responsibility for the project, as the lead developer, until 12 July 2018, when he announced his "permanent vacation" from responsibilities as Python's "benevolent dictator for life" (BDFL); this title was bestowed on him by the Python community to reflect his long-term commitment as the project's chief decision-maker. In January 2019, active Python core developers elected a five-member Steering Council to lead the project.
> 
> The name Python derives from the British comedy series Monty Python's Flying Circus. (See § Naming.)
> 
> Python 2.0 was released on 16 October 2000, featuring many new features such as list comprehensions, cycle-detecting garbage collection, reference counting, and Unicode support. Python 2.7's end-of-life was initially set for 2015, and then postponed to 2020 out of concern that a large body of existing code could not easily be forward-ported to Python 3. It no longer receives security patches or [truncated]

### Step 4 — action: `finish`
**Thought:** From the history section, it's clear that Guido van Rossum created Python and the first public release happened in 1991. This satisfies our stopping criterion since we've found both pieces of required information directly from the source.
**Action input:** `{"answer": "Guido van Rossum created the Python programming language, and its first public release was in 1991.", "sufficiency": {"met": true, "confidence": 1.0, "justification": "Both the creator's name and the year of the first public release were explicitly stated in the 'History' section."}}`
**Sufficiency note:** Sufficient evidence has been obtained to satisfy the stopping criterion.
**Observation:**

> (finished)

## Final answer
Guido van Rossum created the Python programming language, and its first public release was in 1991.

## Sufficiency judgment
- Met: **True**
- Confidence: 1.0
- Justification: Both the creator's name and the year of the first public release were explicitly stated in the 'History' section.

## Sources (provenance)
- [en] Python (programming language) — section 1 — https://en.wikipedia.org/wiki/Python_(programming_language)
