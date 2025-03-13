import socket
import psutil
import threading

clients_actifs = []

# Fonction pour collecter toutes les informations
def collecter_informations():
    try:
        # Récupérer les informations avec psutil
        nb_logical_cpu = psutil.cpu_count(logical=True)
        nb_physical_cpu = psutil.cpu_count(logical=False)
        cpu_usage_per_cores = psutil.cpu_percent(interval=1, percpu=True)
        cpu_frequence = psutil.cpu_freq()

        # Préparer la chaîne de réponse
        resultat = (
            f"Number of logical CPU cores: {nb_logical_cpu}\n"
            f"Number of physical CPU cores: {nb_physical_cpu}\n"
            f"CPU usage per core: {cpu_usage_per_cores}\n"
            f"Fréquence actuelle du CPU : {cpu_frequence.current:.2f} MHz\n"
            f"Fréquence maximale du CPU : {cpu_frequence.max:.2f} MHz\n"
            f"Fréquence minimale du CPU : {cpu_frequence.min:.2f} MHz"
        )
        return resultat
    except Exception as e:
        return f"Erreur lors de la collecte des informations: {e}"


# Fonction pour gérer un client
def gerer_client(connexion_client, adresse_client):
    global clients_actifs
    clients_actifs.append(connexion_client)  # Ajouter le client à la liste active

    print(f"Connexion établie avec {adresse_client}")
    while True:
        try:
            # Réception des messages du client
            message = connexion_client.recv(1024).decode().strip()  # Conversion en chaîne
            if not message:
                break  # Le client s'est déconnecté
            print(f"Message reçu de {adresse_client}: {message}")

            # Si le message est "collect_info", exécuter toutes les commandes
            if message.lower() == 'collect_info':
                resultat = collecter_informations()
                connexion_client.send(resultat.encode())
                print(f"Envoyé au client {adresse_client}: \n{resultat}")

            # Commande "quit" pour déconnexion
            elif message.lower() == 'quit':
                print(f"Client {adresse_client} a demandé la déconnexion.")
                connexion_client.send("Déconnexion réussie.".encode())
                break  # Sortir de la boucle et fermer la connexion

            else:
                connexion_client.send(f"Commande non reconnue: {message}".encode())

        except ConnectionResetError:
            print(f"Déconnexion brusque de {adresse_client}")
            break
        except Exception as e:
            print(f"Erreur avec {adresse_client}: {e}")
            break

    connexion_client.close()
    clients_actifs.remove(connexion_client)
    print(f"Connexion fermée avec {adresse_client}")


# Initialisation du serveur
socket_ecoute = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket_ecoute.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
socket_ecoute.bind(('', 1200))  # Le serveur écoute sur toutes les interfaces réseau, port 1200
socket_ecoute.listen()          # Le serveur écoute les connexions entrantes
print("Serveur en écoute sur le port 1200...")

# Boucle principale pour accepter et gérer les connexions
while True:
    connexion_client, adresse_client = socket_ecoute.accept()
    print(f"Nouvelle connexion de {adresse_client}")
    thread_client = threading.Thread(target=gerer_client, args=(connexion_client, adresse_client))
    thread_client.start()
