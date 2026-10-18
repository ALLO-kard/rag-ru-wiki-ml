# ЗДЕСЬ делается RAG над русской Википедией (ML)

Создается проект по поиску ответов на вопросы

## Запуск
    python -m venv .venv
    .venv\Scripts\activate
    pip install -r requirements.txt
    mkdir data
    python load_data.py
    python chunk.py

## Что я еще проверяю
Мин размер чанка 80 и макс размер 800 выбраны неточно, буду проверять. Макс чанк взят с запасом, потому что буду запускаться на слабой ЛЛМ