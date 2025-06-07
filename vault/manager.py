from vault.crypto import CryptoManager
import os
import time
import random
import string

class PasswordManager:
    def __init__(self, auth):
        key = auth._derive_key(getattr(auth, 'password', ''))
        self.crypto = CryptoManager(key)
        self.crypto.initialize_vault()

    def run(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        while True:
            print("\t\t\t\tBienvenue dans le gestionnaire de mots de passe.\n")
            print("\t\t\t--- MENU ---")
            print("1. Lister les mots de passe")
            print("2. Ajouter un mot de passe")
            print("3. Supprimer un mot de passe")
            print("4. Rechercher un mot de passe")
            print("5. Générer un mot de passe aléatoire")
            print("6. Modifier un mot de passe")
            print("7. Quitter")
            choix = input("Choix : ")

            if choix == '1':
                self.lister_passwords()
            elif choix == '2':
                self.ajouter_password()
            elif choix == '3':
                self.supprimer_password()
            elif choix == '4':
                self.rechercher_password()
            elif choix == '5':
                print("\n\nMot de passe généré :", self.generer_mot_de_passe())
                input("\nAppuyez sur Entrée pour continuer...")
                os.system('cls' if os.name == 'nt' else 'clear')
            elif choix == '6':
                self.modifier_password()
            elif choix == '7':
                print("\n\nFermeture du gestionnaire.")
                time.sleep(2)
                os.system('cls' if os.name == 'nt' else 'clear')
                break
            else:
                print("Choix invalide. Veuillez réessayer.")

    def lister_passwords(self):
        data = self.crypto.load_data()
        if not data:
            print("\nAucun mot de passe enregistré.")
            time.sleep(2)
            os.system('cls' if os.name == 'nt' else 'clear')
            return
        else:
            for site, creds in data.items():
                os.system('cls' if os.name == 'nt' else 'clear')
                print("\t\t\t\tVoici les mots de passe enregistrés\n")
                print(f"- {site} : \n\tNom d'utilisateur: {creds['username']} \n\tMot de passe: {creds['password']}")
                input("\nAppuyez sur Entrée pour continuer...")
                os.system('cls' if os.name == 'nt' else 'clear')
                

    def ajouter_password(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\t\t\t\tAjout d'un nouveau mot de passe.\n")
        print("Veuillez entrer les informations suivantes :")
        site = input("Nom du site : ")
        username = input("\nNom d'utilisateur : ")
        password = input("\nMot de passe : ")
        data = self.crypto.load_data()
        data[site] = {'username': username, 'password': password}
        self.crypto.save_data(data)
        print("\nMot de passe ajouté avec succès.")
        time.sleep(2)
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def rechercher_password(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\t\t\t\tRecherche de mot de passe.\n")
        recherche = input("Entrez le nom (ou une partie) du site à rechercher : ").lower()
        data = self.crypto.load_data()
        resultats = {site: creds for site, creds in data.items() if recherche in site.lower()}

        if resultats:
            print("\nRésultats trouvés :")
            for site, creds in resultats.items():
                print(f"- {site} : {creds['username']} / {creds['password']}")
            input("\nAppuyez sur Entrée pour continuer...")
        else:
            os.system('cls' if os.name == 'nt' else 'clear')
            print("Aucun résultat trouvé.")
        time.sleep(2)
        os.system('cls' if os.name == 'nt' else 'clear')

    def supprimer_password(self):
      data = self.crypto.load_data()
      if not data:
        print("Aucun site à supprimer.")
        time.sleep(2)
        os.system('cls' if os.name == 'nt' else 'clear')
        return

      sites = list(data.keys())
      os.system('cls' if os.name == 'nt' else 'clear')
      print("\t\t\t\tSuppression d'un mot de passe.\n")
      print("\nSites enregistrés :")
      for idx, site in enumerate(sites, 1):
        print(f"{idx}. {site}")

      try:
        choix = int(input("Entrez le numéro du site à supprimer (entrez 0 pour annuler): "))
        if 1 <= choix <= len(sites):
          site_to_delete = sites[choix - 1]
          del data[site_to_delete]
          self.crypto.save_data(data)
          print(f"Mot de passe pour '{site_to_delete}' supprimé.")
        elif choix == 0:
          os.system('cls' if os.name == 'nt' else 'clear')
          print("\n\n\t\t\t\tSuppression annulée.")
          time.sleep(2)
          os.system('cls' if os.name == 'nt' else 'clear')
          return
        else:
          print("\nNuméro invalide.\n")
      except ValueError:
        print("\nEntrée invalide.\n")
      time.sleep(2)
      os.system('cls' if os.name == 'nt' else 'clear')

    def generer_mot_de_passe(self, longueur=16):
        caracteres = string.ascii_letters + string.digits + string.punctuation
        return ''.join(random.choice(caracteres) for _ in range(longueur))

    def modifier_password(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\t\t\t\tModification d'un mot de passe.\n")
        site = input("Nom du site à modifier : ")
        data = self.crypto.load_data()
        if site in data:
            username = input(f"Nom d'utilisateur [{data[site]['username']}] : ") or data[site]['username']
            password = input(f"Nouveau mot de passe (laisser vide pour conserver l'actuel) : ") or data[site]['password']
            data[site] = {'username': username, 'password': password}
            self.crypto.save_data(data)

            print("\nMot de passe mis à jour.")
            time.sleep(2)
            os.system('cls' if os.name == 'nt' else 'clear')
        else:
            os.system('cls' if os.name == 'nt' else 'clear')
            print("Ce site n'existe pas dans la base.")
            time.sleep(2)
            os.system('cls' if os.name == 'nt' else 'clear')
