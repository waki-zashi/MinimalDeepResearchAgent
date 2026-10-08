# Deep Research trace: Who was the doctoral advisor of the physicist who formulated the uncertainty principle?

- Language: `en`  
- Backend / requested model: `gigachat` / `GigaChat-2-Max`  
- Model that actually answered: `GigaChat-2-Max:2.0.28.2` **(differs from the requested identifier — server-side redirect)**  
- JSON mode: native  
- Started (UTC): 2026-10-03 20:32:51Z  
- Elapsed: 23.3 s  
- Steps: 4  
- Run (repeat index): 2  
- Stopped: agent called finish  
- Voluntary finish: True  
- Grounding-gate rejections: 0  
- Relevance-checked: True  
- Relevance judge: **supported** over 1 read passage(s) — The passage explicitly states that Werner Heisenberg received his doctorate 'under Sommerfeld'.  
- LLM calls: 6 — tokens: 4392 total (3847 prompt / 545 completion)  
- Reference (gold): Sommerfeld, Зоммерфельд  

## Stopping criterion
_provided by user_: The physicist behind the uncertainty principle is identified AND their doctoral advisor is confirmed by a read Wikipedia section.

## Sub-questions
- Who formulated the uncertainty principle?
- What is the name of the doctoral advisor of the physicist who formulated the uncertainty principle?

## Initial plan
First, identify the physicist associated with formulating the uncertainty principle. Then, find information about their academic background on Wikipedia, specifically looking for details regarding their doctoral advisor.

## Reasoning trace
### Step 1 — action: `search`
**Thought:** The question asks for the doctoral advisor of the physicist who formulated the uncertainty principle. First, I need to identify the physicist responsible for formulating the uncertainty principle.
**Action input:** `{"query": "uncertainty principle", "lang": "en"}`
**Sufficiency note:** Current evidence does not include the identity of the physicist nor their doctoral advisor.
**Observation:**

> - Uncertainty principle: The uncertainty principle, also known as Heisenberg's indeterminacy principle, is a fundamental concept in quantum mechanics. It states that there is
> - Fourier transform: domain and vice versa, a phenomenon known as the uncertainty principle. The critical case for this principle is the Gaussian function, of substantial importance
> - Uncertainty principle (disambiguation): uncertainty principle in Wiktionary, the free dictionary. Heisenberg's uncertainty principle is a fundamental concept in quantum physics. Uncertainty
> - Uncertainty: Heisenberg's uncertainty principle allows. The term 'radical uncertainty' was popularised by John Kay and Mervyn King in their book Radical Uncertainty: Decision-Making
> - Discrete Fourier transform: analogous uncertainty principle is not useful, because the uncertainty will not be shift-invariant. Still, a meaningful uncertainty principle has been

### Step 2 — action: `get_sections`
**Thought:** From the search results, it's clear that the uncertainty principle is associated with Heisenberg. Next, I'll look up more details about Heisenberg to find his doctoral advisor.
**Action input:** `{"title": "Werner Heisenberg", "lang": "en"}`
**Sufficiency note:** We have identified the physicist but haven't found the doctoral advisor yet.
**Observation:**

> Sections of 'Werner Heisenberg':
> [0] (Lead / introduction)
> [1] Early life and education
> [2] Early years
> [3] University studies
> [4] Personal life
> [5] Academic career
> [6] Göttingen, Copenhagen and Leipzig
> [7] Matrix mechanics and the Nobel Prize
> [8] Interpretation of quantum theory
> [9] <i>SS</i> investigation
> [10] German nuclear weapons program
> [11] Pre-war work on physics
> [12] Membership in the Uranverein
> [13] Post-Second World War
> [14] 1945: Alsos Mission
> [15] 1945: Reaction to Hiroshima
> [16] Post-war research career
> [17] Executive positions at German research institutions
> [18] Promotion of international scientific cooperation
> [19] Research interests
> [20] Philosophy and worldview
> [21] Political stance
> [22] Autobiography and death
> [23] Honors and awards
> [24] Research reports on nuclear physics
> [25] Other research publications
> [26] Published books
> [27] In popular culture
> [28] See also
> [29] References
> [30] Footnotes
> [31] Citations
> [32] Bibliography
> [33] External links

### Step 3 — action: `read_section`
**Thought:** To find out who Heisenberg's doctoral advisor was, I should focus on sections related to his early academic background. Section [3], 'University studies', seems like a good place to start looking for this information.
**Action input:** `{"title": "Werner Heisenberg", "section": "3", "lang": "en"}`
**Sufficiency note:** Still waiting for confirmation of the doctoral advisor.
**Observation:**

> Werner Heisenberg — section 3 [truncated]:
> University studies
> 
> Heisenberg in 1924
> 
> From 1920 to 1923, he studied physics and mathematics at the Ludwig-Maximilians-Universität München under Arnold Sommerfeld and Wilhelm Wien and at the University of Göttingen with Max Born and James Franck and mathematics with David Hilbert. He received his doctorate in 1923 at the Ludwig-Maximilians-Universität München under Sommerfeld.
> 
> In June 1922, Sommerfeld took Heisenberg to Göttingen to attend the Bohr Festival, because Sommerfeld had a sincere interest in his students and knew of Heisenberg's interest in Niels Bohr's theories on atomic physics. At the event, Bohr was a guest lecturer and gave a series of comprehensive lectures on quantum atomic physics and Heisenberg met Bohr for the first time, which had a lasting effect on him.
> 
> Heisenberg's doctoral thesis, the topic of which was suggested by Sommerfeld, was on turbulence; the thesis discussed both the stability of laminar flow and the nature of turbulent flow. The problem of stability was investigated by the use of the Orr–Sommerfeld equation, a fourth-order linear differential equation for small disturbances from laminar flow. He briefly returned to this topic after World War II.
> 
> At Göttingen, under Born, he completed his habilitation in 1924 with a Habilitationsschrift (habilitation thesis) on the anomalous Zeeman effect.
> 
> In his youth, he was a member and Scoutleader of the Neupfadfinder, a German Scout association and part of [truncated]

### Step 4 — action: `finish`
**Thought:** Based on the section, we learn that Heisenberg received his doctorate under Arnold Sommerfeld. This satisfies our requirement to confirm the doctoral advisor.
**Action input:** `{"answer": "Arnold Sommerfeld", "sufficiency": {"met": true, "confidence": 1.0, "justification": "Directly observed in the relevant Wikipedia section."}}`
**Sufficiency note:** All necessary information has been obtained.
**Observation:**

> (finished)

## Final answer
Arnold Sommerfeld

## Sufficiency judgment
- Met: **True**
- Confidence: 1.0
- Justification: Directly observed in the relevant Wikipedia section.

## Sources (provenance)
- [en] Werner Heisenberg — section 3 — https://en.wikipedia.org/wiki/Werner_Heisenberg
