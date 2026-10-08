# Deep Research trace: How many lines of source code did the first public release of the Python interpreter contain?

- Language: `en`  
- Backend / requested model: `gigachat` / `GigaChat-2-Max`  
- Model that actually answered: `GigaChat-2-Max:2.0.28.2` **(differs from the requested identifier — server-side redirect)**  
- JSON mode: native  
- Started (UTC): 2026-10-03 20:50:04Z  
- Elapsed: 20.9 s  
- Steps: 5  
- Run (repeat index): 5  
- Stopped: agent called finish  
- Voluntary finish: True  
- Grounding-gate rejections: 0  
- Relevance-checked: False  
- LLM calls: 6 — tokens: 4152 total (3355 prompt / 797 completion)  
- Reference (gold): (abstention expected)  

## Stopping criterion
_provided by user_: The number of lines is stated in the text of a read Wikipedia section; if no read section states it, the correct outcome is to report that the evidence is insufficient and to abstain.

## Sub-questions
- What was the first public release version of the Python interpreter?
- Where can I find information about the development history of Python?

## Initial plan
First, identify the first public release version of the Python interpreter from relevant Wikipedia sections. Then, search for detailed historical accounts or technical specifications within these sections that might mention the line count.

## Reasoning trace
### Step 1 — action: `search`
**Thought:** To determine how many lines of source code were in the first public release of the Python interpreter, we need to identify its initial version and gather historical data regarding its development.
**Action input:** `{"query": "Python programming language", "lang": "en"}`
**Sufficiency note:** We don't have any evidence yet; let's start with finding out more about Python's early versions.
**Observation:**

> - Python (programming language): and garbage collection. Python supports multiple programming paradigms but with an emphasis on object-oriented programming and dynamic typing. Guido
> - Outline of the Python programming language: functional programming. ABC (programming language) – precursor to Python Python was started by Guido van Rossum in 1989 and first released in 1991. Python 2 —
> - Mojo (programming language): Mojo is a programming language for Linux and macOS. It is a system programming language with semantics inspired by Rust such as static typing and a borrow
> - History of Python: The programming language Python was conceived in the late 1980s, and its implementation was started in December 1989 by Guido van Rossum at CWI in the
> - Python syntax and semantics: The syntax of the Python programming language is the set of rules that defines how a Python program will be written and interpreted (by both the runtime

### Step 2 — action: `get_sections`
**Thought:** The 'History of Python' page seems relevant since it mentions the conception and implementation timeline. Let's examine its sections to see where details about the first public release might be found.
**Action input:** `{"title": "History of Python", "lang": "en"}`
**Sufficiency note:** No direct evidence so far; we'll check the structure of the 'History of Python' article next.
**Observation:**

> Sections of 'History of Python':
> [0] (Lead / introduction)
> [1] Early history
> [2] Version 1
> [3] BeOpen
> [4] Version 2
> [5] Version 3
> [6] Compatibility
> [7] Features
> [8] Subsequent releases
> [9] Security
> [10] Table of versions
> [11] Support
> [12] See also
> [13] References
> [14] External links

### Step 3 — action: `read_section`
**Thought:** Given our goal is to learn about the first public release, the most promising sections appear to be 'Early history', 'Version 1', and possibly 'Table of versions'. We'll begin with reading the 'Early history' section to understand the context around the first release.
**Action input:** `{"title": "History of Python", "section": "1", "lang": "en"}`
**Sufficiency note:** Still lacking specific line count info; proceeding to investigate further.
**Observation:**

> History of Python — section 1:
> Early history
> 
> Van Rossum first published the code (for Python version 0.9.1) to alt.sources in February 1991. Several features of the language were already present at this stage, among them classes with inheritance, exception handling, functions, and various core datatypes such as list, dict, and str. The initial release also contained a module system borrowed from Modula-3; Van Rossum describes the module as "one of Python's major programming units". Python's exception model also resembled Modula-3's, with the addition of an else clause. In 1994 comp.lang.python, the primary discussion forum for Python, was formed.
> 
> ^ "Python 0.9.1 Part 01/21". alt.sources archives. Archived from the original on August 11, 2021. Retrieved August 11, 2021.
> 
> ^ "History". Python source distribution. Python Foundation. Archived from the original on December 1, 2017. Retrieved November 23, 2017.
> 
> ^ Cite error: The named reference venners-interview-pt-1 was invoked but never defined (see the help page).
> 
> ^ Cite error: The named reference faq-created was invoked but never defined (see the help page).

### Step 4 — action: `read_section`
**Thought:** This section provides valuable background on the first publication of Python's code, specifically mentioning version 0.9.1. However, there is no mention of the number of lines of source code. We should proceed to explore other sections like 'Version 1' or 'Table of versions' which could provide additional insights into the evolution of Python.
**Action input:** `{"title": "History of Python", "section": "2", "lang": "en"}`
**Sufficiency note:** Current evidence does not include the required line count; continuing investigation.
**Observation:**

> History of Python — section 2 [truncated]:
> Version 1
> 
> Python reached version 1.0 in January 1994. The major new features included in this release were the functional programming tools lambda, map, filter and reduce. Van Rossum stated that "Python acquired lambda, reduce(), filter() and map(), courtesy of a Lisp hacker who missed them and submitted working patches".
> 
> The last version released while Van Rossum was at CWI was Python 1.2. In 1995, Van Rossum continued his work on Python at the Corporation for National Research Initiatives (CNRI) in Reston, Virginia from where he released several versions.
> 
> By version 1.4, Python had acquired several new features. Notable among these are the Modula-3 inspired keyword arguments (which are also similar to Common Lisp's keyword arguments) and built-in support for complex numbers. Also included is a basic form of data hiding by name mangling, though this is easily bypassed.
> 
> During Van Rossum's stay at CNRI, he launched the Computer Programming for Everybody (CP4E) initiative, intending to make programming more accessible to more people, with a basic "literacy" in programming languages, similar to the basic English literacy and mathematics skills required by most employers. Python served a central role in this: because of its focus on clean syntax, it was already suitable, and CP4E's goals bore similarities to its predecessor, ABC. The project was funded by DARPA. As of 2007, the CP4E project is inactive, and while Python attempts to  [truncated]

### Step 5 — action: `finish`
**Thought:** Section 'Version 1' gives us insight into the progression of Python up to version 1.0, including notable additions like lambda, map, filter, and reduce. However, there's still no explicit mention of the number of lines of source code in the first public release. Since we've covered significant ground without locating the desired detail, it's reasonable to conclude that Wikipedia doesn't provide this specific piece of information directly.
**Action input:** `{"answer": "Based on available Wikipedia articles, the exact number of lines of source code in the first public release of the Python interpreter is not explicitly documented.", "sufficiency": {"met": false, "confidence": 0.9, "justification": "Despite thorough examination of relevant sections in the 'History of Python' article, no concrete figure for the number of lines of source code has been located."}}`
**Sufficiency note:** After examining key sections, we haven't found the requested line count. It's unlikely that further searching within Wikipedia would yield different results.
**Observation:**

> (finished)

## Final answer
Based on available Wikipedia articles, the exact number of lines of source code in the first public release of the Python interpreter is not explicitly documented.

## Sufficiency judgment
- Met: **False**
- Confidence: 0.9
- Justification: Despite thorough examination of relevant sections in the 'History of Python' article, no concrete figure for the number of lines of source code has been located.

## Sources (provenance)
- [en] History of Python — section 1 — https://en.wikipedia.org/wiki/History_of_Python
- [en] History of Python — section 2 — https://en.wikipedia.org/wiki/History_of_Python
