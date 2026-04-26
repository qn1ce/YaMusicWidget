# Yandex Music Widget

## English

A lightweight Windows desktop widget that displays currently playing track information from your system media player. The widget shows the track title, artist name, and provides media control buttons (previous, play/pause, next).

### Features
- **Real-time Track Display**: Shows current playing track title and artist
- **Media Controls**: Previous, Play/Pause, Next buttons
- **Animated Text Scrolling**: Long track names scroll smoothly
- **Compact Design**: Floating widget that stays on top
- **Toggle Visibility**: Hide/show widget with Alt+Shift+S
- **Draggable**: Move widget around the screen

### Requirements
⚠️ **Important**: This widget works **only when a media player is running** and actively playing music. The widget reads track information from the Windows Media Session API, so you need:
- Windows 10/11
- An active media player (Yandex Music)
- Python 3.8+
- Dependencies: tkinter, PIL, keyboard, screeninfo, winsdk

### Installation
```bash
pip install -r requirements.txt
```

### Usage
```bash
python main.py
```

**Keyboard Shortcut**: Press `Alt+Shift+S` to toggle widget visibility

---

## Русский

Лёгкий виджет для рабочего стола Windows, который отображает информацию о текущей композиции из системного медиаплеера. Виджет показывает название трека, имя исполнителя и предоставляет кнопки управления музыкой (предыдущий трек, воспроизведение/пауза, следующий трек).

### Возможности
- **Отображение в реальном времени**: Показывает название трека и исполнителя
- **Управление музыкой**: Кнопки предыдущий, воспроизведение/пауза, следующий
- **Анимированный скроллинг текста**: Длинные названия треков плавно прокручиваются
- **Компактный дизайн**: Плавающий виджет, всегда поверху
- **Переключение видимости**: Скрывать/показывать виджет через Alt+Shift+S
- **Перемещение**: Перетягивайте виджет по экрану

### Требования
⚠️ **Важно**: Этот виджет работает **только при включённом медиаплеере**. Виджет получает информацию через Windows Media Session API, поэтому вам нужны:
- Windows 10/11
- Активный медиаплеер (Яндекс.Музыка)
- Python 3.8+
- Зависимости: tkinter, PIL, keyboard, screeninfo, winsdk

### Установка
```bash
pip install -r requirements.txt
```

### Использование
```bash
python main.py
```

**Горячая клавиша**: Нажмите `Alt+Shift+S` для переключения видимости виджета

---

## License
MIT
