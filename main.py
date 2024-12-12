from tkinter import *
from tkinter import messagebox, filedialog
from CardButton import CardButton
import csv, random, os, shutil
from resources import resource_path, BACKGROUND_COLOR, KOREAN_FONT, BLUE_COLOUR
from Word import Word
from FlashCard import FlashCard

# ---------------------------- FUNCTIONS ------------------------------- #
def load_words_from_csv(file_path):
    word_list = []
    with open(file_path, newline="", encoding="utf-8") as data_file:
        reader = csv.reader(data_file)
        next(reader, None)

        for row in reader:
            korean, english, romanized = row
            word_list.append(Word(korean, english, romanized))
    return word_list

def shuffle_words(event=None):
    confirm_shuffle = messagebox.askyesno("Shuffle words", "Do you wish to shuffle the list of words?")

    if confirm_shuffle:
        random.shuffle(words)
        flashcard.current_index = 0
        flashcard.get_card()
        populate_list()

def populate_list():
    word_listbox.delete(0, END)
    for word in words:
        word_listbox.insert(END, word.korean)

def select_word(event):
    selected_index = word_listbox.curselection()
    flashcard.select_card(selected_index[0])

def load_words():
    global words
    confirm_load = messagebox.askyesno("Load words", "Do you wish to load your previously unknown words?")

    if confirm_load:
        file_path = filedialog.askopenfilename(
            title="Select CSV file",
            filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")]
        )

        if not file_path:
            messagebox.showinfo("No File Selected", "No file selected.")
            return

        try:
            words = load_words_from_csv(file_path)
            flashcard.words = words
            flashcard.current_index = 0
            flashcard.get_card()
            populate_list()

        except FileNotFoundError:
            messagebox.showerror("File not found", f"The file {file_path} could not be found.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while loading the file:\n{str(e)}")

def reset():
    confirm_reset = messagebox.askyesno("Reset words", "Do you wish to reset the word list to default?")

    if confirm_reset:
        global words
        words = load_words_from_csv(resource_path("assets/data/data.csv"))
        flashcard.words = words
        flashcard.current_index = 0
        flashcard.get_card()
        populate_list()

def save_list(file_path):
    temp_file_path = resource_path("assets/data/unknown_words.csv")

    if not os.path.exists(temp_file_path):
        messagebox.showerror("Error", "No data to save. The temporary file does not exist.")
        return

    try:
        shutil.copy(temp_file_path, file_path)
        messagebox.showinfo("Success", f"File saved successfully at {file_path}")
    except Exception as e:
        messagebox.showerror("Error", f"Could not save file: {str(e)}")

def on_close():
    if flashcard.saved_cards:
        window.withdraw()
        should_save = messagebox.askyesno("Save?", "Save unknown words?")
        if should_save:
            directory = filedialog.asksaveasfilename(
                title="Save File",
                defaultextension=".csv",
                filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")]
            )
            save_list(directory)

    window.destroy()

# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Korean Flashcards")
window.config(padx=100, pady=0, bg=BACKGROUND_COLOR)
window.minsize(1150, 800)
window.resizable(False, False)
window.rowconfigure(0, pad=100)
window.rowconfigure(2, pad=50)

icon_photo = PhotoImage(file=resource_path("assets/images/icon.png"))
window.iconphoto(False, icon_photo)

words = load_words_from_csv(resource_path("assets/data/data.csv"))
flashcard = FlashCard(window, words)

# BUTTONS
romanize_button = CardButton(
    window,
    "assets/images/buttons/translate_button.png",
    "assets/images/buttons/translate_button_active.png",
    flashcard.toggle_romanized
)
romanize_button.grid(row=0, column=0)

audio_button = CardButton(
    window,
    "assets/images/buttons/audio_button.png",
    "assets/images/buttons/audio_button_active.png",
    flashcard.play_audio
)
audio_button.grid(row=0, column=1)

flip_button = CardButton(
    window,
    "assets/images/buttons/flip_button.png",
    "assets/images/buttons/flip_button_active.png",
    flashcard.flip_card
)
flip_button.grid(row=0, column=2)

shuffle_button = CardButton(
    window,
    "assets/images/buttons/mix_button.png",
    "assets/images/buttons/mix_button_active.png",
    shuffle_words
)
shuffle_button.grid(row=0, column=3)

load_button = CardButton(
    window,
    "assets/images/buttons/load_button.png",
    "assets/images/buttons/load_button_active.png",
    load_words
)
load_button.grid(row=0, column=4)

dunno_button = CardButton(
    window,
    "assets/images/buttons/dunno_button.png",
    "assets/images/buttons/dunno_button_active.png",
    flashcard.dont_know_word
)
dunno_button.grid(row=2, column=1)

know_button = CardButton(
    window,
    "assets/images/buttons/know_button.png",
    "assets/images/buttons/know_button_active.png",
    flashcard.next_word
)
know_button.grid(row=2, column=2)

left_button = CardButton(
    window,
    "assets/images/buttons/left_button.png",
    "assets/images/buttons/left_button_active.png",
    flashcard.prev_word
)
left_button.grid(row=2, column=0)

right_button = CardButton(
    window,
    "assets/images/buttons/right_button.png",
    "assets/images/buttons/right_button_active.png",
    flashcard.next_word
)
right_button.grid(row=2, column=3)

reset_button = CardButton(
    window,
    "assets/images/buttons/reset_button.png",
    "assets/images/buttons/reset_button_active.png",
    reset
)
reset_button.grid(row=2, column=4)

frame = Frame(window)
frame.grid(row=1, column=4, rowspan=2, sticky="nw", padx=(50,0), pady=(10,0))

word_listbox = Listbox(frame, selectmode = SINGLE, height=20, width=10, font=(KOREAN_FONT, 12, "bold"), relief="solid", borderwidth=10, selectbackground=BLUE_COLOUR)
word_listbox.grid(row=0, column=4)

scrollbar = Scrollbar(frame, orient=VERTICAL, command=word_listbox.yview)
scrollbar.grid(row=0, column=5, sticky="ns", rowspan=3)

word_listbox.config(yscrollcommand = scrollbar.set)

populate_list()
word_listbox.bind("<<ListboxSelect>>", select_word)

window.protocol("WM_DELETE_WINDOW", on_close)
window.mainloop()
