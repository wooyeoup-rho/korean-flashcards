# Korean Flashcard App
A flashcard app to learn Korean (probably).

Created as a part of [
100 Days of Code: The Complete Python Pro Bootcamp
](https://www.udemy.com/course/100-days-of-code/) by Angela Yu.

---
### Requirements
1. Python
2. PyInstaller (For creating the executable)

### Installation
Clone the repository:

```commandline
git clone https://github.com/wooyeoup-rho/korean-flashcards.git
```

### Running the application:
```commandline
cd korean-flashcards
python main.py
```

### Creating an executable
1. Install PyInstaller
```commandline
pip install pyinstaller
```
2. Create the executable:
```commandline
pyinstaller --onefile --add-data "assets;assets" --name flashcard --windowed --icon=assets/images/icon.ico main.py
```
- `--onefile` bundles everything into a single executable.
- `--add-data "assets;assets"` includes everything in the `assets` file into the executable.
- `--name flashcard` names the executable file.
- `--windowed` prevents a command-line window from appearing.
- `--icon=assets/images/icon.ico` specifies the application icon.
- `main.py` specifies the Python script to bundle.

3. Locate and run the executable:

The executable will be located in the `dist` folder. You can now open the `flashcard.exe` inside to open the application.
