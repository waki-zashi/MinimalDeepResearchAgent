# Deep Research trace: Кто основал DeepMind и в каком году компания была куплена Google?

- Language: `ru`  
- Backend / requested model: `gigachat` / `GigaChat-2-Max`  
- Model that actually answered: `GigaChat-2-Max:2.0.28.2` **(differs from the requested identifier — server-side redirect)**  
- JSON mode: native  
- Started (UTC): 2026-10-03 20:46:09Z  
- Elapsed: 22.1 s  
- Steps: 5  
- Run (repeat index): 1  
- Stopped: agent called finish  
- Voluntary finish: True  
- Grounding-gate rejections: 0  
- Relevance-checked: True  
- Relevance judge: **supported** over 2 read passage(s) — The passages explicitly state that DeepMind was founded in 2010 by Demis Hassabis, Shane Legg, and Mustafa Suleyman, and it was acquired by Google in 2014.  
- LLM calls: 7 — tokens: 5272 total (4600 prompt / 672 completion)  
- Reference (gold): 2014  

## Stopping criterion
_provided by user_: И основатели, и год покупки подтверждены прочитанными разделами Википедии.

## Sub-questions
- Кто является основателями компании DeepMind?
- В каком году Google приобрела компанию DeepMind?

## Initial plan
Сначала найдем информацию о том, кто именно основал компанию DeepMind. Затем выясним точный год приобретения этой компании компанией Google.

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
**Thought:** Теперь найдем точную информацию из статьи 'Google DeepMind'. Начнем с получения секций этой статьи для поиска нужной информации.
**Action input:** `{"title": "Google DeepMind", "lang": "ru"}`
**Sufficiency note:** Нужно уточнить основателей и дату приобретения компанией Google.
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
**Thought:** Основную информацию об истории создания и приобретении можно найти в разделе 'История' или во введении. Прочитаю введение для начала.
**Action input:** `{"title": "Google DeepMind", "section": "0", "lang": "ru"}`
**Sufficiency note:** Необходимо проверить наличие необходимой информации в других разделах, если она не будет найдена здесь.
**Observation:**

> Google DeepMind — section 0 [truncated]:
> Google DeepMind, ранее DeepMind Technologies, — британская компания, занимающаяся искусственным интеллектом. Основана в 2010 году в Лондоне под названием DeepMind Technologies. В 2014 году была приобретена Google.
> 
> Компания получила известность благодаря разработке компьютерной системы AlphaGo, победившей профессионального игрока в го.
> 
> DeepMind создала нейронную сеть, способную научиться играть в видеоигры на уровне человека.
> 
> В 2020 году компания разработала программу AlphaFold 2, позволяющую решать одну из фундаментальных проблем биологической науки — предсказание структуры белка.
> 
> В 2022 году компания разработала нейросетевой алгоритм AlphaTensor, при помощи которого были найдены несколько новых алгоритмов перемножения матриц небольших размерностей. Так для матриц 4X4 алгоритм Штрассена требует 49 умножений, а AlphaTensor нашёл алгоритм, требующий 47 умножений, но работает он только для поля 
> 
>  Z
> 
>  /
>  
>  2
>  
>  Z
> 
>  {\displaystyle \mathbb {Z} /2\mathbb {Z} }
>  
> .
> 
> В апреле 2023 года компания объединилась с подразделением Google Brain и стала Google DeepMind.
> 
> 10 декабря 2024 года CEO компании Демис Хассабис, лауреат премии Дэна Дэвида (2020), и директор компании Джон Джампер получили Нобелевскую премию по химии за 2024 год, которая была присуждена ему за предсказание структуры белка с помощью разработанной компанией программы AlphaFold 2.
> 
> ↑ DeepMind exec Andrew Eland leaves to launch startup . Дата обращения: 6 февраля 2020. Архивирова [truncated]

### Step 4 — action: `read_section`
**Thought:** Из введения мы узнали, что DeepMind была основана в 2010 году и приобретена Google в 2014 году. Однако информация об основателях отсутствует. Нужно прочитать раздел 'История', чтобы узнать больше.
**Action input:** `{"title": "Google DeepMind", "section": "1", "lang": "ru"}`
**Sufficiency note:** Год основания и дата приобретения подтверждены, но еще нет информации об основателях.
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

### Step 5 — action: `finish`
**Thought:** Теперь у нас есть полная информация: основатели - Демис Хассабис, Шейн Легг, Мустафа Сулейман, и компания была приобретена Google в 2014 году.
**Action input:** `{"answer": "DeepMind была основана в 2010 году Демисом Хассабисом, Шейном Леггом и Мустафой Сулейманом. Компания была приобретена Google в 2014 году.", "sufficiency": {"met": true, "confidence": 1.0, "justification": "Информация об основателях и дате приобретения подтверждена соответствующими разделами статьи."}}`
**Sufficiency note:** Все необходимые данные собраны и подтверждены источниками.
**Observation:**

> (finished)

## Final answer
DeepMind была основана в 2010 году Демисом Хассабисом, Шейном Леггом и Мустафой Сулейманом. Компания была приобретена Google в 2014 году.

## Sufficiency judgment
- Met: **True**
- Confidence: 1.0
- Justification: Информация об основателях и дате приобретения подтверждена соответствующими разделами статьи.

## Sources (provenance)
- [ru] Google DeepMind — section 0 — https://ru.wikipedia.org/wiki/Google_DeepMind
- [ru] Google DeepMind — section 1 — https://ru.wikipedia.org/wiki/Google_DeepMind
