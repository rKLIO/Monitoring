import tkinter as tk

# Création de la fenêtre principale
root = tk.Tk()
root.title("Fenêtre avec menu")
root.geometry("800x850")  # Dimensions initiales de la fenêtre

# Encadré supérieur pour la saisie
top_frame = tk.Frame(root, bg="lightgray", relief="groove", bd=2)
top_frame.pack(side="top", fill="x", padx=5, pady=5)

# Fonction pour récupérer le texte saisi
def get_text():
    print(f"Texte saisi : {entry.get()}")

# Fonction pour le deuxième bouton
def second_action():
    print("Deuxième bouton cliqué !")

# Conteneur pour les boutons alignés à droite
buttons_frame = tk.Frame(top_frame, bg="lightgray")
buttons_frame.pack(side="right", padx=10, pady=5)

# Bouton "Valider"
validate_button = tk.Button(buttons_frame, text="Valider", command=get_text)
validate_button.pack(side="left", padx=5)

# Deuxième bouton
second_button = tk.Button(buttons_frame, text="Autre Action", command=second_action)
second_button.pack(side="left", padx=5)

# Champ de texte pour saisir du contenu (remplit le reste de la largeur)
entry = tk.Entry(top_frame, font=("Arial", 14))
entry.pack(side="left", fill="x", expand=True, padx=10, pady=5)

# Encadré inférieur qui remplit le reste de la fenêtre
bottom_frame = tk.Frame(root, bg="white", relief="groove", bd=2)
bottom_frame.pack(side="bottom", fill="both", expand=True, padx=5, pady=5)

# Partie gauche de l'encadré inférieur (70% de la largeur)
left_frame = tk.Frame(bottom_frame, bg="lightblue", relief="groove", bd=2, width=int(800 * 0.7))
left_frame.pack(side="left", fill="both", expand=True, padx=5, pady=5)

left_label = tk.Label(left_frame, text="Zone gauche", font=("Arial", 14), bg="lightblue")
left_label.pack(pady=20)

# Partie droite de l'encadré inférieur (30% de la largeur)
right_frame = tk.Frame(bottom_frame, bg="white", relief="groove", bd=2, width=int(800 * 0.3))
right_frame.pack(side="right", fill="both", expand=True, padx=5, pady=5)

# Zone supérieure dans la partie droite (environ 33% de la hauteur de la partie droite)
top_right_frame = tk.Frame(right_frame, bg="lightgreen", relief="groove", bd=2, height=int(850 * 0.33))
top_right_frame.pack(side="top", fill="x", padx=5, pady=5)

top_right_label = tk.Label(top_right_frame, text="Zone droite supérieure", font=("Arial", 14), bg="lightgreen")
top_right_label.pack(pady=20)

# Zone inférieure dans la partie droite (remplit le reste)
bottom_right_frame = tk.Frame(right_frame, bg="lightpink", relief="groove", bd=2)
bottom_right_frame.pack(side="bottom", fill="both", expand=True, padx=5, pady=5)

bottom_right_label = tk.Label(bottom_right_frame, text="Zone droite inférieure", font=("Arial", 14), bg="lightpink")
bottom_right_label.pack(pady=20)

# Lancer la boucle principale
root.mainloop()