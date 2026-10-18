import wikipedia, os, time, requests
from wikipedia.exceptions import DisambiguationError, PageError

wikipedia.set_lang('ru')
wikipedia.set_user_agent("RAGLearningProject/0.1 (galimov-student)")
titles = [
"машинное обучение",
"обучение с учителем",
"переобучение",
"кросс-валидация",
"Регуляризация (математика)",
"линейная регрессия",
"логистическая регрессия",
"решающее дерево",
"случайный лес",
"Бустинг",
"метод опорных векторов",
"градиентный спуск",
"метод обратного распространения ошибки",
"искусственная нейронная сеть",
"Трансформер (модель машинного обучения)",
"Большая языковая модель",
"рекомендательная система",
"коллаборативная фильтрация",
"ROC-кривая",
"A/B-тестирование"]
assert len(titles) == 20
           # нужен, чтобы назвать тип ошибки requests.exceptions.JSONDecodeError

def fetch_page(title, attempts=3):
    """Скачать статью; если пришёл «плохой» ответ, подождать и повторить."""
    for attempt in range(1, attempts + 1):
    # range(1, attempts + 1) даёт числа 1, 2, 3: номера попыток
        try:
            page = wikipedia.page(title, auto_suggest=False)
            return page.title, page.content
            # при успехе return сразу отдаёт страницу и выходит из функции (цикл дальше не идёт)
        except requests.exceptions.JSONDecodeError:
            print(f"сбой ответа, попытка {attempt} из {attempts}: {title}")
            time.sleep(attempt* 5)
    return None
    # сюда доходим, только если все попытки неудачны; возвращаем «ничего»


for number, title in enumerate(titles, start = 1):
    try:
        
        filename = f"{number:03d}.txt"
        path = os.path.join("data", filename)
        if os.path.exists(path):
            continue
        page = fetch_page(title, attempts = 5)
        if page is None:
            print("не удалось скачать файл", title)
            continue
        page_title, text = page
        with open(path, "w", encoding= "utf-8") as f:
            f.write(page_title + "\n")
            f.write(text)
            print("сохранено", page_title)
    except DisambiguationError as e:
        print("неоднозначное название", title, e.options)
    except PageError:
        print("статьи нет", title)
    time.sleep(0.5)

