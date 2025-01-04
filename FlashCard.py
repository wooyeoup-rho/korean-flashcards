from tkinter import *
import pygame
import os, pyperclip, csv
from resources import resource_path, ENGLISH_FONT, KOREAN_FONT, BACKGROUND_COLOR, WHITE_COLOUR, BLACK_COLOUR
from gtts import gTTS
from io import BytesIO

class FlashCard:
    def __init__(self, window, word_list):
        self.window = window
        self.window.title("Korean Flashcards")
        self.window.geometry("808x428")

        self.words = word_list
        self.current_index = 0
        self.current_word = self.words[self.current_index]
        self.flipped = False
        self.saved_cards = False
        self.english_mode = False

        # Initialize audio
        pygame.mixer.init()

        # Canvas
        self.red_card = PhotoImage(file=resource_path("assets/images/red_card.png"))
        self.blue_card = PhotoImage(file=resource_path("assets/images/blue_card.png"))
        self.canvas = Canvas(window, width=808, height=428, bg=BACKGROUND_COLOR, highlightthickness=0)
        self.canvas.grid(row=1, column=0, columnspan=4)

        # Flashcard
        self.flashcard = self.canvas.create_image(0, 0, image=self.red_card, anchor="nw", tag="card")

        # Korean Word
        self.word_label = self.canvas.create_text(404, 214, text=self.words[self.current_index].korean, font=(KOREAN_FONT, 48, "bold"), fill=WHITE_COLOUR)
        pyperclip.copy(self.words[self.current_index].korean)

        # Romanized Word
        self.romanized_label = self.canvas.create_text(404, 314, text=self.words[self.current_index].romanized, font=(ENGLISH_FONT, 24), fill=WHITE_COLOUR, state=HIDDEN)

    def get_card(self, word=None):
        if word is None:
            self.current_word = self.words[self.current_index]
            self.canvas.itemconfigure(self.word_label, font=(KOREAN_FONT, 48, "bold"))
            self.canvas.itemconfigure(self.romanized_label, font=(ENGLISH_FONT, 24))
        else:
            self.current_word = word
            pyperclip.copy(self.current_word.korean)
            self.canvas.itemconfigure(self.word_label, font=(KOREAN_FONT, 24, "bold"))
            self.canvas.itemconfigure(self.romanized_label, font=(ENGLISH_FONT, 12))

        pyperclip.copy(self.current_word.korean)

        self.canvas.itemconfig(self.word_label, text=self.current_word.korean, fill=WHITE_COLOUR)
        self.canvas.itemconfig(self.romanized_label, text=self.current_word.romanized, state=HIDDEN)

        self.canvas.itemconfig(self.flashcard, image=self.red_card)
        self.flipped = FALSE

    def select_card(self, index):
        self.current_index = index
        self.get_card()

    def next_word(self, event=None):
        self.current_index = (self.current_index + 1) % len(self.words)
        self.get_card()

    def prev_word(self, event=None):
        self.current_index = (self.current_index - 1) % len(self.words)
        self.get_card()

    def dont_know_word(self):
        self.save_card()
        self.next_word()

    def play_audio(self):
        korean_audio = BytesIO()
        tts = gTTS(text=self.current_word.korean, lang='ko')
        tts.write_to_fp(korean_audio)
        korean_audio.seek(0)
        pygame.mixer.music.load(korean_audio)
        pygame.mixer.music.play()

    def toggle_romanized(self, event=None):
        current_state = self.canvas.itemcget(self.romanized_label, "state")
        new_state = HIDDEN if current_state == NORMAL else NORMAL
        self.canvas.itemconfig(self.romanized_label, state=new_state)
        self.canvas.update_idletasks()

    def flip_card(self, event=None):
        new_state = FALSE if self.flipped else TRUE
        self.flipped = new_state

        if self.flipped:
            self.canvas.itemconfig(self.flashcard, image=self.blue_card)
            self.canvas.itemconfig(self.word_label, text=self.current_word.english, fill=BLACK_COLOUR)
            self.canvas.itemconfig(self.romanized_label, text="")
        else:
            self.canvas.itemconfig(self.flashcard, image=self.red_card)
            self.canvas.itemconfig(self.word_label, text=self.current_word.korean, fill=WHITE_COLOUR)
            self.canvas.itemconfig(self.romanized_label, text=self.current_word.romanized)

    def save_card(self):
        word = self.words[self.current_index]
        new_data = {"ko_word": word.korean, "en_word": word.english, "romanized_word": word.romanized}
        headers = ["ko_word", "en_word", "romanized_word"]

        file_path = resource_path("assets/data/unknown_words.csv")

        if os.path.exists(file_path):
            # Checks duplicate
            with open(file_path, mode="r", newline="", encoding="utf-8") as csv_file:
                reader = csv.DictReader(csv_file)
                for row in reader:
                    if all(row[key] == str(value) for key, value in new_data.items()):
                        return

            # If no duplicate, appends
            with open(file_path, mode="a", newline="", encoding="utf-8") as csv_file:
                writer = csv.DictWriter(csv_file, fieldnames=headers)
                writer.writerow(new_data)
        else:
            self.saved_cards = True
            with open(file_path, mode="w", newline="", encoding="utf-8") as csv_file:
                writer = csv.DictWriter(csv_file, fieldnames = headers)
                writer.writeheader()
                writer.writerow(new_data)

    def change_mode(self):
        self.english_mode = not self.english_mode
