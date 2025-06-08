from vault.auth import Authenticator
from vault.manager import PasswordManager
import os
import time
import tkinter as tk
from gui.app import PasswordVaultApp

def main():
    time.sleep(0.5)
    os.system('cls' if os.name == 'nt' else 'clear')
    
    print("Bienvenue dans le gestionnaire de mots de passe Vault\n")
    
    auth = Authenticator()
    while True:
        if not auth.login_or_register():
            break
    
        time.sleep(1)
        manager = PasswordManager(auth)
        manager.run()

        os.system('cls' if os.name == 'nt' else 'clear')
        print("\t\tRetour au menu principal.")
        time.sleep(2)
        os.system('cls' if os.name == 'nt' else 'clear')

if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordVaultApp(root)
    root.mainloop()