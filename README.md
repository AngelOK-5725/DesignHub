# 🎨 DesignHub  
> 🧵 Магазин готовых дизайнов для вышивальных машин (и не только)

![GitHub repo size](https://img.shields.io/github/repo-size/AngelOK-5725/DesignHub?color=blue)
![GitHub last commit](https://img.shields.io/github/last-commit/AngelOK-5725/DesignHub)
![GitHub stars](https://img.shields.io/github/stars/AngelOK-5725/DesignHub?style=social)
![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python)
![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)

---

## 🪡 О проекте
**DesignHub** — это платформа для покупки и загрузки **готовых дизайнерских файлов**.  
На первом этапе проект ориентирован на **вышивальные машины**, но в будущем планируется поддержка **лазерных станков** и **плоттеров**.  

Цель — создать универсальный магазин, где мастера и дизайнеры смогут быстро находить и использовать готовые шаблоны для своих устройств.

---

## 🚀 Возможности
- 🔍 Просмотр и поиск готовых дизайнов  
- 🧷 Категории: *вышивка*, *лазер*, *плоттер*  
- 💾 Поддержка популярных форматов (PES, DST, EXP, SVG, DXF и др.)  
- ⚙️ Удобная структура файлов (`embroidery_designs/`, `laser_designs/` и т.д.)  
- 🌐 Возможность масштабирования до полноценного онлайн-магазина  

---

## 🧱 Текущая структура
DesignHub/
│
├── embroidery_designs/ # Главное Django-приложение
│ │
│ ├── accounts/ # Регистрация и авторизация пользователей
│ ├── designs/ # Управление дизайнами (модели, представления, загрузка)
│ ├── embroidery_desings/ # (главный модуль)
│ ├── payments/ # Обработка платежей и заказов
│ │
│ └── media/designs/ # Хранилище пользовательских файлов
│ ├── files/ # Основные файлы дизайнов (.jef, .pes, .dst и др.)
│ └── manage.py # Основной управляющий скрипт Django
│
├── static/ # Глобальные статические файлы (иконки, CSS, JS)
├── templates/ # HTML-шаблоны
│ └── base.html # Базовый шаблон сайта
│
├── venv/ # Виртуальное окружение Python
├── requirements.txt # Список зависимостей проекта
└── README.md

---

## ⚙️ Установка и запуск

1. Клонируйте репозиторий  
   ```bash
   git clone https://github.com/AngelOK-5725/DesignHub.git
   cd DesignHub

2. Создайте виртуальное окружение и установите зависимости
python -m venv venv
venv\Scripts\activate   # Windows
pip install -r requirements.txt


3. Запустите проект
python manage.py runserver


4. Перейдите по адресу
http://127.0.0.1:8000

🧭 Планы развития
✨ Добавление поддержки дизайнов для лазеров и плоттеров
💳 Интеграция платёжных систем
👩‍🎨 Кабинет дизайнера (добавление своих работ)
🌍 Мультиязычность (RU/EN)
🧠 Интеллектуальный поиск по тегам и стилю дизайна

🤝 Вклад
Хочешь помочь проекту?
Сделай fork репозитория
Создай новую ветку: git checkout -b feature/my-feature
Добавь изменения и закоммить: git commit -m "Добавлена новая функция"
Отправь Pull Request 

Контакты
Автор: @AngelOK-5725
