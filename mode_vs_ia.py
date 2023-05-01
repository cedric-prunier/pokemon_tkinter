import random
import json
import time
from tkinter import *
from PIL import Image, ImageTk
import subprocess
from tkinter import messagebox

import pygame.mixer

pygame.mixer.init()


# Background music
def play_background_music(music_file):
    pygame.mixer.music.load(music_file)
    pygame.mixer.music.play(-1)  # Play the music in an infinite loop


play_background_music(music_file="son/fight.mp3")

# Click sound
click_file = "son/click2.mp3"


def play_click(click_file):
    click_sound = pygame.mixer.Sound(click_file)
    click_sound.play()  # Play the click sound once


def begin():
    play_click(click_file)
    time.sleep(0.5)
    contre_ia()


def vs_mode():
    play_click(click_file)
    time.sleep(0.5)
    subprocess.Popen(["python3", "game_graph.py"])
    root2.destroy()


def stop_background_music():
    pygame.mixer.music.stop()


class Pokemon:
    def __init__(self, name, hp, attack, defense, type):
        self.name = name
        self.hp = hp
        self.attack = attack
        self.defense = defense
        self.type = type

    def attack_success(self):
        return random.choice([0, 1])

    def take_damage(self, damage):
        self.hp -= damage
        self.hp = max(self.hp, 0)

    def is_defeated(self):
        return self.hp == 0

    def calculate_type_multiplier(self, opponent_type):
        multiplier = 1
        if self.type == "Feu":
            if opponent_type == "Terre":
                multiplier = 2
            elif opponent_type == "Eau":
                multiplier = 0.5
            elif opponent_type == "Feu":
                multiplier = 1
            elif opponent_type == "Normal":
                multiplier = 1
        elif self.type == "Eau":
            if opponent_type == "Feu":
                multiplier = 2
            elif opponent_type == "Terre":
                multiplier = 0.5
            elif opponent_type == "Normal":
                multiplier = 1
            elif opponent_type == "Eau":
                multiplier = 1
        elif self.type == "Terre":
            if opponent_type == "Eau":
                multiplier = 2
            elif opponent_type == "Feu":
                multiplier = 0.5
            elif opponent_type == "Terre":
                multiplier = 1
            elif opponent_type == "Normal":
                multiplier = 1
        elif self.type == "Normal":
            if opponent_type == "Eau":
                multiplier = 0.75
            elif opponent_type == "Feu":
                multiplier = 0.75
            elif opponent_type == "Terre":
                multiplier = 0.75
            elif opponent_type == "Normal":
                multiplier = 1
        return multiplier


def create_pokemon_from_name(pokemon_name):
    with open("data.json", "r") as f:
        data = json.load(f)

    pokemon_data = data[pokemon_name]
    return Pokemon(
        pokemon_name,
        pokemon_data["points_de_vie"],
        pokemon_data["puissance_attaque"],
        pokemon_data["niveau_defense"],
        pokemon_data["type"],  # Add the 'type' attribute here
    )


def afficher_pokemons():
    with open("data.json", "r") as f:
        data = json.load(f)

    root = Toplevel()
    root.geometry("400x300")
    root.title("Sélectionnez un Pokémon")

    pokemon_listbox = Listbox(root, width=40)
    pokemon_listbox.pack(padx=20, pady=20)

    for nom in data.keys():
        pokemon_listbox.insert(END, nom)

    selected_pokemon = StringVar()

    def selectionner_pokemon():
        selection = pokemon_listbox.curselection()
        nom_pokemon = pokemon_listbox.get(selection)

        selected_pokemon.set(nom_pokemon)
        root.destroy()

    button_frame = Frame(root)
    button_frame.pack(side=BOTTOM, padx=20, pady=10, fill=X)

    selection_button = Button(
        button_frame, text="Sélectionner", command=selectionner_pokemon
    )
    selection_button.pack(side=RIGHT, padx=5)

    annuler_button = Button(button_frame, text="Annuler", command=root.destroy)
    annuler_button.pack(side=RIGHT, padx=5)

    root.wait_window(root)

    return selected_pokemon.get()


def choix_aleatoire_pokemon():
    with open("data.json", "r") as f:
        data = json.load(f)

    nom_pokemons = list(data.keys())
    pokemon_choisi = random.choice(nom_pokemons)

    return pokemon_choisi


def afficher_choix_ia(joueur_pokemon, ia_pokemon):
    def start_combat():
        lancer_combat(joueur_pokemon, ia_pokemon)
        root.destroy()

    root = Toplevel()
    root.geometry("300x150")
    root.title("Choix de l'IA")

    choix_label = Label(
        root,
        text="L'IA a choisi le Pokémon : {}".format(ia_pokemon),
        font=("Arial", 14),
    )
    choix_label.pack(pady=20)

    fermer_button = Button(root, text="OK", command=start_combat)
    fermer_button.pack(pady=10)


def lancer_combat(joueur_pokemon, ia_pokemon):
    combat_window = CombatWindow(joueur_pokemon, ia_pokemon)
    combat_window.wait_window()


def contre_ia():
    joueur_pokemon = afficher_pokemons()

    if joueur_pokemon:
        ia_pokemon = choix_aleatoire_pokemon()
        afficher_choix_ia(joueur_pokemon, ia_pokemon)
    else:
        print("Le jeu contre l'IA a été annulé.")


