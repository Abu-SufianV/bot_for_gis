# Чат-бот для Государственных Информационных Систем (ГИС)
Данный проект был мне задан в качестве курсового проекта

Стек технологий: 
- Python 3.10
- SQLite

API и библиотеки:
- pyTelegramBotAPI 4.7.1
- sqlite3
- json
- datetime

### Описание работы бота

При запуске бота, будет предложена регистрация в системе
После прохождения регистрации все данные о пользователе будут добавлены в БД, откуда в дальнейшем будет браться информация

После регистрации станут доступны функции:
- Информация обо мне:
  - ФИО
  - Дата рождения
  - Паспорт
  - СНИЛС
  - Телефон
  - E-mail
- Информация о департаментах:
  - Название
  - Адрес
  - Часы работы
- Подать заявку:
  - Выбираем департаментах
  - Выбираем услугу
  - Сверяем и подтверждаем информацию


### Исполняемые команды
- `/start` — Запуск бота
- `/help` — Описание работы бота

### База Данных

В БД хранится информация о пользователях, заявках, департаментах и услугах

Таблицы:
- USERS
- APPLICATIONS
- DEPARTMENTS
- TARGETS
