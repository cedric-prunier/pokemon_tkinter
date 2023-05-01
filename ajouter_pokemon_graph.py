import json
from tkinter import *
import subprocess
from PIL import Image, ImageTk
import time

# Import audio
import pygame.mixer

pygame.mixer.init()


# Musique
def play_background_music(music_file):
    pygame.mixer.music.load(music_file)
    pygame.mixer.music.play(-1)  # Play the music in an infinite loop


play_background_music(music_file="son/Pokédex.mp3")

# Click sound
click_file = "son/click2.mp3"


def play_click(click_file):
    click_sound = pygame.mixer.Sound(click_file)
    click_sound.play()  # Play the click sound once


def menugame():
    play_click(click_file)
    time.sleep(0.5)
    subprocess.Popen(["python3", "menu_game_graph.py"])
    root3.destroy()


def click():
    play_click(click_file)
    time.sleep(0.5)
    save_data()


def save_data():
    # Charger les données existantes à partir du fichier JSON
    try:
        with open("data.json", "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        data = {}

    # Ajouter les nouvelles données
    pokemon_data = {
        "nom": nom_entry.get(),
        "type": type_entry.get(),
        "niveau": int(niveau_entry.get()),
        "puissance_attaque": int(puissance_attaque_entry.get()),
        "niveau_defense": int(niveau_defense_entry.get()),
        "points_de_vie": int(points_de_vie_entry.get()),
    }
    data[nom_entry.get()] = pokemon_data

    # Enregistrer les données dans le fichier JSON
    with open("data.json", "w") as f:
        json.dump(data, f, indent=1)

    # Effacer les données des Entry
    nom_entry.delete(0, END)
    type_entry.delete(0, END)
    niveau_entry.delete(0, END)
    puissance_attaque_entry.delete(0, END)
    niveau_defense_entry.delete(0, END)
    points_de_vie_entry.delete(0, END)


# Créer une fenêtre Tkinter
root3 = Tk()
root3.geometry("1080x800")

# Charger les images
image1 = Image.open("images/pokedex.png")
# Créer des objets PhotoImage
photo1 = ImageTk.PhotoImage(image1)
# Créer des labels pour les images
label1 = Label(root3, image=photo1)
label1.place(x=0, y=0)


# Créer des widgets pour collecter les données
nom_label = Label(root3, text="Nom du Pokémon:", width=30, height=3)
nom_label.place(x=570, y=130)
nom_entry = Entry(root3, width=25)
nom_entry.place(x=570, y=170)

type_label = Label(
    root3, text="Type (Normal, Eau, Feu, Terre, Electrique):", width=30, height=3
)
type_label.place(x=570, y=230)
type_entry = Entry(root3, width=25)
type_entry.place(x=570, y=270)

niveau_label = Label(root3, text="Niveau:", width=30, height=3)
niveau_label.place(x=570, y=330)
niveau_entry = Entry(root3, width=25)
niveau_entry.place(x=570, y=370)

puissance_attaque_label = Label(root3, text="Puissance d'attaque:", width=30, height=3)
puissance_attaque_label.place(x=570, y=430)
puissance_attaque_entry = Entry(root3, width=25)
puissance_attaque_entry.place(x=570, y=470)

niveau_defense_label = Label(root3, text="Niveau de défense:", width=30, height=3)
niveau_defense_label.place(x=570, y=530)
niveau_defense_entry = Entry(root3, width=25)
niveau_defense_entry.place(x=570, y=570)

points_de_vie_label = Label(root3, text="Points de vie:", width=30, height=3)
points_de_vie_label.place(x=570, y=630)
points_de_vie_entry = Entry(root3, width=25)
points_de_vie_entry.place(x=570, y=670)

# Bouton pour enregistrer les données
save_button = Button(
    root3,
    width=17,
    height=8,
    text="Enregistrer \n ce nouveau pokémon \n Cliquez ici",
    font=("Arial", 35),
    command=click,
)
save_button.place(x=75, y=110)

button_retour = Button(
    root3,
    width=25,
    height=4,
    text="Revenir au menu",
    font=("Arial", 25),
    command=menugame,
)
button_retour.place(x=67, y=590)


root3.mainloop()
