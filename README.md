## phpMyAdmin_parser

## Запуск проекта

### Предварительные требования

- Установите [Python](https://www.python.org/downloads/) (версия 3.8 или выше)
- Установите [uv](https://github.com/astral-sh/uv) (альтернатива pip/pipenv/poetry)

### Установка
- Создайте и активируйте виртуальное окружение
``` 
uv venv
```
- Установите зависимости 
``` 
uv sync
```

### Запуск

- Запустите скрипт посредством make 
``` 
make run
```
- или запустите напрямую 
``` 
uv run main.py
```