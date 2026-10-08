# Batch summary

- Backend: `gigachat`  
- Requested model: `GigaChat-2-Max`  
- Model that actually answered: `GigaChat-2-Max:2.0.28.2`  
- JSON mode: native  
- Relevance gate: OFF — longest run: 9 steps  
- Total tokens across the batch: 342874  
- Rescored from saved traces in `reports_v2_gate_off`, `reports_v2_patch_trap_ru` (excluding 5 run(s) aborted by transport failures) against `questions.bilingual.json` — 2026-10-03 22:04:33Z  

| # | Run | Lang | Question | Steps | Sources | Grounded | Stop met | Voluntary | Judge | Tool err | Gold/abstention | Gold & met | Verbal abst. | Tokens | Answer |
|---|-----|------|----------|-------|---------|----------|----------|-----------|-------|----------|-----------------|------------|--------------|--------|--------|
| 1 | 1 | en | In which city was the person born who is considered a founde… | 5 | 2 | True | True | True | — | 0 | YES | YES |  | 6392 | Maida Vale, London |
| 1 | 2 | en | In which city was the person born who is considered a founde… | 4 | 1 | True | True | True | — | 0 | YES | YES |  | 5336 | Maida Vale, London |
| 1 | 3 | en | In which city was the person born who is considered a founde… | 4 | 1 | True | True | True | — | 0 | YES | YES |  | 3169 | Maida Vale, London |
| 1 | 4 | en | In which city was the person born who is considered a founde… | 4 | 1 | True | True | True | — | 0 | YES | YES |  | 3540 | Maida Vale, London |
| 1 | 5 | en | In which city was the person born who is considered a founde… | 4 | 1 | True | True | True | — | 0 | YES | YES |  | 3753 | Maida Vale, London |
| 2 | 1 | ru | В каком городе родился человек, которого считают одним из ос… | 4 | 1 | True | True | True | — | 0 | YES | YES |  | 4849 | Вестминстер |
| 2 | 2 | ru | В каком городе родился человек, которого считают одним из ос… | 6 | 1 | True | True | True | — | 0 | YES | YES |  | 5931 | Лондон |
| 2 | 3 | ru | В каком городе родился человек, которого считают одним из ос… | 5 | 1 | True | True | True | — | 0 | YES | YES |  | 4797 | Алан Тьюринг родился в Лондоне. |
| 2 | 4 | ru | В каком городе родился человек, которого считают одним из ос… | 9 | 1 | True | True | True | — | 0 | YES | YES |  | 12556 | Лондон |
| 2 | 5 | ru | В каком городе родился человек, которого считают одним из ос… | 6 | 1 | True | True | True | — | 0 | YES | YES |  | 5145 | Вестминстер |
| 3 | 1 | en | What is the nationality of the mathematician after whom the … | 4 | 1 | True | True | True | — | 0 | YES | YES |  | 2141 | Edsger W. Dijkstra was Dutch. |
| 3 | 2 | en | What is the nationality of the mathematician after whom the … | 4 | 1 | True | True | True | — | 0 | YES | YES |  | 3103 | Edsger W. Dijkstra was Dutch. |
| 3 | 3 | en | What is the nationality of the mathematician after whom the … | 4 | 1 | True | True | True | — | 0 | YES | YES |  | 2817 | Edsger W. Dijkstra was Dutch. |
| 3 | 4 | en | What is the nationality of the mathematician after whom the … | 5 | 1 | True | True | True | — | 0 | YES | YES |  | 3605 | Edsgar W. Dijkstra, the mathematician after whom Dijkstra's algorithm is named, … |
| 3 | 5 | en | What is the nationality of the mathematician after whom the … | 5 | 1 | True | True | True | — | 0 | YES | YES |  | 3235 | Edsger W. Dijkstra was Dutch. |
| 4 | 1 | ru | Какова национальность математика, в честь которого назван ал… | 4 | 1 | True | True | True | — | 0 | YES | YES |  | 3745 | Эдсгер Дейкстра был голландцем. |
| 4 | 2 | ru | Какова национальность математика, в честь которого назван ал… | 4 | 1 | True | True | True | — | 0 | YES | YES |  | 2318 | Эдсгер Дейкстра был голландцем. |
| 4 | 3 | ru | Какова национальность математика, в честь которого назван ал… | 4 | 1 | True | True | True | — | 0 | YES | YES |  | 3710 | Национальность математика, в честь которого назван алгоритм Дейкстры, — нидерлан… |
| 4 | 4 | ru | Какова национальность математика, в честь которого назван ал… | 4 | 1 | True | True | True | — | 0 | YES | YES |  | 1774 | Голландец |
| 4 | 5 | ru | Какова национальность математика, в честь которого назван ал… | 4 | 1 | True | True | True | — | 0 | YES | YES |  | 1378 | Национальность математика, в честь которого назван алгоритм Дейкстры, — нидерлан… |
| 5 | 1 | en | Who was the doctoral advisor of the physicist who formulated… | 7 | 3 | True | True | True | — | 0 | YES | YES |  | 9065 | Arnold Sommerfeld was the doctoral advisor of Werner Heisenberg, the physicist w… |
| 5 | 2 | en | Who was the doctoral advisor of the physicist who formulated… | 6 | 2 | True | True | True | — | 0 | YES | YES |  | 5370 | Arnold Sommerfeld was the doctoral advisor of Werner Heisenberg, the physicist w… |
| 5 | 3 | en | Who was the doctoral advisor of the physicist who formulated… | 6 | 2 | True | True | True | — | 0 | YES | YES |  | 6652 | Arnold Sommerfeld was the doctoral advisor of Werner Heisenberg, the physicist w… |
| 5 | 4 | en | Who was the doctoral advisor of the physicist who formulated… | 4 | 1 | True | True | True | — | 0 | YES | YES |  | 3047 | Arnold Sommerfeld |
| 5 | 5 | en | Who was the doctoral advisor of the physicist who formulated… | 6 | 2 | True | True | True | — | 0 | YES | YES |  | 7614 | Arnold Sommerfeld was the doctoral advisor of Werner Heisenberg, the physicist w… |
| 6 | 1 | ru | Кто был научным руководителем диссертации физика, сформулиро… | 5 | 2 | True | True | True | — | 0 | YES | YES |  | 6233 | Научным руководителем диссертации Вернера Гейзенберга был Арнольд Зоммерфельд. |
| 6 | 2 | ru | Кто был научным руководителем диссертации физика, сформулиро… | 8 | 3 | True | True | True | — | 0 | NO | NO |  | 10623 | Научным руководителем Вернера Гейзенберга был Макс Борн. |
| 6 | 3 | ru | Кто был научным руководителем диссертации физика, сформулиро… | 6 | 2 | True | True | True | — | 0 | YES | YES |  | 7504 | Научным руководителем Вернера Гейзенберга был Арнольд Зоммерфельд. |
| 6 | 4 | ru | Кто был научным руководителем диссертации физика, сформулиро… | 6 | 3 | True | True | True | — | 0 | YES | YES |  | 8741 | Научным руководителем диссертации Вернера Гейзенберга был Арнольд Зоммерфельд. |
| 6 | 5 | ru | Кто был научным руководителем диссертации физика, сформулиро… | 6 | 3 | True | True | True | — | 0 | YES | YES |  | 8162 | Научным руководителем диссертации Вернера Гейзенберга был Арнольд Зоммерфельд. |
| 7 | 1 | en | Who created the Python programming language, and in what yea… | 4 | 1 | True | True | True | — | 0 | YES | YES |  | 3592 | Guido van Rossum created the Python programming language, and its first public r… |
| 7 | 2 | en | Who created the Python programming language, and in what yea… | 4 | 1 | True | True | True | — | 0 | YES | YES |  | 3286 | Guido van Rossum created the Python programming language, and its first public r… |
| 7 | 3 | en | Who created the Python programming language, and in what yea… | 4 | 1 | True | True | True | — | 0 | YES | YES |  | 4196 | Guido van Rossum created the Python programming language, and its first public r… |
| 7 | 4 | en | Who created the Python programming language, and in what yea… | 4 | 1 | True | True | True | — | 0 | YES | YES |  | 3038 | Guido van Rossum created the Python programming language, and its first public r… |
| 7 | 5 | en | Who created the Python programming language, and in what yea… | 4 | 1 | True | True | True | — | 0 | YES | YES |  | 2911 | Guido van Rossum created the Python programming language, and its first public r… |
| 8 | 1 | ru | Кто создал язык программирования Python и в каком году состо… | 4 | 1 | True | True | True | — | 0 | YES | YES |  | 2856 | Язык программирования Python был создан Гвидо ван Россумом, а его первый публичн… |
| 8 | 2 | ru | Кто создал язык программирования Python и в каком году состо… | 4 | 1 | True | True | True | — | 0 | YES | YES |  | 2415 | Язык программирования Python был создан Гвидо ван Россумом, а его первый публичн… |
| 8 | 3 | ru | Кто создал язык программирования Python и в каком году состо… | 4 | 1 | True | True | True | — | 0 | YES | YES |  | 2676 | Язык программирования Python был создан Гвидо ван Россумом, а его первый публичн… |
| 8 | 4 | ru | Кто создал язык программирования Python и в каком году состо… | 4 | 1 | True | True | True | — | 0 | YES | YES |  | 3787 | Язык программирования Python был создан Гвидо ван Россумом, а его первый публичн… |
| 8 | 5 | ru | Кто создал язык программирования Python и в каком году состо… | 4 | 1 | True | True | True | — | 0 | YES | YES |  | 3420 | Язык программирования Python был создан Гвидо ван Россумом, а его первый публичн… |
| 9 | 1 | en | At which universities did the logician work after whom rever… | 5 | 1 | True | True | True | — | 0 | YES | YES |  | 5190 | Jan Łukasiewicz, the logician after whom reverse Polish notation is named, worke… |
| 9 | 2 | en | At which universities did the logician work after whom rever… | 5 | 1 | True | True | True | — | 0 | YES | YES |  | 2887 | Jan Łukasiewicz, the logician after whom reverse Polish notation is named, worke… |
| 9 | 3 | en | At which universities did the logician work after whom rever… | 6 | 2 | True | True | True | — | 0 | YES | YES |  | 8129 | Jan Łukasiewicz, the inventor of Polish notation, worked at the University of Le… |
| 9 | 4 | en | At which universities did the logician work after whom rever… | 5 | 1 | True | True | True | — | 0 | YES | YES |  | 4181 | Jan Łukasiewicz, the logician after whom reverse Polish notation is named, worke… |
| 9 | 5 | en | At which universities did the logician work after whom rever… | 5 | 1 | True | True | True | — | 0 | YES | YES |  | 3531 | Jan Łukasiewicz worked at the University of Lemberg and the University of Warsaw… |
| 10 | 1 | ru | В каких университетах работал логик, в честь которого назван… | 5 | 1 | True | True | True | — | 0 | YES | YES |  | 3553 | Логиком, в честь которого названа обратная польская запись, является Ян Лукашеви… |
| 10 | 2 | ru | В каких университетах работал логик, в честь которого назван… | 5 | 1 | True | True | True | — | 0 | YES | YES |  | 4644 | Логиком, в честь которого названа обратная польская запись, является Ян Лукашеви… |
| 10 | 3 | ru | В каких университетах работал логик, в честь которого назван… | 5 | 1 | True | True | True | — | 0 | YES | YES |  | 4018 | Логиком, в честь которого названа обратная польская запись, является Ян Лукашеви… |
| 10 | 4 | ru | В каких университетах работал логик, в честь которого назван… | 5 | 1 | True | True | True | — | 0 | YES | YES |  | 4669 | Логиком, в честь которого названа обратная польская запись, является Ян Лукашеви… |
| 10 | 5 | ru | В каких университетах работал логик, в честь которого назван… | 5 | 1 | True | True | True | — | 0 | YES | YES |  | 4063 | Логиком, в честь которого названа обратная польская запись, является Ян Лукашеви… |
| 11 | 1 | en | Who founded DeepMind, and in which year was the company acqu… | 4 | 1 | True | True | True | — | 0 | YES | YES |  | 3232 | DeepMind was founded by Demis Hassabis, Shane Legg, and Mustafa Suleyman in Nove… |
| 11 | 2 | en | Who founded DeepMind, and in which year was the company acqu… | 4 | 1 | True | True | True | — | 0 | YES | YES |  | 3602 | DeepMind was founded by Demis Hassabis, Shane Legg, and Mustafa Suleyman in Nove… |
| 11 | 3 | en | Who founded DeepMind, and in which year was the company acqu… | 4 | 1 | True | True | True | — | 0 | YES | YES |  | 3861 | DeepMind was founded by Demis Hassabis, Shane Legg, and Mustafa Suleyman in Nove… |
| 11 | 4 | en | Who founded DeepMind, and in which year was the company acqu… | 4 | 1 | True | True | True | — | 0 | YES | YES |  | 3468 | DeepMind was founded by Demis Hassabis, Shane Legg, and Mustafa Suleyman in Nove… |
| 11 | 5 | en | Who founded DeepMind, and in which year was the company acqu… | 4 | 1 | True | True | True | — | 0 | YES | YES |  | 2553 | DeepMind was founded by Demis Hassabis, Shane Legg, and Mustafa Suleyman in Nove… |
| 12 | 1 | ru | Кто основал DeepMind и в каком году компания была куплена Go… | 4 | 1 | True | True | True | — | 0 | YES | YES |  | 3408 | DeepMind была основана в 2010 году Демисом Хассабисом, Шейном Леггом и Мустафой … |
| 12 | 2 | ru | Кто основал DeepMind и в каком году компания была куплена Go… | 4 | 1 | True | True | True | — | 0 | YES | YES |  | 3376 | Основателями DeepMind являются Демис Хассабис, Шейн Легг и Мустафа Сулейман. Ком… |
| 12 | 3 | ru | Кто основал DeepMind и в каком году компания была куплена Go… | 4 | 1 | True | True | True | — | 0 | YES | YES |  | 3053 | Основателями компании DeepMind являются Демис Хассабис, Шейн Легг и Мустафа Суле… |
| 12 | 4 | ru | Кто основал DeepMind и в каком году компания была куплена Go… | 4 | 1 | True | True | True | — | 0 | YES | YES |  | 3204 | Основателями компании DeepMind являются Демис Хассабис, Шейн Легг и Мустафа Суле… |
| 12 | 5 | ru | Кто основал DeepMind и в каком году компания была куплена Go… | 4 | 1 | True | True | True | — | 0 | YES | YES |  | 2896 | Основателями компании DeepMind являются Демис Хассабис, Шейн Легг и Мустафа Суле… |
| 13 | 1 | en | How many lines of source code did the first public release o… | 5 | 2 | True | False | True | — | 0 | YES |  | yes | 4961 | Insufficient evidence available from Wikipedia to determine the number of lines … |
| 13 | 2 | en | How many lines of source code did the first public release o… | 5 | 2 | True | False | True | — | 0 | YES |  | yes | 5809 | Insufficient evidence: The number of lines of source code in the first public re… |
| 13 | 3 | en | How many lines of source code did the first public release o… | 4 | 1 | True | False | True | — | 0 | YES |  | yes | 3346 | Unable to determine based on available Wikipedia sources. |
| 13 | 4 | en | How many lines of source code did the first public release o… | 5 | 2 | True | False | True | — | 0 | YES |  | yes | 4878 | Insufficient evidence available on Wikipedia to determine the number of lines of… |
| 13 | 5 | en | How many lines of source code did the first public release o… | 5 | 2 | True | False | True | — | 0 | YES |  | yes | 5472 | Insufficient information. The exact number of lines of source code in the first … |
| 14 | 1 | ru | Сколько строк исходного кода содержал первый публичный выпус… | 8 | 3 | True | False | True | — | 0 | YES |  | yes | 14006 | На данный момент нет доступной информации о точном количестве строк исходного ко… |
| 14 | 2 | ru | Сколько строк исходного кода содержал первый публичный выпус… | 6 | 2 | True | False | True | — | 0 | YES |  | yes | 7935 | На данный момент невозможно определить точное количество строк исходного кода в … |
| 14 | 3 | ru | Сколько строк исходного кода содержал первый публичный выпус… | 7 | 2 | True | False | True | — | 0 | YES |  | yes | 6141 | На данный момент невозможно точно указать количество строк исходного кода в перв… |
| 14 | 4 | ru | Сколько строк исходного кода содержал первый публичный выпус… | 8 | 3 | True | False | True | — | 0 | YES |  | yes | 12798 | На данный момент не удалось установить точное количество строк исходного кода пе… |
| 14 | 5 | ru | Сколько строк исходного кода содержал первый публичный выпус… | 8 | 3 | True | False | True | — | 0 | YES |  | yes | 11528 | На данный момент нет достаточной информации для определения количества строк исх… |

