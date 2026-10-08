# Deep Research trace: Who founded DeepMind, and in which year was the company acquired by Google?

- Language: `en`  
- Backend / requested model: `gigachat` / `GigaChat-2-Max`  
- Model that actually answered: `GigaChat-2-Max:2.0.28.2` **(differs from the requested identifier — server-side redirect)**  
- JSON mode: native  
- Started (UTC): 2026-10-03 20:08:26Z  
- Elapsed: 21.3 s  
- Steps: 4  
- Run (repeat index): 2  
- Stopped: agent called finish  
- Voluntary finish: True  
- Grounding-gate rejections: 0  
- Relevance-checked: False  
- LLM calls: 5 — tokens: 3602 total (3109 prompt / 493 completion)  
- Reference (gold): 2014  

## Stopping criterion
_provided by user_: Both the founders and the year of the acquisition are confirmed by read Wikipedia sections.

## Sub-questions
- Who were the founders of DeepMind?
- In what year did Google acquire DeepMind?

## Initial plan
First, find the relevant Wikipedia page for DeepMind. Then extract information about its founding members from the article. Next, locate details on when Google acquired DeepMind within the same or related articles.

## Reasoning trace
### Step 1 — action: `search`
**Thought:** To find out who founded DeepMind and when it was acquired by Google, I need to look up the relevant Wikipedia page.
**Action input:** `{"query": "DeepMind"}`
**Sufficiency note:** Current evidence is insufficient; need to retrieve the appropriate article.
**Observation:**

> - Google DeepMind: DeepMind Technologies Limited, trading as Google DeepMind or simply DeepMind, is a British-American artificial intelligence (AI) research laboratory which
> - AlphaGo: program that plays the board game Go. It was developed by the London-based DeepMind Technologies, an acquired subsidiary of Google. Subsequent versions of
> - Gemini (language model): models (LLMs) developed by Google DeepMind, and the successor to LaMDA and PaLM 2. Comprising Gemini Pro, Gemini Deep Think, Gemini Flash, and Gemini Flash
> - Gato (DeepMind): blocks, and more. Gato was created by researchers at London-based AI firm DeepMind. It is a transformer, like GPT-3. According to MIT Technology Review, the
> - AlphaGo versus Lee Sedol: the DeepMind Challenge Match, was a five-game Go match between top Go player Lee Sedol and AlphaGo, a computer Go program developed by DeepMind, played

### Step 2 — action: `get_sections`
**Thought:** The most promising result seems to be 'Google DeepMind'. I'll fetch its sections to see where the founder's names might appear.
**Action input:** `{"title": "Google DeepMind"}`
**Sufficiency note:** Still no direct evidence; need to inspect the article's structure.
**Observation:**

> Sections of 'Google DeepMind':
> [0] (Lead / introduction)
> [1] History
> [2] Products and technologies
> [3] Games
> [4] AlphaGo and successors
> [5] AlphaStar
> [6] Datacenter operation
> [7] Protein folding
> [8] Genomics
> [9] Language models
> [10] AlphaCode
> [11] Gemini
> [12] Gemma
> [13] SIMA
> [14] Habermas machine
> [15] Generative AI
> [16] Video generation
> [17] Music generation
> [18] Environment generation
> [19] Robotics
> [20] Others
> [21] Football
> [22] Archaeology
> [23] Materials science
> [24] Mathematics
> [25] AlphaTensor
> [26] AlphaGeometry
> [27] AlphaProof
> [28] AlphaDev
> [29] AlphaEvolve
> [30] AI-assisted scientific research
> [31] Chip design
> [32] Safety
> [33] Weather prediction
> [34] Miscellaneous contributions to Google
> [35] Neuroscience research
> [36] DeepMind Health
> [37] NHS data-sharing controversy
> [38] DeepMind Ethics and Society
> [39] DeepMind Professors of machine learning
> [40] See also
> [41] References
> [42] External links

### Step 3 — action: `read_section`
**Thought:** The 'History' section likely contains details about the founding and acquisition of DeepMind.
**Action input:** `{"title": "Google DeepMind", "section": "1"}`
**Sufficiency note:** Need to confirm the founders and acquisition date within the history section.
**Observation:**

> Google DeepMind — section 1 [truncated]:
> History
> 
> The start-up was founded by Demis Hassabis, Shane Legg and Mustafa Suleyman in November 2010. Hassabis and Legg first met at the Gatsby Computational Neuroscience Unit at University College London (UCL). The goal of the founders is to create a general-purpose AI that can be useful and effective for almost anything. Hassabis said that the start-up began working on artificial intelligence technology by teaching it how to play Atari video games from the seventies and eighties including Breakout, Pong, and Space Invaders. AI was introduced to the games without any programmed knowledge of how to play. After a period flailing around, AI would eventually learn what worked, and over time even become an expert in it. "The cognitive processes which the AI goes through are said to be very like those of a human who had never seen the game would use to understand and attempt to master it."
> 
> Logo from 2015–2016
> 
> Logo from 2016–2019
> 
> Major venture capital firms Horizons Ventures and Founders Fund invested in the company, as well as entrepreneurs Scott Banister, Peter Thiel, and Elon Musk. Jaan Tallinn was an early investor and an adviser to the company. DeepMind needed a well-funded backer to pay its employees, provide compute resources and further expand. It was courted by Facebook, Musk, Google and some others.
> 
> On 26 January 2014, Google confirmed its acquisition of DeepMind for a price reportedly ranging between $400 million and $650 mil [truncated]

### Step 4 — action: `finish`
**Thought:** I have identified the founders of DeepMind and the year of its acquisition by Google. Now I will summarize my findings into a coherent answer.
**Action input:** `{"answer": "DeepMind was founded by Demis Hassabis, Shane Legg, and Mustafa Suleyman in November 2010. It was acquired by Google in January 2014.", "sufficiency": {"met": true, "confidence": 1.0, "justification": "Both the founders and the acquisition date are explicitly stated in the 'History' section of the 'Google DeepMind' Wikipedia article."}}`
**Sufficiency note:** All necessary information has been retrieved and verified.
**Observation:**

> (finished)

## Final answer
DeepMind was founded by Demis Hassabis, Shane Legg, and Mustafa Suleyman in November 2010. It was acquired by Google in January 2014.

## Sufficiency judgment
- Met: **True**
- Confidence: 1.0
- Justification: Both the founders and the acquisition date are explicitly stated in the 'History' section of the 'Google DeepMind' Wikipedia article.

## Sources (provenance)
- [en] Google DeepMind — section 1 — https://en.wikipedia.org/wiki/Google_DeepMind
