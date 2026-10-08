# Batch summary

- Backend: `gigachat`  
- Requested model: `GigaChat-2-Max`  
- Model that actually answered: `GigaChat-2-Max:2.0.28.2`  
- JSON mode: native  
- Relevance gate: ON — longest run: 8 steps  
- Total tokens across the batch: 326615  
- Rescored from saved traces in `reports_v2_gate_on` against `questions.bilingual.json` — 2026-10-03 22:02:04Z  

| # | Run | Lang | Question | Steps | Sources | Grounded | Stop met | Voluntary | Judge | Tool err | Gold/abstention | Gold & met | Verbal abst. | Tokens | Answer |
|---|-----|------|----------|-------|---------|----------|----------|-----------|-------|----------|-----------------|------------|--------------|--------|--------|
| 1 | 1 | en | In which city was the person born who is considered a founde… | 4 | 1 | True | True | True | supported | 0 | YES | YES |  | 4459 | London |
| 1 | 2 | en | In which city was the person born who is considered a founde… | 5 | 1 | True | True | True | supported | 1 | YES | YES |  | 7715 | Maida Vale, London |
| 1 | 3 | en | In which city was the person born who is considered a founde… | 4 | 1 | True | True | True | supported | 0 | YES | YES |  | 4346 | Maida Vale, London |
| 1 | 4 | en | In which city was the person born who is considered a founde… | 4 | 1 | True | True | True | supported | 0 | YES | YES |  | 4540 | Maida Vale, London |
| 1 | 5 | en | In which city was the person born who is considered a founde… | 5 | 1 | True | True | True | supported | 0 | YES | YES |  | 4441 | Maida Vale, London |
| 2 | 1 | ru | В каком городе родился человек, которого считают одним из ос… | 5 | 1 | True | True | True | supported | 0 | YES | YES |  | 5366 | Алан Тьюринг родился в Лондоне. |
| 2 | 2 | ru | В каком городе родился человек, которого считают одним из ос… | 7 | 1 | True | True | True | supported | 0 | YES | YES |  | 7233 | Вестминстер |
| 2 | 3 | ru | В каком городе родился человек, которого считают одним из ос… | 5 | 1 | True | True | True | supported | 0 | YES | YES |  | 5799 | Вестминстер |
| 2 | 4 | ru | В каком городе родился человек, которого считают одним из ос… | 5 | 1 | True | True | True | supported | 0 | YES | YES |  | 5415 | Алан Тьюринг родился в Лондоне. |
| 2 | 5 | ru | В каком городе родился человек, которого считают одним из ос… | 7 | 1 | True | True | True | supported | 0 | YES | YES |  | 8174 | Вестминстер |
| 3 | 1 | en | What is the nationality of the mathematician after whom the … | 4 | 1 | True | True | True | supported | 0 | YES | YES |  | 4079 | Dutch |
| 3 | 2 | en | What is the nationality of the mathematician after whom the … | 5 | 1 | True | True | True | supported | 0 | YES | YES |  | 5434 | Edsger W. Dijkstra was Dutch. |
| 3 | 3 | en | What is the nationality of the mathematician after whom the … | 4 | 1 | True | True | True | supported | 0 | YES | YES |  | 3995 | Edsger W. Dijkstra was Dutch. |
| 3 | 4 | en | What is the nationality of the mathematician after whom the … | 4 | 1 | True | True | True | supported | 0 | YES | YES |  | 2515 | Dutch |
| 3 | 5 | en | What is the nationality of the mathematician after whom the … | 4 | 1 | True | True | True | supported | 0 | YES | YES |  | 3361 | Edsger W. Dijkstra was Dutch. |
| 4 | 1 | ru | Какова национальность математика, в честь которого назван ал… | 4 | 1 | True | True | True | supported | 0 | YES | YES |  | 4389 | Эдсгер Дейкстра был голландцем, родившись в Роттердаме и получив образование в Н… |
| 4 | 2 | ru | Какова национальность математика, в честь которого назван ал… | 4 | 1 | True | True | True | supported | 0 | YES | YES |  | 3346 | Эдсгер Дейкстра родился в Роттердаме, следовательно, он является голландцем. |
| 4 | 3 | ru | Какова национальность математика, в честь которого назван ал… | 4 | 1 | True | True | True | supported | 0 | YES | YES |  | 2700 | Национальность математика, в честь которого назван алгоритм Дейкстры, — нидерлан… |
| 4 | 4 | ru | Какова национальность математика, в честь которого назван ал… | 5 | 2 | True | True | True | supported | 0 | YES | YES |  | 4795 | Национальность математика, в честь которого назван алгоритм Дейкстры, — нидерлан… |
| 4 | 5 | ru | Какова национальность математика, в честь которого назван ал… | 4 | 1 | True | False | True | — | 0 | YES | NO | yes | 1652 | Эдсгер Дейкстра родился в Нидерландах, что позволяет предположить его голландско… |
| 5 | 1 | en | Who was the doctoral advisor of the physicist who formulated… | 6 | 2 | True | True | True | supported | 0 | YES | YES |  | 7915 | Arnold Sommerfeld was the doctoral advisor of Werner Heisenberg, the physicist w… |
| 5 | 2 | en | Who was the doctoral advisor of the physicist who formulated… | 4 | 1 | True | True | True | supported | 0 | YES | YES |  | 4392 | Arnold Sommerfeld |
| 5 | 3 | en | Who was the doctoral advisor of the physicist who formulated… | 6 | 2 | True | True | True | supported | 0 | YES | YES |  | 7351 | Arnold Sommerfeld was the doctoral advisor of Werner Heisenberg, the physicist w… |
| 5 | 4 | en | Who was the doctoral advisor of the physicist who formulated… | 6 | 2 | True | True | True | supported | 0 | YES | YES |  | 6352 | Arnold Sommerfeld was the doctoral advisor of Werner Heisenberg, the physicist w… |
| 5 | 5 | en | Who was the doctoral advisor of the physicist who formulated… | 6 | 2 | True | True | True | supported | 0 | YES | YES |  | 6703 | Arnold Sommerfeld was the doctoral advisor of Werner Heisenberg, the physicist w… |
| 6 | 1 | ru | Кто был научным руководителем диссертации физика, сформулиро… | 5 | 1 | True | True | True | supported | 0 | YES | YES |  | 5444 | Научным руководителем диссертации Вернера Гейзенберга был Арнольд Зоммерфельд. |
| 6 | 2 | ru | Кто был научным руководителем диссертации физика, сформулиро… | 5 | 2 | True | True | True | supported | 0 | YES | YES |  | 6338 | Научным руководителем Вернера Гейзенберга был Арнольд Зоммерфельд. |
| 6 | 3 | ru | Кто был научным руководителем диссертации физика, сформулиро… | 8 | 4 | True | True | True | supported | 0 | YES | YES |  | 11420 | Научным руководителем диссертации Вернера Гейзенберга был Арнольд Зоммерфельд. |
| 6 | 4 | ru | Кто был научным руководителем диссертации физика, сформулиро… | 4 | 1 | True | True | True | supported | 0 | YES | YES |  | 3607 | Научным руководителем диссертации Вернера Гейзенберга был Арнольд Зоммерфельд. |
| 6 | 5 | ru | Кто был научным руководителем диссертации физика, сформулиро… | 5 | 1 | True | True | True | supported | 0 | YES | YES |  | 4155 | Научным руководителем диссертации Вернера Гейзенберга был Арнольд Зоммерфельд. |
| 7 | 1 | en | Who created the Python programming language, and in what yea… | 4 | 1 | True | True | True | supported | 0 | YES | YES |  | 4125 | Guido van Rossum created the Python programming language, and its first public r… |
| 7 | 2 | en | Who created the Python programming language, and in what yea… | 4 | 1 | True | True | True | supported | 0 | YES | YES |  | 3732 | Guido van Rossum created the Python programming language, and its first public r… |
| 7 | 3 | en | Who created the Python programming language, and in what yea… | 4 | 1 | True | True | True | supported | 0 | YES | YES |  | 3795 | Guido van Rossum created the Python programming language, and its first public r… |
| 7 | 4 | en | Who created the Python programming language, and in what yea… | 4 | 1 | True | True | True | supported | 0 | YES | YES |  | 2812 | Guido van Rossum created the Python programming language, and its first public r… |
| 7 | 5 | en | Who created the Python programming language, and in what yea… | 4 | 1 | True | True | True | supported | 0 | YES | YES |  | 3177 | Guido van Rossum created the Python programming language, and its first public r… |
| 8 | 1 | ru | Кто создал язык программирования Python и в каком году состо… | 4 | 1 | True | True | True | supported | 0 | YES | YES |  | 3505 | Язык программирования Python был создан Гвидо ван Россумом, а его первый публичн… |
| 8 | 2 | ru | Кто создал язык программирования Python и в каком году состо… | 4 | 1 | True | True | True | supported | 0 | YES | YES |  | 3959 | Язык программирования Python был создан Гвидо ван Россумом и его первая публична… |
| 8 | 3 | ru | Кто создал язык программирования Python и в каком году состо… | 4 | 1 | True | True | True | supported | 0 | YES | YES |  | 3904 | Язык программирования Python был создан Гвидо ван Россумом, а его первый публичн… |
| 8 | 4 | ru | Кто создал язык программирования Python и в каком году состо… | 4 | 1 | True | True | True | supported | 0 | YES | YES |  | 3130 | Язык программирования Python был создан Гвидо ван Россумом, а его первый публичн… |
| 8 | 5 | ru | Кто создал язык программирования Python и в каком году состо… | 4 | 1 | True | True | True | supported | 0 | YES | YES |  | 3591 | Язык программирования Python был создан Гвидо ван Россумом, а его первый публичн… |
| 9 | 1 | en | At which universities did the logician work after whom rever… | 5 | 1 | True | True | True | supported | 0 | YES | YES |  | 5613 | Jan Łukasiewicz, the logician after whom reverse Polish notation is named, worke… |
| 9 | 2 | en | At which universities did the logician work after whom rever… | 5 | 1 | True | True | True | supported | 0 | YES | YES |  | 3935 | Jan Łukasiewicz worked at the University of Lemberg and the University of Warsaw… |
| 9 | 3 | en | At which universities did the logician work after whom rever… | 5 | 1 | True | True | True | supported | 0 | YES | YES |  | 4026 | Jan Łukasiewicz, the logician after whom reverse Polish notation is named, worke… |
| 9 | 4 | en | At which universities did the logician work after whom rever… | 5 | 1 | True | True | True | supported | 0 | YES | YES |  | 4225 | Jan Łukasiewicz, the logician after whom reverse Polish notation is named, worke… |
| 9 | 5 | en | At which universities did the logician work after whom rever… | 5 | 1 | True | True | True | supported | 0 | YES | YES |  | 4231 | Jan Łukasiewicz, the logician after whom reverse Polish notation is named, worke… |
| 10 | 1 | ru | В каких университетах работал логик, в честь которого назван… | 5 | 1 | True | True | True | supported | 0 | YES | YES |  | 5056 | Логиком, в честь которого названа обратная польская запись, является Ян Лукашеви… |
| 10 | 2 | ru | В каких университетах работал логик, в честь которого назван… | 5 | 1 | True | True | True | supported | 0 | YES | YES |  | 4096 | Логиком, в честь которого названа обратная польская запись, является Ян Лукашеви… |
| 10 | 3 | ru | В каких университетах работал логик, в честь которого назван… | 5 | 1 | True | True | True | supported | 0 | YES | YES |  | 4840 | Логиком, в честь которого названа обратная польская запись, является Ян Лукашеви… |
| 10 | 4 | ru | В каких университетах работал логик, в честь которого назван… | 5 | 1 | True | True | True | supported | 0 | YES | YES |  | 3926 | Логиком, в честь которого названа обратная польская запись, является Ян Лукашеви… |
| 10 | 5 | ru | В каких университетах работал логик, в честь которого назван… | 5 | 1 | True | True | True | supported | 0 | YES | YES |  | 4984 | Логиком, в честь которого названа обратная польская запись, является Ян Лукашеви… |
| 11 | 1 | en | Who founded DeepMind, and in which year was the company acqu… | 4 | 1 | True | True | True | supported | 0 | YES | YES |  | 2475 | DeepMind was founded by Demis Hassabis, Shane Legg, and Mustafa Suleyman in Nove… |
| 11 | 2 | en | Who founded DeepMind, and in which year was the company acqu… | 4 | 1 | True | True | True | supported | 0 | YES | YES |  | 3778 | DeepMind was founded by Demis Hassabis, Shane Legg, and Mustafa Suleyman in Nove… |
| 11 | 3 | en | Who founded DeepMind, and in which year was the company acqu… | 4 | 1 | True | True | True | supported | 0 | YES | YES |  | 3825 | DeepMind was founded by Demis Hassabis, Shane Legg, and Mustafa Suleyman in Nove… |
| 11 | 4 | en | Who founded DeepMind, and in which year was the company acqu… | 4 | 1 | True | True | True | supported | 0 | YES | YES |  | 3813 | DeepMind was founded by Demis Hassabis, Shane Legg, and Mustafa Suleyman in Nove… |
| 11 | 5 | en | Who founded DeepMind, and in which year was the company acqu… | 4 | 1 | True | True | True | supported | 0 | YES | YES |  | 2561 | DeepMind was founded by Demis Hassabis, Shane Legg, and Mustafa Suleyman in Nove… |
| 12 | 1 | ru | Кто основал DeepMind и в каком году компания была куплена Go… | 5 | 2 | True | True | True | supported | 0 | YES | YES |  | 5272 | DeepMind была основана в 2010 году Демисом Хассабисом, Шейном Леггом и Мустафой … |
| 12 | 2 | ru | Кто основал DeepMind и в каком году компания была куплена Go… | 4 | 1 | True | True | True | supported | 0 | YES | YES |  | 2664 | Основателями компании DeepMind являются Демис Хассабис, Шейн Легг и Мустафа Суле… |
| 12 | 3 | ru | Кто основал DeepMind и в каком году компания была куплена Go… | 4 | 1 | True | True | True | supported | 0 | YES | YES |  | 2201 | DeepMind была основана в 2010 году Демисом Хассабисом, Шейном Леггом и Мустафой … |
| 12 | 4 | ru | Кто основал DeepMind и в каком году компания была куплена Go… | 4 | 1 | True | True | True | supported | 0 | YES | YES |  | 2530 | Основателями компании DeepMind являются Демис Хассабис, Шейн Легг и Мустафа Суле… |
| 12 | 5 | ru | Кто основал DeepMind и в каком году компания была куплена Go… | 4 | 1 | True | True | True | supported | 0 | YES | YES |  | 2354 | DeepMind была основана Демисом Хассабисом, Шейном Леггом и Мустафой Сулейманом в… |
| 13 | 1 | en | How many lines of source code did the first public release o… | 5 | 1 | True | False | True | — | 0 | YES |  | yes | 4100 | Unable to determine the exact number of lines of source code in the first public… |
| 13 | 2 | en | How many lines of source code did the first public release o… | 5 | 2 | True | False | True | — | 0 | YES |  | yes | 3091 | Insufficient evidence exists within Wikipedia to determine the precise number of… |
| 13 | 3 | en | How many lines of source code did the first public release o… | 5 | 2 | True | False | True | — | 0 | YES |  | yes | 4198 | Insufficient information. The number of lines of source code in the first public… |
| 13 | 4 | en | How many lines of source code did the first public release o… | 5 | 2 | True | False | True | — | 0 | YES |  | yes | 4247 | Insufficient information available on Wikipedia to determine the number of lines… |
| 13 | 5 | en | How many lines of source code did the first public release o… | 5 | 2 | True | False | True | — | 0 | YES |  | yes | 4152 | Based on available Wikipedia articles, the exact number of lines of source code … |
| 14 | 1 | ru | Сколько строк исходного кода содержал первый публичный выпус… | 5 | 2 | True | False | True | — | 0 | YES |  | yes | 3729 | На данный момент невозможно точно указать число строк исходного кода первого пуб… |
| 14 | 2 | ru | Сколько строк исходного кода содержал первый публичный выпус… | 8 | 3 | True | False | True | — | 0 | YES |  | yes | 11989 | На данный момент невозможно точно указать количество строк исходного кода первог… |
| 14 | 3 | ru | Сколько строк исходного кода содержал первый публичный выпус… | 5 | 2 | True | False | True | — | 0 | YES |  | yes | 4912 | На данный момент невозможно определить точное количество строк исходного кода пе… |
| 14 | 4 | ru | Сколько строк исходного кода содержал первый публичный выпус… | 8 | 3 | True | False | True | — | 0 | YES |  | yes | 10063 | На данный момент я не могу предоставить точное число строк исходного кода в перв… |
| 14 | 5 | ru | Сколько строк исходного кода содержал первый публичный выпус… | 6 | 2 | True | False | True | — | 0 | YES |  | yes | 6568 | На данный момент невозможно определить точное число строк исходного кода первого… |

