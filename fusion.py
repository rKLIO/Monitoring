import socket
import threading
import tkinter as tk
import time

# Initialisation des variables
connexion_server = None
redemarrer = False
stop_auto_execution = False

def envoyer_message():
    """
    Envoie un message au serveur à partir du champ de texte.
    """
    global connexion_server, redemarrer

    if connexion_server is None:
        afficher_message_gauche("Erreur : Non connecté au serveur.")
        return

    message = entry.get().strip()  # Récupérer le texte saisi
    entry.delete(0, tk.END)  # Effacer le champ de texte

    try:
        connexion_server.send(message.encode("utf-8"))
        afficher_message_gauche(f"Vous : {message}")

        if message.lower() == 'quit':
            afficher_message_gauche("Déconnexion demandée au serveur.")
            connexion_server.close()
            connexion_server = None
        elif message.lower() == 'restart':
            afficher_message_gauche("Commande 'restart' reçue. Déconnexion et redémarrage du client.")
            redemarrer = True
            #connexion_server.close()
            #connexion_server = None

    except Exception as e:
        afficher_message_gauche(f"Erreur d'envoi : {e}")

def recevoir_message():
    """
    Reçoit des messages du serveur et les affiche dans l'interface.
    """
    global connexion_server

    while connexion_server:
        try:
            message = connexion_server.recv(1024).decode().strip()
            if not message:
                afficher_message_gauche("Serveur déconnecté.")
                break
            afficher_message_gauche(f"Message du serveur : {message}")
        except Exception as e:
            afficher_message_gauche(f"Erreur de réception : {e}")
            break

def lancer_connexion():
    """
    Connecte le client au serveur et démarre les threads.
    """
    global connexion_server

    try:
        afficher_message_gauche("Connexion au serveur...")
        connexion_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connexion_server.connect(('192.168.56.106', 1200))
        afficher_message_gauche("Connecté au serveur.")

        # Thread pour gérer la réception
        thread_reception = threading.Thread(target=recevoir_message, daemon=True)
        thread_reception.start()

    except ConnectionRefusedError:
        afficher_message_gauche("Impossible de se connecter au serveur. Vérifiez l'adresse IP et le port.")
    except Exception as e:
        afficher_message_gauche(f"Une erreur est survenue : {e}")

def afficher_message_gauche(message):
    """
    Affiche un message dans la zone gauche (left_frame).
    """
    left_frame_text.insert(tk.END, message + "\n")
    left_frame_text.see(tk.END)

def afficher_message_droite(reponse):
    """
    Affiche un message dans la zone droite inférieure (bottom_right_frame).
    """
    bottom_right_text.delete(1.0, tk.END)  # Supprime le texte précédent
    bottom_right_text.insert(tk.END, reponse)

def collecter_informations():
    """
    Envoie une commande au serveur pour collecter des informations et affiche uniquement dans bottom_right_frame.
    """
    global connexion_server

    if connexion_server is None:
        afficher_message_droite("Erreur : Non connecté au serveur.")
        return

    try:
        # Envoyer la commande pour récupérer les informations
        commande = "collect_info"
        #print(f"Envoi de la commande au serveur : {commande}")  # Debug print
        connexion_server.send(commande.encode("utf-8"))

        # Configurer un délai d'attente pour éviter le blocage indéfini
        connexion_server.settimeout(3)  # Délai d'attente de 2 secondes

        # Recevoir la réponse du serveur
        response = connexion_server.recv(1024).decode("utf-8").strip()
        #print(f"Réponse reçue du serveur : {response}")  # Debug print

        # Si la réponse est vide ou ne correspond pas à ce qui est attendu
        if not response:
            afficher_message_droite("Aucune réponse du serveur.")
        else:
            # Assurez-vous que seul ce message apparaît dans la zone de droite
            afficher_message_droite(response)

    except socket.timeout:
        afficher_message_droite("Erreur : Délai d'attente dépassé.")
    except Exception as e:
        afficher_message_droite(f"Erreur lors de la communication avec le serveur : {e}")



def auto_executer_commandes():
    """
    Exécute collecter_informations toutes les secondes.
    """
    global stop_auto_execution
    while not stop_auto_execution:
        collecter_informations()
        time.sleep(1)

def lancer_auto_execution():
    """
    Lance un thread pour l'exécution automatique des commandes.
    """
    global stop_auto_execution
    stop_auto_execution = False
    threading.Thread(target=auto_executer_commandes, daemon=True).start()

def arreter_auto_execution():
    """
    Arrête l'exécution automatique des commandes.
    """
    global stop_auto_execution
    stop_auto_execution = True

# def afficher_message(message):
#     """
#     Affiche un message dans la zone gauche.
#     """
#     text_area.insert(tk.END, message + "\n")
#     text_area.see(tk.END)

# Interface graphique
root = tk.Tk()
root.title("Client avec Interface")
root.geometry("800x850")

# Encadré supérieur
top_frame = tk.Frame(root, bg="lightgray", relief="groove", bd=2)
top_frame.pack(side="top", fill="x", padx=5, pady=5)

# Champ de texte pour saisir la commande
entry = tk.Entry(top_frame, font=("Arial", 14))
entry.pack(side="left", fill="x", expand=True, padx=10, pady=5)

# Conteneur des boutons
buttons_frame = tk.Frame(top_frame, bg="lightgray")
buttons_frame.pack(side="right", padx=10, pady=5)

# Bouton "Valider"
validate_button = tk.Button(buttons_frame, text="Valider", command=envoyer_message)
validate_button.pack(side="left", padx=5)

# Bouton "Connexion au serveur"
connect_button = tk.Button(buttons_frame, text="Connexion", command=lancer_connexion)
connect_button.pack(side="left", padx=5)

# Encadré inférieur (contenu principal)
bottom_frame = tk.Frame(root, bg="white", relief="groove", bd=2)
bottom_frame.pack(side="bottom", fill="both", expand=True, padx=5, pady=5)

# Zone gauche (messages) : 70% de la largeur
left_frame = tk.Frame(bottom_frame, bg="lightblue", relief="groove", bd=2)
left_frame.pack(side="left", fill="both", expand=True, padx=5, pady=5)

# Texte déroulant pour afficher les messages
left_frame_text = tk.Text(left_frame, font=("Arial", 12), bg="white", state="normal")
left_frame_text.pack(fill="both", expand=True)

# Zone droite (conteneur général pour diviser en 2 parties) : 30% de la largeur
right_frame = tk.Frame(bottom_frame, bg="white", relief="groove", bd=2, width=240)
right_frame.pack(side="right", fill="both", expand=False, padx=5, pady=5)

# Zone droite supérieure (Bouton)
top_right_frame = tk.Frame(right_frame, bg="lightgreen", relief="groove", bd=2, height=100)
top_right_frame.pack(side="top", fill="x", padx=5, pady=5)

top_right_button = tk.Button(top_right_frame, text="Exécuter Commandes", command=lancer_auto_execution)
top_right_button.pack(pady=10)

# Bouton pour arrêter l'exécution automatique
stop_button = tk.Button(top_right_frame, text="Arrêter", command=arreter_auto_execution)
stop_button.pack(pady=10)

# Zone droite inférieure
bottom_right_frame = tk.Frame(right_frame, bg="lightpink", relief="groove", bd=2)
bottom_right_frame.pack(side="bottom", fill="both", expand=True, padx=5, pady=5)

bottom_right_text = tk.Text(bottom_right_frame, font=("Arial", 12), bg="white", state="normal")
bottom_right_text.pack(fill="both", expand=True)

# Lancement de l'interface
root.mainloop()