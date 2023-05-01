from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import Button
import subprocess
import time

# Import audio
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


play_background_music(music_file="son/Générique.mp3")


def menugame():
    play_click(click_file)
    time.sleep(0.5)
    subprocess.Popen(["python3", "menu_game_graph.py"])
    root.destroy()


root = Tk()
root.geometry("1080x720")

# Load the background image
pikachu = "images/pika.jpeg"  # Replace with the path to your background image
bg_image = Image.open(pikachu).convert("RGBA")

# Load the logo image
pokemon_logo = "images/Pokémon_logo.png"  # Replace with the path to your logo image
logo_image = Image.open(pokemon_logo).convert("RGBA")
# Resize the logo image if needed
logo_image = logo_image.resize((700, 250), Image.LANCZOS)
# Paste the logo image onto the background image
bg_image.paste(logo_image, (200, 320), logo_image)

# Load and paste Sacha image
sacha = "images/sacha.png"  # Replace with the path to your Sacha image
logo_image2 = Image.open(sacha).convert("RGBA")
bg_image.paste(
    logo_image2, (750, 450), logo_image2
)  # Change these coordinates to move Sacha image

# Create a PhotoImage from the combined image
photo = ImageTk.PhotoImage(bg_image)

# Create a label with the combined image and place it on the window
image_label = Label(root, image=photo, borderwidth=0)
image_label.place(x=-20, y=-300)

# Bouton pour lancer le jeu
button = Button(
    root,
    text="Accéder au menu",
    borderwidth=0,
    width=15,
    height=3,
    font=("Arial", 16),
    command=menugame,
)
button.place(x=470, y=340)

root.mainloop()
