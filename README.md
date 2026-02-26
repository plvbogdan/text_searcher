# Text Searcher

Поиск по тексту в файлах и архивах (ZIP, 7z, RAR) с сохранением в PostgreSQL.

## Возможности

- Обход папок и подпапок
- Работа с архивами: ZIP, 7z, RAR (включая вложенные)
- Чтение файлов: txt, pdf, docx, xlsx
- Поиск по тексту и именам файлов
- Экспорт данных в формате csv
- Просмотр созданной базы данных в pgweb
- Генерация тестовых данных в папке test_data
  
## Быстрый старт

```bash
# Клонировать репозиторий
git clone git@github.com:plvbogdan/text_searcher.git
cd text_searcher
```
# Создать .env файл
Пример:
```env
DB_HOST=postgres           # имя сервиса в docker-compose
DB_PORT=5432               # стандартный порт PostgreSQL
DB_NAME=text_searcher      # имя базы данных
DB_USER=searcher_user      # пользователь БД
DB_PASSWORD=searcer_password
```

# Сборка и запуск
При первом запуске потребуется время для загрузки образов и установки зависимостей
```bash
docker compose build
./text_searcher.sh


```


## Меню

```
1. Запустить базу данных
2. Запустить краулер
3. Поиск по тексту
4. Экспорт в CSV
5. Открыть pgweb
6. Остановить всё
7. Очистить БД
8. Сгенерировать тестовые файлы
0. Выйти
```

## Тестовые данные

Скрипт `generate_test_files.py` создаёт файлы с текстами Пушкина:
- Стихи и проза в .txt
- Документы .docx, .xlsx, .pdf, .txt
- Архивы ZIP, 7z
- Вложенные архивы

Также можно добавить необходимые файлы в папку /text_searcher/test_data

## Стек

- Python 
- PostgreSQL 
- Docker + docker-compose
