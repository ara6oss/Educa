# Название продукта
**Educa**

## Описание
**E_learn** - это онлайн платформа, созданная для облегчения процесса обучения. Платформа предоставляет пользователям доступ к разнообразным курсам, тестам и другим образовательным ресурсам. Главная цель проекта - предоставить удобный и эффективный инструмент для обучения и саморазвития.

## Основные возможности
- **Управление курсами**: возможность создания, редактирования и удаления курсов.
- **Пользовательская аутентификация**: регистрация и вход пользователей.
- **Оценка и тестирование**: поддержка тестов и квизов.
- **Отслеживание прогресса**: возможность отслеживания прогресса студентов.

## Установка
Для установки и запуска проекта выполните следующие шаги:

1. **Клонирование репозитория**:

     ```bash
     git clone https://github.com/your_username/E_learn.git
     cd E_learn

2. **Создание виртуального окружения**:

    ```bash
    python -m venv env
    source env/bin/activate  # Для Windows используйте `env\Scripts\activate`

3. **Установка зависимостей**:

   ```bash
   pip install -r requirements.txt

4. **Настройка базы данных**:
  - Убедитесь, что PostgreSQL установлен и база данных создана.
  - Обновите настройки DATABASES в settings.py с данными вашей базы данных.
  - Примените миграции:
      ```bash
      python manage.py makemigrations
      python manage.py migrate


5. **Создание суперпользователя**:

    ```bash
    python manage.py createsuperuser

    
6. **Запуск сервера**:

    ```bash
    python manage.py runserver

