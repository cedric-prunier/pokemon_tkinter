import random
import json
from tkinter import *
from PIL import Image, ImageTk
import subprocess
import time
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
    contre_joueur()


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


def afficher_choix_joueur(joueur_pokemon, joueur2_pokemon):
    def start_combat():
        lancer_combat(joueur_pokemon, joueur2_pokemon)
        root.destroy()

    root = Toplevel()
    root.geometry("400x200")
    root.title("Choix du second joueur")

    choix_label = Label(
        root,
        text="Le premier joueur a choisi le Pokémon : {} \n Le second joueur a choisi le Pokémon : {}".format(
            joueur_pokemon, joueur2_pokemon
        ),
        font=("Arial", 15),
    )
    choix_label.pack(pady=20)

    fermer_button = Button(root, text="OK", command=start_combat)
    fermer_button.pack(pady=10)


def lancer_combat(joueur_pokemon, joueur2_pokemon):
    combat_window = CombatWindow(joueur_pokemon, joueur2_pokemon)
    combat_window.wait_window()


def contre_joueur():
    joueur1_pokemon = afficher_pokemons()

    if joueur1_pokemon:
        joueur2_pokemon = afficher_pokemons()
        if joueur2_pokemon:
            afficher_choix_joueur(joueur1_pokemon, joueur2_pokemon)
        else:
            print("Le combat entre deux joueurs a été annulé.")
    else:
        print("Le combat entre deux joueurs a été annulé.")


class CombatWindow(Toplevel):
    def __init__(self, player1_pokemon, player2_pokemon):
        super().__init__()

        self.player1_pokemon = player1_pokemon
        self.player2_pokemon = player2_pokemon
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

        self.player1_label = Label(
            self, text=self.player1_pokemon.name, font=("Arial", 25)
        )
        self.player1_label.pack(side=LEFT, padx=40)

        self.player1_hp_label = Label(
            self,
            text="Points de vie: {}".format(self.player1_pokemon.hp),
            font=("Arial", 15),
        )
        self.player1_hp_label.place(x=40, y=350)

        self.player2_label = Label(
            self, text=self.player2_pokemon.name, font=("Arial", 25)
        )
        self.player2_label.pack(side=RIGHT, padx=40)

        self.player2_hp_label = Label(
            self,
            text="Points de vie: {}".format(self.player2_pokemon.hp),
            font=("Arial", 15),
        )
        self.player2_hp_label.place(x=635, y=350)

        self.attack_button = Button(
            self, text="Attaque Joueur 1", command=self.player1_attack
        )
        self.attack_button.place(x=30, y=400)

        self.attack_button2 = Button(
            self, text="Attaque Joueur 2", command=self.player2_attack
        )
        self.attack_button2.place(x=630, y=400)

    def player1_attack(self):
        attack_success = random.choice([0, 1])
        if attack_success:
            damage = self.calculate_damage(self.player1_pokemon, self.player2_pokemon)
            self.player2_pokemon.take_damage(damage)
            self.player2_hp_label.config(
                text="Points de vie: {}".format(self.player2_pokemon.hp)
            )
            message_label = Label(
                self,
                text="L'attaque de {} inflige -{} points de vie de dégâts".format(
                    self.player1_pokemon.name, damage
                ),
            )
            message_label.pack()
            if self.player2_pokemon.hp <= 0:
                message_label = Label(
                    self,
                    text="{} a gagné !".format(self.player1_pokemon.name),
                    fg="green",
                )
                message_label.pack()
                self.attack_button.config(state=DISABLED)
                self.attack_button2.config(state=DISABLED)
                return
        else:
            message_label = Label(
                self,
                text="L'attaque de {} a échouée !".format(self.player1_pokemon.name),
            )
            message_label.pack()

        self.attack_button.config(state=DISABLED)
        self.attack_button2.config(state=NORMAL)

    def player2_attack(self):
        attack_success = random.choice([0, 1])
        if attack_success:
            damage = self.calculate_damage(self.player2_pokemon, self.player1_pokemon)
            self.player1_pokemon.take_damage(damage)
            self.player1_hp_label.config(
                text="Points de vie : {}".format(self.player1_pokemon.hp)
            )

            message_label = Label(
                self,
                text="L'attaque de {} inflige -{} points de vie de dégâts".format(
                    self.player2_pokemon.name, damage
                ),
            )
            message_label.pack()

            if self.player1_pokemon.hp <= 0:
                message_label = Label(
                    self,
                    text="{} a gagné !".format(self.player2_pokemon.name),
                    fg="green",
                )
                message_label.pack()
                self.attack_button.config(state=DISABLED)
                self.attack_button2.config(state=DISABLED)
                return
        else:
            message_label = Label(
                self,
                text="L'attaque de {} a échouée !".format(self.player2_pokemon.name),
            )
            message_label.pack()

        self.attack_button.config(state=NORMAL)
        self.attack_button2.config(state=DISABLED)

    def calculate_damage(self, attacker, defender):
        # Calculate base damage
        damage = attacker.attack - defender.defense
        damage = max(damage, 0)

        # Apply type multiplier
        type_multiplier = attacker.calculate_type_multiplier(defender.type)
        damage *= type_multiplier

        return int(damage)


def lancer_combat(joueur_pokemon, adversaire_pokemon):
    player_pokemon = create_pokemon_from_name(joueur_pokemon)
    opponent_pokemon = create_pokemon_from_name(adversaire_pokemon)

    combat_window = CombatWindow(player_pokemon, opponent_pokemon)
    combat_window.wait_window()


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
