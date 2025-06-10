import os
import time
import getpass
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
import base64
import json

class Authenticator:
    USERS_FILE = os.path.join('data', 'users.json')

    def __init__(self):
        self.username = None
        self.password = None
        self.salt = None
        self.backend = default_backend()
        if not os.path.exists(self.USERS_FILE):
            with open(self.USERS_FILE, 'w') as f:
                json.dump({}, f)

    def login_or_register(self) -> bool:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\n\t\t\t\tBienvenue dans le gestionnaire de mots de passe Vault\n")
        print("1. Se connecter\n")
        print("2. Créer un compte\n")
        print("3. Quitter\n")
        choix = input("Entrer votre Choix : ")
        if choix == '1':
            return self.login_cli()
        elif choix == '2':
            return self.register_cli()
        elif choix == '3':
            os.system('cls' if os.name == 'nt' else 'clear')
            print("\n\t\t\t\tMerci d'avoir utilisé Vault !")
            print("\n\t\t\t\tFermeture du gestionnaire.")
            time.sleep(2)
            os.system('cls' if os.name == 'nt' else 'clear')
            return False
        else:
            print("\nChoix invalide.")
            time.sleep(2)
            os.system('cls' if os.name == 'nt' else 'clear')
            return self.login_or_register()

    def register_cli(self) -> bool:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\n\t\t\t\tCréation de compte\n\n")
        username = input("Nom d'utilisateur : ")
        with open(self.USERS_FILE, 'r') as f:
            users = json.load(f)

        if username in users:
            print("\n\tCe nom d'utilisateur existe déjà.")
            time.sleep(3)
            os.system('cls' if os.name == 'nt' else 'clear')
            return self.login_or_register()

        while True:
            pwd = getpass.getpass("Mot de passe : ")
            pwd2 = getpass.getpass("Confirmez le mot de passe : ")
            if pwd != pwd2:
                print("\n\tLes mots de passe ne correspondent pas.")
            else:
                break

        salt = os.urandom(16)
        key = self._derive_key(pwd, salt)
        users[username] = {
            'salt': base64.b64encode(salt).decode(),
            'hash': key.decode()
        }

        with open(self.USERS_FILE, 'w') as f:
            json.dump(users, f)

        os.makedirs(os.path.join('data', 'vaults'), exist_ok=True)
        self.username = username
        self.password = pwd
        self.salt = salt
        print("\t\t\tCompte créé avec succès !")
        time.sleep(3)
        os.system('cls' if os.name == 'nt' else 'clear')
        return True

    def login_cli(self) -> bool:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\n\t\t\t\tConnexion\n\n")
        print("Veuillez entrer vos identifiants :")
        username = input("Nom d'utilisateur : ")
        with open(self.USERS_FILE, 'r') as f:
            users = json.load(f)

        if username not in users:
            print("\nCe compte n'existe pas.")
            return False

        salt = base64.b64decode(users[username]['salt'])
        hash_saved = users[username]['hash'].encode()

        tentatives = 3
        while tentatives > 0:
            pwd = getpass.getpass("Mot de passe : ")
            key_try = self._derive_key(pwd, salt)

            if key_try == hash_saved:
                self.username = username
                self.password = pwd
                self.salt = salt
                print("\nConnexion réussie !")
                time.sleep(2)
                os.system('cls' if os.name == 'nt' else 'clear')
                return True
            else:
                tentatives -= 1
                print(f"\n\nMot de passe incorrect. Tentatives restantes : {tentatives}")
                time.sleep(3)
                os.system('cls' if os.name == 'nt' else 'clear')

        print("Trop de tentatives échouées. Retour au menu principal.")
        time.sleep(3)
        os.system('cls' if os.name == 'nt' else 'clear')
        return False
    
    def register(self, username: str, password: str) -> bool:
      with open(self.USERS_FILE, 'r') as f:
        users = json.load(f)

      if username in users:
        return False  # L'utilisateur existe déjà

      salt = os.urandom(16)
      key = self._derive_key(password, salt)
      users[username] = {
          'salt': base64.b64encode(salt).decode(),
          'hash': key.decode()
      }

      with open(self.USERS_FILE, 'w') as f:
          json.dump(users, f)

      os.makedirs(os.path.join('data', 'vaults'), exist_ok=True)
      self.username = username
      self.password = password
      self.salt = salt
      return True
    
    def login(self, username: str, password: str) -> bool:
      if not os.path.exists(self.USERS_FILE):
          return False
  
      with open(self.USERS_FILE, 'r') as f:
          users = json.load(f)
  
      if username not in users:
          return False
  
      salt = base64.b64decode(users[username]['salt'])
      hash_saved = users[username]['hash'].encode()
  
      key_try = self._derive_key(password, salt)
  
      if key_try == hash_saved:
          self.username = username
          self.password = password
          self.salt = salt
          return True
      else:
          return False

    def _derive_key(self, password: str, salt: bytes) -> bytes:
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100_000,
            backend=self.backend
        )
        return base64.urlsafe_b64encode(kdf.derive(password.encode()))