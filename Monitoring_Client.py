import tkinter as tk
from tkinter import ttk
import socket
import threading
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from collections import deque
import time

# Variables globales
connexion_server = None
cpu_usage_data = deque([0] * 30, maxlen=30)
ram_usage_data = deque([0] * 30, maxlen=30)
connexion_etablie = False
collecte_active = False


def afficher_message(message, onglet=""):
    """Ajoute un message dans l'onglet correspondant."""
    if onglet == "Performance":
        texte_performance.insert(tk.END, f"{message}\n")
        texte_performance.see(tk.END)
    else:
        texte_log.insert(tk.END, f"{message}\n")
        texte_log.see(tk.END)


def collecter_informations_auto():
    """Lance la collecte des performances toutes les 1 seconde."""
    global collecte_active
    collecte_active = True

    def collect_task():
        global connexion_server, connexion_etablie, collecte_active
        while collecte_active and connexion_etablie:
            try:
                connexion_server.send("collect_info".encode("utf-8"))
                connexion_server.settimeout(5)
                response = connexion_server.recv(2048).decode("utf-8").strip()
                connexion_server.settimeout(None)

                afficher_message(f"Réponse du serveur : {response}", "Performance")

                # Extraction des valeurs CPU et RAM
                try:
                    lines = response.split("\n")
                    for line in lines:
                        if "CPU usage per core" in line:
                            cpu_value = float(line.split(":")[1].strip(" []").split(",")[0])
                            cpu_usage_data.append(cpu_value)
                        elif "RAM usage" in line:  # Adaptez selon les données réelles
                            ram_value = float(line.split(":")[1].strip())
                            ram_usage_data.append(ram_value)
                    mise_a_jour_graphiques()
                except ValueError as e:
                    afficher_message(f"Erreur de format des données : {e}", "Performance")

                time.sleep(1)  # Pause d'une seconde entre chaque collecte
            except Exception as e:
                afficher_message(f"Erreur lors de la collecte : {e}", "Performance")
                collecte_active = False

    threading.Thread(target=collect_task, daemon=True).start()


def arreter_collecte():
    """Arrête la collecte automatique des performances."""
    global collecte_active
    collecte_active = False
    afficher_message("Collecte des performances arrêtée.", "Performance")


def mise_a_jour_graphiques():
    """Met à jour les graphiques avec les nouvelles données."""
    cpu_line.set_ydata(cpu_usage_data)
    ram_line.set_ydata(ram_usage_data)
    canvas_performance.draw()


def envoyer_commande():
    """Envoie une commande manuelle au serveur."""
    global connexion_server, connexion_etablie
    if not connexion_etablie:
        afficher_message("Erreur : Non connecté au serveur.", "Connexion")
        return

    commande = entry_commande.get()
    if not commande:
        afficher_message("Veuillez entrer une commande.", "Connexion")
        return

    try:
        connexion_server.send(commande.encode("utf-8"))
        response = connexion_server.recv(1024).decode("utf-8").strip()
        afficher_message(f"Réponse : {response}", "Connexion")
    except Exception as e:
        afficher_message(f"Erreur : {e}", "Connexion")


def deconnecter():
    """Envoie la commande 'quit' pour déconnecter le client."""
    global connexion_server, connexion_etablie
    if not connexion_etablie:
        afficher_message("Erreur : Déjà déconnecté.", "Connexion")
        return

    try:
        connexion_server.send("quit".encode("utf-8"))
        connexion_server.close()
        connexion_etablie = False
        afficher_message("Déconnecté du serveur.", "Connexion")
    except Exception as e:
        afficher_message(f"Erreur : {e}", "Connexion")


def redemarrer_serveur():
    """Envoie la commande 'restart' pour redémarrer le serveur."""
    global connexion_server, connexion_etablie
    if not connexion_etablie:
        afficher_message("Erreur : Non connecté au serveur.", "Connexion")
        return

    try:
        connexion_server.send("restart".encode("utf-8"))
        response = connexion_server.recv(1024).decode("utf-8").strip()
        afficher_message(f"Réponse : {response}", "Connexion")
    except Exception as e:
        afficher_message(f"Erreur : {e}", "Connexion")