## Reproducibility across repeats

| # | Lang | Stop met | Gold/abstention | Gold & met | Tool err | Question |
|---|------|----------|-----------------|------------|----------|----------|
| 1 | en | 5/5 | 5/5 | 5/5 | 0/5 | In which city was the person born who is considered a founde… |
| 2 | ru | 5/5 | 5/5 | 5/5 | 0/5 | В каком городе родился человек, которого считают одним из ос… |
| 3 | en | 5/5 | 5/5 | 5/5 | 0/5 | What is the nationality of the mathematician after whom the … |
| 4 | ru | 5/5 | 5/5 | 5/5 | 0/5 | Какова национальность математика, в честь которого назван ал… |
| 5 | en | 5/5 | 5/5 | 5/5 | 0/5 | Who was the doctoral advisor of the physicist who formulated… |
| 6 | ru | 5/5 | 4/5 | 4/5 | 0/5 | Кто был научным руководителем диссертации физика, сформулиро… |
| 7 | en | 5/5 | 5/5 | 5/5 | 0/5 | Who created the Python programming language, and in what yea… |
| 8 | ru | 5/5 | 5/5 | 5/5 | 0/5 | Кто создал язык программирования Python и в каком году состо… |
| 9 | en | 5/5 | 5/5 | 5/5 | 0/5 | At which universities did the logician work after whom rever… |
| 10 | ru | 5/5 | 5/5 | 5/5 | 0/5 | В каких университетах работал логик, в честь которого назван… |
| 11 | en | 5/5 | 5/5 | 5/5 | 0/5 | Who founded DeepMind, and in which year was the company acqu… |
| 12 | ru | 5/5 | 5/5 | 5/5 | 0/5 | Кто основал DeepMind и в каком году компания была куплена Go… |
| 13 | en | 0/5 | 5/5 | n/a | 0/5 | How many lines of source code did the first public release o… |
| 14 | ru | 0/5 | 5/5 | n/a | 0/5 | Сколько строк исходного кода содержал первый публичный выпус… |