from gtts import gTTS
import os
import random
import requests
import tkinter as tk
from tkinter import messagebox
import json

# File to store favorite words
FAVORITES_FILE = os.path.join(os.path.dirname(__file__), "favorites.json")
# Initialize global variable
example_sentence = ""

# Function to fetch word details from API
def fetch_word_details(word):
    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data:
            meanings = data[0].get('meanings', [])
            result_text = f"Word: {word}\n"
            global example_sentence
            example_sentence = ""  # Reset previous sentence
            for meaning in meanings:
                result_text += f"\n{meaning['partOfSpeech'].capitalize()}:\n"
                for definition in meaning.get('definitions', []):
                    result_text += f"\n- {definition['definition']}\n"
                    if 'synonyms' in definition and definition['synonyms']:
                        result_text += f"  Synonyms: {', '.join(definition['synonyms'])}\n"
                    if 'antonyms' in definition and definition['antonyms']:
                        result_text += f"  Antonyms: {', '.join(definition['antonyms'])}\n"
                    if 'example' in definition:
                        example_sentence = definition['example']  # Store example sentence
            if example_sentence:
                result_text += f"\nExample: {example_sentence}"
            output_label.config(text=result_text)
        else:
            output_label.config(text="Word not found! Please try another word.")
    else:
        output_label.config(text="Word not found! Please try another word.")

# Function to get a random word of the day
def get_word_of_the_day():
    word_list = ["serendipity", "quixotic", "ephemeral", "eloquent", "melancholy",
                 "nefarious", "ineffable", "sonder"]
    word_of_the_day = random.choice(word_list)
    fetch_word_details(word_of_the_day)

# Function to save a word as favorite
def save_favorite_word():
    word = entry.get().strip()
    if not word:
        messagebox.showwarning("Warning", "Please enter a word first!")
        return
    favorites = load_favorites()
    if word not in favorites:
        favorites.append(word)
        save_favorites(favorites)
        messagebox.showinfo("Success", f"'{word}' added to favorites!")
    else:
        messagebox.showinfo("Info", f"'{word}' is already in favorites.")

# Function to load saved favorite words
def load_favorites():
    if os.path.exists(FAVORITES_FILE):
        with open(FAVORITES_FILE, "r") as file:
            return json.load(file)
    return []

# Function to save favorites to file
def save_favorites(favorites):
    with open(FAVORITES_FILE, "w") as file:
        json.dump(favorites, file)

# Function to show saved favorite words
def show_favorites():
    favorites = load_favorites()
    if favorites:
        messagebox.showinfo("Favorite Words", "\n".join(favorites))
    else:
        messagebox.showinfo("Favorite Words", "No favorite words saved yet.")

# Function to pronounce the word
def pronounce_word():
    word = entry.get().strip()
    if word:
        tts = gTTS(text=word, lang='en')
        tts.save("word.mp3")
        os.system("afplay word.mp3")  # For macOS
        os.remove("word.mp3")
    else:
        messagebox.showwarning("Warning", "Please enter a word first!")

# Function to pronounce the example sentence
def pronounce_sentence():
    global example_sentence
    if example_sentence:
        tts = gTTS(text=example_sentence, lang='en')
        tts.save("sentence.mp3")
        os.system("afplay sentence.mp3")  # For macOS
        os.remove("sentence.mp3")
    else:
        messagebox.showwarning("Warning", "No example sentence available for this word.")

# GUI Setup
root = tk.Tk()
root.title("Dictionary App with Pronunciation & Example Sentences")
root.geometry("500x650")

# Input Field
tk.Label(root, text="Enter a word:", font=("Arial", 12)).pack(pady=5)
entry = tk.Entry(root, font=("Arial", 12))
entry.pack(pady=5)

# Buttons
search_button = tk.Button(root, text="Search", font=("Arial", 12), command=lambda: fetch_word_details(entry.get().strip()))
search_button.pack(pady=5)
word_day_button = tk.Button(root, text="Word of the Day", font=("Arial", 12), command=get_word_of_the_day)
word_day_button.pack(pady=5)
save_button = tk.Button(root, text="Save to Favorites", font=("Arial", 12), command=save_favorite_word)
save_button.pack(pady=5)
show_favorites_button = tk.Button(root, text="Show Favorite Words", font=("Arial", 12), command=show_favorites)
show_favorites_button.pack(pady=5)
pronounce_button = tk.Button(root, text="Pronounce Word", font=("Arial", 12), command=pronounce_word)
pronounce_button.pack(pady=5)
pronounce_sentence_button = tk.Button(root, text="Pronounce Example", font=("Arial", 12), command=pronounce_sentence)
pronounce_sentence_button.pack(pady=5)

# Output Label
output_label = tk.Label(root, text="", font=("Arial", 10), justify="left", wraplength=450)
output_label.pack(pady=10)

# Run the GUI
root.mainloop()
