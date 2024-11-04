
# Bullet Tracker

Bullet Tracker is a program for visually marking and managing bullet states, created using Python and Tkinter.

## Features
- Visual marking of loaded and empty chambers.
- Toggle states of chambers using mouse clicks or keys 1-8 (or numpad keys).
- Movable separator to divide loaded and empty chambers. Use mouse or CTRL+ keys 1-8 (or numpad keys) to move the separator.
- Last Key Display: The last pressed key or combination is now shown in the bottom-right corner.
- Action History: The program remembers the last 8 changes in button states, which can be undone by pressing CTRL+Z while CTRL+SHIFT+Z redoes the last undone action.

## Installation
1. Make sure Python 3 is installed on your system.
2. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/bullet-tracker.git
   ```
3. Navigate to the project directory:
   ```bash
   cd bullet-tracker
   ```
4. Run the program:
   ```bash
   python bullet_tracker.py
   ```

## Building an Executable
To build a `.exe` file for Windows, you can use PyInstaller:
   ```bash
   pyinstaller --onefile --windowed bullet_tracker.py
   ```

## License
This project is licensed under the MIT License.


...................................................................................................

# Bullet Tracker

Bullet Tracker — это программа для визуальной отметки и управления зарядами, созданная с использованием Python и Tkinter.

## Функционал
- Визуальная отметка заряженных и пустых ячеек.
- Переключение состояния ячеек с помощью мыши и клавиш 1-8 или нумпад.
- Перемещение и фиксация перегородки для разделения зарядов. Перемещение перегородки возможно используя CTRL+ кнопки 1-8 (или кнопки нампада).
- Отображение последнего нажатия: В правом нижнем углу теперь отображается последняя нажатая клавиша или комбинация.
- История действий: программа запоминает до 8 последних изменений состояния кнопок, которые можно отменить нажатием CTRL+Z, в то время как CTRL+SHIFT+Z восстанавливает отменённое действие.

## Установка
1. Убедитесь, что у вас установлен Python 3.
2. Склонируйте репозиторий:
   ```bash
   git clone https://github.com/yourusername/bullet-tracker.git
   ```
3. Перейдите в папку проекта:
   ```bash
   cd bullet-tracker
   ```
4. Запустите программу:
   ```bash
   python bullet_tracker.py
   ```

## Сборка исполняемого файла
Если хотите собрать `.exe` файл для Windows, используйте PyInstaller:
   ```bash
   pyinstaller --onefile --windowed bullet_tracker.py
   ```

## Лицензия
Проект распространяется под лицензией MIT.