## Reproducibility across repeats

| # | Lang | Stop met | Gold/abstention | Gold & met | Tool err | Question |
|---|------|----------|-----------------|------------|----------|----------|
| 1 | en | 5/5 | 5/5 | 5/5 | 1/5 | In which city was the person born who is considered a founde… |
| 2 | ru | 5/5 | 5/5 | 5/5 | 0/5 | В каком городе родился человек, которого считают одним из ос… |
| 3 | en | 5/5 | 5/5 | 5/5 | 0/5 | What is the nationality of the mathematician after whom the … |
| 4 | ru | 4/5 | 5/5 | 4/5 | 0/5 | Какова национальность математика, в честь которого назван ал… |
| 5 | en | 5/5 | 5/5 | 5/5 | 0/5 | Who was the doctoral advisor of the physicist who formulated… |
| 6 | ru | 5/5 | 5/5 | 5/5 | 0/5 | Кто был научным руководителем диссертации физика, сформулиро… |
| 7 | en | 5/5 | 5/5 | 5/5 | 0/5 | Who created the Python programming language, and in what yea… |
| 8 | ru | 5/5 | 5/5 | 5/5 | 0/5 | Кто создал язык программирования Python и в каком году состо… |
| 9 | en | 5/5 | 5/5 | 5/5 | 0/5 | At which universities did the logician work after whom rever… |
| 10 | ru | 5/5 | 5/5 | 5/5 | 0/5 | В каких университетах работал логик, в честь которого назван… |
| 11 | en | 5/5 | 5/5 | 5/5 | 0/5 | Who founded DeepMind, and in which year was the company acqu… |
| 12 | ru | 5/5 | 5/5 | 5/5 | 0/5 | Кто основал DeepMind и в каком году компания была куплена Go… |
| 13 | en | 0/5 | 5/5 | n/a | 0/5 | How many lines of source code did the first public release o… |
| 14 | ru | 0/5 | 5/5 | n/a | 0/5 | Сколько строк исходного кода содержал первый публичный выпус… |