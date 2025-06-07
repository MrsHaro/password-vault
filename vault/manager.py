from vault.crypto import CryptoManager
import os
import time

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
            print("4. Quitter")
            choix = input("Choix : ")

            if choix == '1':
                self.lister_passwords()
            elif choix == '2':
                self.ajouter_password()
            elif choix == '3':
                self.supprimer_password()
            elif choix == '4':
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
