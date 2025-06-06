from vault.auth import Authenticator
from vault.manager import PasswordManager
import os

def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    
    print("Bienvenue dans le gestionnaire de mots de passe Vault\n")
    
    auth = Authenticator()
    if not auth.is_initialized():
        auth.setup_master_password()
    if not auth.verify_master_password():
        print("Accès refusé. Mot de passe maître incorrect.")
        return

    manager = PasswordManager(auth)
    manager.run()

if __name__ == "__main__":
    main()