<div align="center">
  <h1>🐱 Приключение Лунного Кота 🌙</h1>
  <p>2D-платформер с уникальной механикой лунных прыжков и волнами врагов</p>
  
  <img src="https://img.shields.io/badge/Python-3.8+-yellow?logo=python" alt="Python">
  <img src="https://img.shields.io/badge/Pygame-2.5+-red?logo=pygame" alt="Pygame">
  <img src="https://img.shields.io/badge/Version-1.3.0-green" alt="Version">
  
  <br>
  <img src="Скриншоты игры\Screenshot 2025-06-19 211211.png" alt="Игровой процесс" width="300">
  <img src="Скриншоты игры\Screenshot 2025-06-19 211818.png" alt="Игровой процесс" width="300">
  <img src="Скриншоты игры\Screenshot 2025-06-19 211902.png" alt="Игровой процесс" width="300">
  <img src="Скриншоты игры\Screenshot 2025-06-19 211734.png" alt="Игровой процесс" width="300">
</div>

## 🎮 Особенности игры
- 🌠 **Лунные прыжки** - специальная способность с ограниченным зарядом
- ❤️ **Система жизней** - 3 попытки перед окончательной смертью
- 🌊 **Волны врагов** - каждые 20 убийств активируется интенсивный спавн
- 🎵 **Полное звуковое сопровождение** - 5+ уникальных звуковых эффектов
- 🏆 **Система рекордов** - сохраняется между сеансами игры
- 🔄 **Мгновенный рестарт** - по нажатию любой клавиши после смерти

## 🚀 Быстрый старт
```bash
# Клонировать репозиторий
git clone https://github.com/your-username/moon-cat-adventure.git
cd moon-cat-adventure

# Установить зависимости (рекомендуется использовать виртуальное окружение)
python -m pip install -r requirements.txt

# Запустить игру
python main.py

## ⚙️ Установка
```bash
# Клонировать репозиторий
git clone https://github.com/pofack06/myfirstgame.git

# Перейти в директорию проекта
cd myfirstgame

# Установить зависимости
pip install -r requirements.txt
```

## 🕹️ Управление
<table> <tr> <th>Клавиша</th> <th>Действие</th> </tr> <tr> <td><code>A/D</code></td> <td>Движение влево/вправо</td> </tr> <tr> <td><code>W</code></td> <td>Обычный прыжок</td> </tr> <tr> <td><code>X</code></td> <td>Лунный прыжок (усиленный)</td> </tr> <tr> <td><code>ESC</code></td> <td>Пауза/продолжить игру</td> </tr> </table>

## 🏗️ Структура проекта
```bash
.
├── main.py            # Главный запускающий файл
├── menu.py            # Система меню с анимациями
├── game.py            # Основная игровая логика
├── entities.py        # Классы игровых объектов
├── constants.py       # Константы и настройки
├── utils.py           # Вспомогательные функции
├── assets.py          # Менеджер ресурсов
├── images/            # Графика (фоны, спрайты)
├── music/             # Звуки и музыкальные треки
├── requirements.txt   # Зависимости
└── README.md          # Документация
```
