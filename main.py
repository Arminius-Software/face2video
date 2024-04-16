import tkinter as tk
from tkinter import PhotoImage
from PIL import Image, ImageTk
import os
import random
from settings import *


"""

todo:
make random if 5 real 4 fake or 5 real 4 fake
add button to game over screen that opens matplotlib plot with images and shows if true/false 2x2 plot
find images for real images

"""

class GUIApp():

    def __init__(self, root):

        self.root = root
        self.score = 0
        self.image_paths = []
        self.modus = ""
        self.init_screen()

    def init_screen(self):

        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.title("Echt oder KI?")
        self.root.geometry("550x400") 
        self.root.configure(bg=dark_background_color)

        header_label = tk.Label(self.root, text="Echt oder KI?", font=("Helvetica", 20, "bold"), fg=text_color, bg=dark_background_color)
        header_label.pack(pady=20)

        select_humans_button = tk.Button(self.root, text="Menschen", command=lambda: self.start_game("Menschen"), font=("Helvetica", 12), width=30, height=2, bg=dark_background_color, fg=text_color)
        select_humans_button.pack(pady=10)

        select_animals_button = tk.Button(self.root, text="Tiere", command=lambda: self.start_game("Tiere"), font=("Helvetica", 12), width=30, height=2, bg=dark_background_color, fg=text_color)
        select_animals_button.pack(pady=10)

        select_landscapes_button = tk.Button(self.root, text="Landschaften", command=lambda: self.start_game("Landscapes"), font=("Helvetica", 12), width=30, height=2, bg=dark_background_color, fg=text_color)
        select_landscapes_button.pack(pady=10)

    def get_images(self, modus):

        # choose path

        if modus == "Menschen":
            path = "Humans/"
        elif modus == "Tiere":
            path = "Animals/"
        else:
            path = "Landscapes/"

        # choose if 4 real and 5 fake or 5 real and 4 fake at random

        more_images = random.choice(["real", "fake"])

        # get fakes

        image_paths = []

        path_to_fake = os.path.join(path, "fake/")

        path_to_fake = os.path.join(os.getcwd(), path_to_fake)
        images_in_folder = []
        for f in os.listdir(path_to_fake): 
            if os.path.isfile(os.path.join(path_to_fake, f)):
                images_in_folder.append((False, os.path.join(path_to_fake, f)))

        if more_images == "fake":
            image_paths.extend(random.sample(images_in_folder, 5))
        else:
            image_paths.extend(random.sample(images_in_folder, 4))

        # get real images

        path_to_real = os.path.join(path, "real/")

        path_to_real = os.path.join(os.getcwd(), path_to_real)
        images_in_folder = []
        for f in os.listdir(path_to_real): 
            if os.path.isfile(os.path.join(path_to_real, f)):
                images_in_folder.append((True, os.path.join(path_to_real, f)))

        if more_images == "real":
            image_paths.extend(random.sample(images_in_folder, 5))
        else:
            image_paths.extend(random.sample(images_in_folder, 4))

        random.shuffle(image_paths)

        self.image_paths = image_paths

    def start_game(self, modus):

        if modus == "Menschen":
            self.get_images("Menschen")
            self.modus = "Menschen"
        elif modus == "Tiere":
            self.get_images("Tiere")
            self.modus = "Tiere"
        else:
            self.get_images("Landschaften")
            self.modus = "Landschaften"

        self.game_screen()

    def button_real(self, fake_or_real):

        if fake_or_real:
            self.score += 1

        self.game_button_pressed()

    def button_fake(self, fake_or_real):

        if not fake_or_real:
            self.score += 1

        self.game_button_pressed()

    def game_button_pressed(self):
        
        self.image_paths = self.image_paths[1:]

        if len(self.image_paths) == 0:
            self.game_over_screen()
        else:
            self.game_screen()

    def game_screen(self):

        # Clear the initial screen widgets
        for widget in self.root.winfo_children():
            widget.destroy()

        # Update the main window for the game
        self.root.title("Ratespiel")
        self.root.geometry("800x700")

        label = tk.Label(self.root, text=f"{self.modus}: Echt oder KI?", font=("Helvetica", 16, "bold"), fg=text_color, bg=dark_background_color)
        label.pack(pady=20)

        # Load and display image
        path_to_image = self.image_paths[0][1]
        pil_image = Image.open(path_to_image)
        resized_image = pil_image.resize((512, 512), Image.Resampling.LANCZOS)
        image = ImageTk.PhotoImage(resized_image)
        image_label = tk.Label(self.root, image=image, bg=dark_background_color)
        image_label.image = image  # Keep a reference!
        image_label.pack(pady=20)

        # Create buttons
        button_frame = tk.Frame(self.root, bg=dark_background_color)
        button_frame.pack(pady=10)

        fake_or_real = self.image_paths[0][0]

        btn1 = tk.Button(button_frame, text="Echt", command=lambda: instance.button_real(fake_or_real), font=("Helvetica", 12), width=30, height=2, bg=dark_background_color, fg=text_color)
        btn2 = tk.Button(button_frame, text="Fake", command=lambda: instance.button_fake(fake_or_real), font=("Helvetica", 12), width=30, height=2, bg=dark_background_color, fg=text_color)

        btn1.pack(side=tk.LEFT, padx=5)
        btn2.pack(side=tk.LEFT, padx=5)

    def game_over_screen(self):
        
        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.title("Ratespiel")
        self.root.geometry("550x400") 

        label = tk.Label(self.root, text=f"Spiel beendet", font=("Helvetica", 16, "bold"), fg=text_color, bg=dark_background_color)
        label.pack(pady=20)

        label_score = tk.Label(self.root, text=f"Punkte: {self.score}/9", font=("Helvetica", 16, "bold"), fg=text_color, bg=dark_background_color)
        label_score.pack(pady=20)

        select_animals_button = tk.Button(self.root, text="Echte Ergebnisse anzeigen", command="", font=("Helvetica", 12), width=30, height=2, bg=dark_background_color, fg=text_color)
        select_animals_button.pack(pady=10)

        select_landscapes_button = tk.Button(self.root, text="Zurück zum Hauptmenü", command=lambda: self.init_screen(), font=("Helvetica", 12), width=30, height=2, bg=dark_background_color, fg=text_color)
        select_landscapes_button.pack(pady=10)

        # reset stats
        self.score = 0
        self.image_paths = []
        self.modus = ""

if __name__ == "__main__":
    root = tk.Tk()
    instance = GUIApp(root)
    root.mainloop()