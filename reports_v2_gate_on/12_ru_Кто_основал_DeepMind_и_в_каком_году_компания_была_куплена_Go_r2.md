# Deep Research trace: Кто основал DeepMind и в каком году компания была куплена Google?

- Language: `ru`  
- Backend / requested model: `gigachat` / `GigaChat-2-Max`  
- Model that actually answered: `GigaChat-2-Max:2.0.28.2` **(differs from the requested identifier — server-side redirect)**  
- JSON mode: native  
- Started (UTC): 2026-10-03 20:46:31Z  
- Elapsed: 15.9 s  
- Steps: 4  
- Run (repeat index): 2  
- Stopped: agent called finish  
- Voluntary finish: True  
- Grounding-gate rejections: 0  
- Relevance-checked: True  
- Relevance judge: **supported** over 1 read passage(s) — The passage explicitly states that Demis Hassabis, Shane Legg, and Mustafa Suleyman founded DeepMind Technologies in 2010, and it also mentions that Google announced the acquisition of DeepMind Technologies on January 26, 2014.  
- LLM calls: 6 — tokens: 2664 total (2087 prompt / 577 completion)  
- Reference (gold): 2014  

## Stopping criterion
_provided by user_: И основатели, и год покупки подтверждены прочитанными разделами Википедии.

## Sub-questions
- Кто является основателями компании DeepMind?
- В каком году Google приобрела компанию DeepMind?

## Initial plan
Сначала найдем информацию о том, кто именно основал компанию DeepMind. Затем выясним, когда именно Google приобрел эту компанию. После того как обе эти детали будут найдены и проверены на страницах соответствующих статей в Википедии, мы сможем уверенно ответить на вопрос.

## Reasoning trace
### Step 1 — action: `search`
**Thought:** Сначала нужно найти статью о DeepMind на русском языке.
**Action input:** `{"query": "DeepMind", "lang": "ru"}`
**Sufficiency note:** Не хватает информации об основателях и дате приобретения компанией Google.
**Observation:**

> - Google DeepMind: Google DeepMind, ранее DeepMind Technologies, — британская компания, занимающаяся искусственным интеллектом. Основана в 2010 году в Лондоне под названием
> - Хассабис, Демис: за предсказания фолдинга белков с помощью разработанной его компанией DeepMind программы AlphaFold. В декабре 2025 года американский журнал Time назвал
> - AlphaFold: программа на базе искусственного интеллекта (AI), разработанная Google DeepMind, которая выполняет предсказания пространственной структуры белка. Программа
> - Google Brain: команда была объединена с бывшей дочерней компанией Google – DeepMind и образовала Google DeepMind. Миссия Google Brain заключается в улучшении жизни людей
> - Gemini (языковая модель): семейство мультимодальных больших языковых моделей (LLM), разработанное Google DeepMind и являющееся преемником LaMDA и PaLM 2. Эта модель лежит в основе одноимённого

### Step 2 — action: `get_sections`
**Thought:** Теперь получим структуру статьи 'Google DeepMind' для поиска нужной информации.
**Action input:** `{"title": "Google DeepMind", "lang": "ru"}`
**Sufficiency note:** Нужно уточнить информацию из соответствующих разделов статьи.
**Observation:**

> Sections of 'Google DeepMind':
> [0] (Lead / introduction)
> [1] История
> [2] Направление исследований
> [3] Нейронная машина Тьюринга
> [4] Глубинное обучение с подкреплением в видеоиграх
> [5] AlphaStar
> [6] Генерация видео
> [7] Игра в го
> [8] Другие направления
> [9] DeepMind Health
> [10] Сотрудничество с университетами
> [11] Примечания

### Step 3 — action: `read_section`
**Thought:** Раздел 'История' может содержать информацию об основателях и дате приобретения компанией Google.
**Action input:** `{"title": "Google DeepMind", "section": "1", "lang": "ru"}`
**Sufficiency note:** Необходимо прочитать раздел 'История', чтобы подтвердить или опровергнуть текущие предположения.
**Observation:**

> Google DeepMind — section 1 [truncated]:
> История
> [править | править код]
> 
> В 2010 году Демис Хассабис, Шейн Легг, Мустафа Сулейман основали стартап DeepMind Technologies. До того Хассабис и Легг уже были знакомы по Университетскому Колледжу Лондона, где работали в подразделении вычислительной нейробиологии Gatsby (Gatsby Computational Neuroscience Unit, www.gatsby.ucl.ac.uk).
> 
> В компанию вложились большие венчурные фонды Horizons Ventures, Founders Fund, а также предприниматели Скотт Банистер и Илон Маск. Ян Таллинн был одним из ранних инвесторов и советников компании.
> 
> В 2014 DeepMind получила награду «Компания года» от Компьютерной лаборатории Кембриджского университета.
> 
> 26 января 2014 года Google объявил о приобретении DeepMind Technologies. По разным сообщениям сумма сделки составила от 400 до 650 миллионов долларов. Сообщается, что сделка состоялась после того, как Facebook прекратил переговоры о покупке DeepMind Technologies в 2013 году. Одним из условий сделки DeepMind с Google было создание последней коллегии по этическим проблемам искусственного интеллекта.
> 
> После покупки Google компания стала называться Google DeepMind.
> 
> В начале сентября 2016 года компания перешла в родительскую компанию Google — Alphabet, а из её названия исчезло упоминание Google, теперь она известна как DeepMind Technologies Limited или же DeepMind. Также веб-сайт компании сменил дизайн.
> 
> В апреле 2023 года DeepMind объединилась с подразделением Google Brain и образовала Google DeepMind в рамках [truncated]

### Step 4 — action: `finish`
**Thought:** Из раздела 'История' мы узнали, что основателями являются Демис Хассабис, Шейн Легг и Мустафа Сулейман, а дата приобретения компанией Google - январь 2014 года.
**Action input:** `{"answer": "Основателями компании DeepMind являются Демис Хассабис, Шейн Легг и Мустафа Сулейман. Компания была приобретена Google в январе 2014 года.", "sufficiency": {"met": true, "confidence": 1.0, "justification": "Информация об основателях и дате приобретения подтверждена прочитанным разделом 'История'."}}`
**Sufficiency note:** Имеется вся необходимая информация для ответа на вопрос.
**Observation:**

> (finished)

## Final answer
Основателями компании DeepMind являются Демис Хассабис, Шейн Легг и Мустафа Сулейман. Компания была приобретена Google в январе 2014 года.

## Sufficiency judgment
- Met: **True**
- Confidence: 1.0
- Justification: Информация об основателях и дате приобретения подтверждена прочитанным разделом 'История'.

## Sources (provenance)
- [ru] Google DeepMind — section 1 — https://ru.wikipedia.org/wiki/Google_DeepMind
