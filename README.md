## Тестовый проект для модуля 24 SkillFactory курса QAP  

Данный проект реализует тесты для REST API сервиса веб-приложения Pet Friends. Тесты написаны с использованием библиотеки `pytest` и проверяют работу методов, предоставляемых библиотекой `api.py`.  

### Структура проекта
```
/project_directory
│
├── /tests # Директория с тестами
│ ├── test_pet_friends.py # Файл с тестами для API Pet Friends
│ └── /images # Директория с изображениями для тестов добавления питомцев и картинок
│
├── api.py # Библиотека для работы с REST API Pet Friends
├── settings.py # Файл с параметрами для тестов (валидные логин и пароль)
└── README.md # Этот файл
```
### Описание компонентов  

 `api.py `  

- Библиотека содержит класс, который реализует методы для взаимодействия с REST API.  
- При инициализации класса объявляется переменная `base_url`, которая используется для формирования URL запросов.  
- Методы класса имеют подробные описания, которые объясняют их функциональность.  

 `tests/test_pet_friends.py`  

- В этом файле располагаются тесты, которые используют методы из `api.py` для проверки функциональности сервиса Pet Friends.  
- Каждый тест проверяет корректность выполнения API запросов и обработку ответов.  

 `settings.py`  

- Этот файл содержит информацию о валидной учетной записи, включая логин и пароль, которые используются для аутентификации при вызове API.  

### Установка  
```
1. Клонируйте репозиторий с проектом на свой локальный компьютер.  
2. Убедитесь, что у вас установлен Python и пакетный менеджер `pip`.  
3. Установите необходимые зависимости, запустив команду:  

   ```bash  
   pip install -r requirements.txt
```
В случае отсутствия файла `requirements.txt`, убедитесь, что у вас установлены `pytest` и другие необходимые библиотеки.

### Запуск тестов
***
Для запуска тестов используйте следующую команду в терминале из корневой директории проекта:
```
pytest tests/
```
### Лицензия
***
Этот проект не является открытым исходным кодом и предназначен только для образовательных целей в рамках курса SkillFactory.

### Контакты
***
Если у вас есть вопросы или комментарии, пожалуйста, свяжитесь с преподавателями курса SkillFactory.

```
### Пояснения к содержимому `README.md`:  

- **Введение**: Начало документа содержит краткое описание проекта и его назначения.  
- **Структура проекта**: Приведен список файлов и директорий с кратким описанием, что они из себя представляют.  
- **Описание компонентов**: Указаны файлы и компоненты с основными задачами и функциями.  
- **Установка**: Инструкции по клонированию репозитория и установке зависимостей.  
- **Запуск тестов**: Как и команду для запуска тестов.  
- **Лицензия** и **Контакты**: Общие предложения о лицензии и как связаться с преподавателем.  

Этот шаблон можно дополнительно настраивать в зависимости от специфики вашего проекта или добавления новых инструкций.
```