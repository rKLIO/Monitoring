import socket
import threading

redemarrer = False

# Fonction pour envoyer des messages au serveur
def envoyer_message(connexion_server):
    
    global redemarrer

    while True:
        try:
            message = input("Entrez un message à envoyer au serveur (ou 'quit' pour quitter) : ")
            connexion_server.send(message.encode("utf-8"))
            
            if message.lower() == 'quit':
                print("Déconnexion demandée au serveur.")
                break  # Sortir de la boucle après avoir envoyé "quit"
            
            elif message.lower() == 'restart':
                print("Commande 'restart' reçue. Déconnexion et redémarrage du client.")
                redemarrer = True  # Signaler un redémarrage
                break

        except Exception as e:
            print(f"Erreur d'envoi : {e}")
            break

# Fonction pour recevoir des messages du serveur
def recevoir_message(connexion_server):
    while True:
        try:
            message = connexion_server.recv(1024).decode().strip()
            if not message:
                print("Serveur déconnecté.")
                break
            print(f"Message du serveur : {message}")
        except Exception as e:
            print(f"Erreur de réception : {e}")
            break

# Main
try:
    # Création et connexion au serveur
    connexion_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connexion_server.connect(('192.168.56.106', 1200))
    print("Connecté au serveur.")

    # Threads pour envoi et réception des messages
    thread_envoi = threading.Thread(target=envoyer_message, args=(connexion_server,))
    thread_reception = threading.Thread(target=recevoir_message, args=(connexion_server,))

    thread_envoi.start()
    thread_reception.start()

    thread_envoi.join()  # Attendre la fin du thread d'envoi
    thread_reception.join()  # Attendre la fin du thread de réception

except ConnectionRefusedError:
    print("Impossible de se connecter au serveur. Vérifiez l'adresse IP et le port.")
except Exception as e:
    print(f"Une erreur est survenue : {e}")
finally:
    connexion_server.close()
    print("Connexion au serveur fermée.")
    
    # Redémarrage du client uniquement si 'restart' a été saisi
    if redemarrer:
        import os
        import sys
        print("Redémarrage du client...")
        os.execl(sys.executable, sys.executable, *sys.argv)  # Relance le programme.