# Batch summary

- Backend: `gigachat`  
- Requested model: `GigaChat-2-Max`  
- Model that actually answered: `GigaChat-2-Max:2.0.28.2`  
- JSON mode: native  
- Relevance gate: ON — longest run: 5 steps  
- Total tokens across the batch: 54428  
- Rescored from saved traces in `reports_v2_dijkstra` against `questions.dijkstra.json` — 2026-10-03 22:02:04Z  

| # | Run | Lang | Question | Steps | Sources | Grounded | Stop met | Voluntary | Judge | Tool err | Gold/abstention | Gold & met | Verbal abst. | Tokens | Answer |
|---|-----|------|----------|-------|---------|----------|----------|-----------|-------|----------|-----------------|------------|--------------|--------|--------|
| 1 | 1 | en | What is the nationality of the mathematician after whom the … | 4 | 1 | True | True | True | supported | 0 | YES | YES |  | 3726 | Edsger W. Dijkstra was Dutch. |
| 1 | 2 | en | What is the nationality of the mathematician after whom the … | 4 | 1 | True | True | True | supported | 0 | YES | YES |  | 3622 | Edsger W. Dijkstra was Dutch. |
| 1 | 3 | en | What is the nationality of the mathematician after whom the … | 4 | 1 | True | True | True | supported | 0 | YES | YES |  | 3018 | Edsger W. Dijkstra was Dutch. |
| 1 | 4 | en | What is the nationality of the mathematician after whom the … | 4 | 1 | True | True | True | supported | 0 | YES | YES |  | 3178 | Dutch |
| 1 | 5 | en | What is the nationality of the mathematician after whom the … | 4 | 1 | True | True | True | supported | 0 | YES | YES |  | 2602 | Edsger W. Dijkstra was Dutch. |
| 1 | 6 | en | What is the nationality of the mathematician after whom the … | 5 | 1 | True | True | True | supported | 0 | YES | YES |  | 4160 | Edsgar W. Dijkstra, the mathematician after whom Dijkstra's algorithm is named, … |
| 1 | 7 | en | What is the nationality of the mathematician after whom the … | 4 | 1 | True | True | True | supported | 0 | YES | YES |  | 3263 | Edsger W. Dijkstra was Dutch. |
| 1 | 8 | en | What is the nationality of the mathematician after whom the … | 4 | 1 | True | True | True | supported | 0 | YES | YES |  | 2713 | Edsger W. Dijkstra was Dutch. |
| 1 | 9 | en | What is the nationality of the mathematician after whom the … | 4 | 1 | True | True | True | supported | 0 | YES | YES |  | 2148 | Edsger W. Dijkstra was Dutch. |
| 2 | 1 | ru | Какова национальность математика, в честь которого назван ал… | 4 | 1 | True | True | True | supported | 0 | YES | YES |  | 3482 | Алгоритм Дейкстры назван в честь нидерландского ученого Эдсгера Дейкстры. |
| 2 | 2 | ru | Какова национальность математика, в честь которого назван ал… | 4 | 1 | True | True | True | supported | 0 | YES | YES |  | 2500 | Эдсгер Дейкстра был голландским математиком и информатиком. |
| 2 | 3 | ru | Какова национальность математика, в честь которого назван ал… | 4 | 1 | True | True | True | supported | 0 | YES | YES |  | 3211 | Эдсгер Дейкстра был родом из Нидерландов, следовательно, его национальность - го… |
| 2 | 4 | ru | Какова национальность математика, в честь которого назван ал… | 4 | 1 | True | False | True | — | 0 | YES | NO |  | 2853 | Эдсгер Дейкстра родился в Нидерландах и получил образование там, что позволяет п… |
| 2 | 5 | ru | Какова национальность математика, в честь которого назван ал… | 4 | 1 | True | True | True | supported | 0 | YES | YES |  | 2833 | Эдсгер Дейкстра родился в Роттердаме, Нидерланды, следовательно, он являлся голл… |
| 2 | 6 | ru | Какова национальность математика, в честь которого назван ал… | 4 | 1 | True | True | True | supported | 0 | YES | YES |  | 3171 | Эдсгер Дейкстра, в честь которого назван алгоритм Дейкстры, является нидерландск… |
| 2 | 7 | ru | Какова национальность математика, в честь которого назван ал… | 4 | 1 | True | True | True | supported | 0 | YES | YES |  | 2291 | Эдсгер Дейкстра был голландцем. |
| 2 | 8 | ru | Какова национальность математика, в честь которого назван ал… | 4 | 1 | True | True | True | supported | 0 | YES | YES |  | 2309 | Эдсгер Дейкстра родился в Роттердаме, Нидерланды, следовательно, его национально… |
| 2 | 9 | ru | Какова национальность математика, в честь которого назван ал… | 4 | 1 | True | True | True | supported | 0 | YES | YES |  | 3348 | Эдсгер Дейкстра родился в Нидерландах, следовательно, он был голландцем. |

## Reproducibility across repeats

| # | Lang | Stop met | Gold/abstention | Gold & met | Tool err | Question |
|---|------|----------|-----------------|------------|----------|----------|
| 1 | en | 9/9 | 9/9 | 9/9 | 0/9 | What is the nationality of the mathematician after whom the … |
| 2 | ru | 8/9 | 9/9 | 8/9 | 0/9 | Какова национальность математика, в честь которого назван ал… |