class CombatWindow(Toplevel):
    def __init__(self, player_pokemon, ia_pokemon):
        super().__init__()

        self.player_pokemon = player_pokemon
        self.ia_pokemon = ia_pokemon
        self.geometry("800x600")
        self.title("Combat Pokémon")

        # Define the user interface components and layout
        self.configure_ui()

    def configure_ui(self):
        # Load the image and create a PhotoImage object
        image_file = "images/pikachu2.png"
        image_obj = Image.open(image_file)
        photo_obj = ImageTk.PhotoImage(image_obj)

        # Create a label to display the image and add it to the CombatWindow
        image_label = Label(self, image=photo_obj)
        image_label.image = photo_obj  # Keep a reference to prevent garbage collection
        image_label.place(x=25, y=150, relwidth=1, relheight=1)

        self.player_label = Label(
            self, text=self.player_pokemon.name, font=("Arial", 25)
        )
        self.player_label.pack(side=LEFT, padx=20)

        self.player_hp_label = Label(
            self, text="Points de vie: {}".format(self.player_pokemon.hp)
        )
        self.player_hp_label.place(x=20, y=350)

        self.ia_label = Label(self, text=self.ia_pokemon.name, font=("Arial", 25))
        self.ia_label.pack(side=RIGHT, padx=20)

        self.ia_hp_label = Label(
            self, text="Point de vie: {}".format(self.ia_pokemon.hp)
        )
        self.ia_hp_label.place(x=670, y=350)

        self.attack_button = Button(
            self,
            text="Joueur 1 \nAttaquer",
            command=self.player_attack,
            width=10,
            height=10,
        )
        self.attack_button.place(x=20, y=400)

    def player_attack(self):
        attack_success = random.choice([0, 1])
        if attack_success:
            damage = self.calculate_damage(self.player_pokemon, self.ia_pokemon)
            self.ia_pokemon.take_damage(damage)
            self.ia_hp_label.config(
                text="Points de vie : {}".format(self.ia_pokemon.hp)
            )
            message_label = Label(
                self,
                text="L'attaque de {} inflige -{} points de vie de dégâts".format(
                    self.player_pokemon.name, damage
                ),
            )
            message_label.pack()
            if self.ia_pokemon.hp <= 0:
                message_label = Label(
                    self,
                    text="{} a gagné !".format(self.player_pokemon.name),
                    fg="green",
                )
                message_label.pack()
                self.attack_button.config(state=DISABLED)
                return
        else:
            message_label = Label(
                self,
                text="L'attaque de {} a échouée !".format(self.player_pokemon.name),
            )
            message_label.pack()

        self.attack_button.config(state=DISABLED)
        self.after(2000, self.ia_attack)

    def ia_attack(self):
        attack_success = random.choice([0, 1])
        if attack_success:
            damage = self.calculate_damage(self.ia_pokemon, self.player_pokemon)
            self.player_pokemon.take_damage(damage)
            self.player_hp_label.config(
                text="Points de vie : {}".format(self.player_pokemon.hp)
            )
            message_label = Label(
                self,
                text="L'attaque de {} inflige -{} points de vie de dégâts".format(
                    self.ia_pokemon.name, damage
                ),
            )
            message_label.pack()
            if self.player_pokemon.hp <= 0:
                message_label = Label(
                    self, text="{} a gagné !".format(self.ia_pokemon.name), fg="red"
                )
                message_label.pack()
                self.attack_button.config(state=DISABLED)
                return
        else:
            message_label = Label(
                self,
                text="L'attaque de {} a échouée !".format(self.ia_pokemon.name),
            )
            message_label.pack()

        self.attack_button.config(state=NORMAL)

    def calculate_damage(self, attacker, defender):
        # Calculate base damage
        damage = attacker.attack - defender.defense
        damage = max(damage, 0)

        # Apply type multiplier
        type_multiplier = attacker.calculate_type_multiplier(defender.type)
        damage *= type_multiplier

        return int(damage)


def lancer_combat(joueur_pokemon, ia_pokemon):
    player_pokemon = create_pokemon_from_name(joueur_pokemon)
    ia_pokemon = create_pokemon_from_name(ia_pokemon)

    combat_window = CombatWindow(player_pokemon, ia_pokemon)
    root2.wait_window(combat_window)


# Main window
root2 = Tk()
root2.title("Fight")
root2.geometry("1080x720")
root2.configure(bg="white")

image = Image.open("images/Pokémon-wallpapers.jpeg")
image_resized = image.resize((1080, 720))
image_resized.save("images/Pokémon-wallpaper.png")

wallpaper = "images/Pokémon-wallpaper.png"
image2 = Image.open(wallpaper).convert("RGBA")
photo2 = ImageTk.PhotoImage(image2)

image_label2 = Label(root2, image=photo2)
image_label2.pack()

button = Button(
    root2,
    text="Commencer le combat",
    borderwidth=0,
    width=30,
    height=2,
    command=begin,
)
button.place(x=50, y=100)

button_quit = Button(
    root2,
    text="Retour",
    borderwidth=0,
    width=30,
    height=2,
    command=vs_mode,
)
button_quit.place(x=50, y=150)

button_quit = Button(
    root2,
    text="Quitter",
    borderwidth=0,
    width=30,
    height=2,
    command=quit,
)
button_quit.place(x=50, y=200)

root2.mainloop()