def connecter_au_serveur():
    """Tente de se connecter au serveur."""
    global connexion_server, connexion_etablie
    adresse_ip = entry_ip.get()

    if not adresse_ip:
        afficher_message("Veuillez entrer une adresse IP.", "Connexion")
        return

    try:
        connexion_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connexion_server.connect((adresse_ip, 1200))  # Exemple de port
        connexion_etablie = True
        afficher_message(f"Connexion réussie à {adresse_ip}.", "Connexion")
        collecter_informations_auto()  # Démarre la collecte automatique après connexion
    except Exception as e:
        afficher_message(f"Erreur de connexion : {e}", "Connexion")


# Interface principale
fenetre = tk.Tk()
fenetre.title("Application Client-Serveur")

# Styles
style = ttk.Style()
style.configure("TButton", font=("Poppins", 12))
style.configure("TLabel", font=("Poppins", 12))
style.configure("TEntry", font=("Poppins", 12))

# Onglets
onglets = ttk.Notebook(fenetre)
onglet_connexion = ttk.Frame(onglets)
onglet_performance = ttk.Frame(onglets)
onglets.add(onglet_connexion, text="Connexion")
onglets.add(onglet_performance, text="Performance")
onglets.pack(expand=1, fill="both")

# Onglet Connexion
frame_connexion = ttk.LabelFrame(onglet_connexion, text="Connexion au serveur")
frame_connexion.pack(pady=10, padx=10, fill="x")
label_ip = ttk.Label(frame_connexion, text="Adresse IP du serveur :")
label_ip.pack(pady=5, anchor="w")
entry_ip = ttk.Entry(frame_connexion)
entry_ip.pack(pady=5, padx=10, fill="x")
bouton_connexion = ttk.Button(frame_connexion, text="Se connecter", command=connecter_au_serveur)
bouton_connexion.pack(pady=5)

frame_commande = ttk.LabelFrame(onglet_connexion, text="Commandes")
frame_commande.pack(pady=10, padx=10, fill="x")
entry_commande = ttk.Entry(frame_commande)
entry_commande.pack(pady=5, padx=10, fill="x")
bouton_envoyer_commande = ttk.Button(frame_commande, text="Envoyer Commande", command=envoyer_commande)
bouton_envoyer_commande.pack(pady=5)

frame_actions = ttk.LabelFrame(onglet_connexion, text="Actions rapides")
frame_actions.pack(pady=10, padx=10, fill="x")
bouton_deconnecter = ttk.Button(frame_actions, text="Déconnecter", command=deconnecter)
bouton_deconnecter.pack(side="left", padx=10, pady=5)
bouton_redemarrer = ttk.Button(frame_actions, text="Redémarrer", command=redemarrer_serveur)
bouton_redemarrer.pack(side="right", padx=10, pady=5)

texte_log = tk.Text(
    onglet_connexion,
    height=10,
    font=("Poppins", 10),
    bg="black",  # Fond noir
    fg="white"   # Texte blanc
)
texte_log.pack(padx=10, pady=10, expand=True, fill="both")

# Onglet Performance
fig, (ax_cpu, ax_ram) = plt.subplots(2, 1, figsize=(5, 4), dpi=100)
ax_cpu.set_title("Utilisation CPU (%)")
ax_ram.set_title("Utilisation RAM (%)")
ax_cpu.set_ylim(0, 100)
ax_ram.set_ylim(0, 100)
cpu_line, = ax_cpu.plot(cpu_usage_data, label="Utilisation CPU", color="blue")
ram_line, = ax_ram.plot(ram_usage_data, label="Utilisation RAM", color="green")
canvas_performance = FigureCanvasTkAgg(fig, master=onglet_performance)
canvas_widget = canvas_performance.get_tk_widget()
canvas_widget.pack(expand=True, fill="both")

texte_performance = tk.Text(onglet_performance,
    height=10,
    font=("Poppins", 10),
    bg="black",  # Fond noir
    fg="white"   # Texte blanc
    )
texte_performance.pack(pady=5, padx=10, expand=True, fill="both")

# Bouton pour arrêter la collecte
bouton_arreter_collecte = ttk.Button(onglet_performance, text="Arrêter Collecte", command=arreter_collecte)
bouton_arreter_collecte.pack(pady=5)

fenetre.mainloop()
