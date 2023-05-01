from tkinter import *
from PIL import Image, ImageTk
import subprocess
import tkinter as tk
from tkinter import ttk
import json
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
    root4.destroy()


def afficher_pokedex(pokedex):
    arbre = ttk.Treeview(
        root4,
        columns=("Nom", "Type", "Niveau", "Attaque", "Défense", "PV"),
        show="headings",
        height=30,
    )
    arbre.column("Nom", width=90)
    arbre.column("Type", width=80)
    arbre.column("Niveau", width=60)
    arbre.column("Attaque", width=60)
    arbre.column("Défense", width=60)
    arbre.column("PV", width=60)

    # Utilisez la méthode 'place()' pour définir la position de l'arbre
    arbre.place(x=555, y=120)

    for pokemon in pokedex:
        arbre.insert(
            "",
            tk.END,
            values=(
                pokemon["name"],
                pokemon["type"],
                pokemon["niveau"],
                pokemon["attaque"],
                pokemon["defense"],
                pokemon["pv"],
            ),
        )


def charger_pokedex():
    with open("data.json", "r", encoding="utf-8") as fichier:
        donnees = json.load(fichier)

    pokedex = []
    for nom, info in donnees.items():
        pokedex.append(
            {
                "name": nom,
                "type": info["type"],
                "niveau": info["niveau"],
                "attaque": info["puissance_attaque"],
                "defense": info["niveau_defense"],
                "pv": info["points_de_vie"],
            }
        )
    return pokedex


# Créer une fenêtre Tkinter
root4 = Tk()
root4.geometry("1080x760")

# Charger les images
image1 = Image.open("images/pokedex.png")
# Créer des objets PhotoImage
photo1 = ImageTk.PhotoImage(image1)
# Créer des labels pour les images
label1 = Label(root4, image=photo1)
label1.place(x=0, y=0)

# Replace with the path to your first image
image2 = Image.open("images/Pokédex_logo.png").convert("RGBA")
photo2 = ImageTk.PhotoImage(image2)

# Create a label with the first image and place it on the window
image_label2 = Label(root4, image=photo2, bg="white", borderwidth=0)
image_label2.place(x=70, y=200)

# Bouton retour au menu
button_retour = Button(
    root4,
    width=25,
    height=4,
    text="Revenir au menu",
    font=("Arial", 25),
    command=menugame,
)
button_retour.place(x=67, y=590)

pokedex = charger_pokedex()

# Bouton afficher pokedex liste pokémons
bouton = Button(
    root4,
    text="Liste des pokémons",
    width=42,
    height=2,
    command=afficher_pokedex(pokedex),
)
bouton.place(x=554, y=100)

root4.mainloop()
