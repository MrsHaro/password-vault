from vault.auth import Authenticator
from vault.manager import PasswordManager
import os
import time

def main():
    time.sleep(0.5)
    os.system('cls' if os.name == 'nt' else 'clear')
    
    print("Bienvenue dans le gestionnaire de mots de passe Vault\n")
    
    auth = Authenticator()
    if not auth.is_initialized():
        auth.setup_master_password()
    if not auth.verify_master_password():
        print("Accès refusé. Mot de passe maître incorrect.")
        time.sleep(3)
        os.system('cls' if os.name == 'nt' else 'clear')
        
        print("Fermeture du gestionnaire.")
        time.sleep(1)
        return
    
    time.sleep(1)
    manager = PasswordManager(auth)
    manager.run()

if __name__ == "__main__":
    main()