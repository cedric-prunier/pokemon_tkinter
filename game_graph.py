from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
import subprocess
import time

import pygame.mixer

pygame.mixer.init()


# Background music
def play_background_music(music_file):
    pygame.mixer.music.load(music_file)
    pygame.mixer.music.play(-1)  # Play the music in an infinite loop


play_background_music(music_file="son/accueil.mp3")

# Click sound
click_file = "son/click2.mp3"


def play_click(click_file):
    click_sound = pygame.mixer.Sound(click_file)
    click_sound.play()  # Play the click sound once


def stop_background_music():
    pygame.mixer.music.stop()


def menugame():
    play_click(click_file)
    time.sleep(0.5)
    subprocess.Popen(["python3", "menu_game_graph.py"])
    root2.destroy()


def deux_joueurs():
    play_click(click_file)
    time.sleep(0.5)
    subprocess.Popen(["python3", "mode_2joueurs.py"])
    root2.destroy()


def mode_vs_ia():
    play_click(click_file)
    time.sleep(0.5)
    subprocess.Popen(["python3", "mode_vs_ia.py"])
    root2.destroy()


root2 = Tk()
root2.geometry("1080x720")


# Ouvrir l'image
image = Image.open("images/Pokémon-wallpapers.jpeg")
image_resized = image.resize((1080, 720))
image_resized.save("images/Pokémon-wallpaper.png")

wallpaper = "images/Pokémon-wallpaper.png"  # Replace with the path to your first image
image1 = Image.open(wallpaper).convert("RGBA")
photo1 = ImageTk.PhotoImage(image1)

# Create a label with the first image and place it on the window
image_label1 = Label(root2, image=photo1)
image_label1.pack()

# Boutons modes de jeu
deux_joueurs_button = Button(
    root2,
    text="Mode 2 joueurs",
    border=0,
    width=30,
    height=2,
    command=deux_joueurs,
)
deux_joueurs_button.place(x=100, y=50)

contre_ia_button = Button(
    root2,
    text="Mode contre l'IA",
    border=0,
    width=30,
    height=2,
    command=mode_vs_ia,
)
contre_ia_button.place(x=100, y=100)

# Bouton retour au menu
button_retour = Button(
    root2,
    width=30,
    height=2,
    text="Revenir au menu",
    borderwidth=0,
    command=menugame,
)
button_retour.place(x=100, y=150)

root2.mainloop()
