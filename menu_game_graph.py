from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import Button
import subprocess
import time

import pygame.mixer

pygame.mixer.init()

click_file = "son/click2.mp3"


def play_click(click_file):
    pygame.mixer.music.load(click_file)
    pygame.mixer.music.play(-1)


# Musique
def play_background_music(music_file):
    pygame.mixer.music.load(music_file)
    pygame.mixer.music.play(-1)  # Play the music in an infinite loop


play_background_music(music_file="son/accueil.mp3")


def lancer_jeu():
    play_click(click_file)
    time.sleep(0.5)
    subprocess.Popen(["python3", "game_graph.py"])
    root1.destroy()


def ajouter_pokemon():
    play_click(click_file)
    time.sleep(0.5)
    subprocess.Popen(["python3", "ajouter_pokemon_graph.py"])
    root1.destroy()


def afficher_pokedex():
    play_click(click_file)
    time.sleep(0.5)
    subprocess.Popen(["python3", "afficher_pokedex_graph.py"])
    root1.destroy()


def accueil():
    play_click(click_file)
    time.sleep(0.5)
    subprocess.Popen(["python3", "accueil_graph.py"])
    root1.destroy()


root1 = Tk()
root1.geometry("1080x720")
root1.configure(bg="red")


wallpaper = "images/wallpaper.png"  # Replace with the path to your first image
image1 = Image.open(wallpaper).resize((1080, 720), Image.ANTIALIAS)
photo1 = ImageTk.PhotoImage(image1)

# Create a label with the first image and place it on the window
image_label1 = Label(root1, image=photo1)
image_label1.pack()


button1 = Button(
    root1,
    text="Lancer la partie",
    borderwidth=0,
    width=30,
    height=2,
    font=("Arial", 16),
    command=lancer_jeu,
)
button1.place(x=50, y=250)


button2 = Button(
    root1,
    text="Ajouter Pokémon",
    borderwidth=0,
    width=30,
    height=2,
    font=("Arial", 16),
    command=ajouter_pokemon,
)
button2.place(x=50, y=300)


button3 = Button(
    root1,
    text="Afficher Pokédex",
    borderwidth=0,
    width=30,
    height=2,
    font=("Arial", 16),
    command=afficher_pokedex,
)
button3.place(x=50, y=350)


button4 = Button(
    root1,
    text="Retour",
    borderwidth=0,
    width=30,
    height=2,
    font=("Arial", 16),
    command=accueil,
)
button4.place(x=50, y=400)


root1.mainloop()
