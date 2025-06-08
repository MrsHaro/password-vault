import tkinter as tk
from tkinter import messagebox
import getpass
from vault.auth import Authenticator

class PasswordVaultApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PasswordVault")
        self.root.geometry("400x300")
        
        self.auth = Authenticator()
        self.show_home()

    def clear_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def show_home(self):
        self.clear_frame()

        frame = tk.Frame(self.root)
        frame.pack(pady=40)

        title = tk.Label(frame, text="Bienvenue dans PasswordVault", font=("Arial", 16))
        title.pack(pady=20)

        login_button = tk.Button(frame, text="Se connecter", width=20, command=self.login_screen)
        login_button.pack(pady=10)

        register_button = tk.Button(frame, text="Créer un compte", width=20, command=self.register_screen)
        register_button.pack(pady=10)

        quit_button = tk.Button(frame, text="Quitter", width=20, command=self.root.quit)
        quit_button.pack(pady=10)

        # pied de page
        footer = tk.Label(self.root, text="© Arthur TCHANDA", font=("Arial", 10))
        footer.pack(side=tk.BOTTOM, pady=10)

    def login_screen(self):
        self.clear_frame()

        frame = tk.Frame(self.root)
        frame.pack(pady=20)

        tk.Label(frame, text="Connexion", font=("Arial", 14)).pack(pady=10)

        tk.Label(frame, text="Nom d'utilisateur:").pack()
        username_entry = tk.Entry(frame)
        username_entry.pack()

        tk.Label(frame, text="Mot de passe:").pack()
        password_entry = tk.Entry(frame, show="*")
        password_entry.pack()

        def login_action():
            username = username_entry.get()
            password = password_entry.get()
            if self.auth.login(username, password):
                messagebox.showinfo("Succès", "Connexion réussie !")
                self.show_home()
            else:
                messagebox.showerror("Erreur", "Échec de connexion.")

        tk.Button(frame, text="Connexion", command=login_action).pack(pady=10)
        tk.Button(frame, text="Retour", command=self.show_home).pack()

    def register_screen(self):
        self.clear_frame()

        frame = tk.Frame(self.root)
        frame.pack(pady=20)

        tk.Label(frame, text="Créer un compte", font=("Arial", 14)).pack(pady=10)

        tk.Label(frame, text="Nom d'utilisateur:").pack()
        username_entry = tk.Entry(frame)
        username_entry.pack()

        tk.Label(frame, text="Mot de passe:").pack()
        password_entry = tk.Entry(frame, show="*")
        password_entry.pack()

        tk.Label(frame, text="Confirmez le mot de passe:").pack()
        confirm_entry = tk.Entry(frame, show="*")
        confirm_entry.pack()

        def register_action():
            username = username_entry.get()
            password = password_entry.get()
            confirm = confirm_entry.get()
            if password != confirm:
                messagebox.showerror("Erreur", "Les mots de passe ne correspondent pas.")
                return

            if self.auth.register(username, password):
                messagebox.showinfo("Succès", "Compte créé avec succès !")
                self.show_home()
            else:
                messagebox.showerror("Erreur", "Nom d'utilisateur déjà utilisé.")

        tk.Button(frame, text="Créer le compte", command=register_action).pack(pady=10)
        tk.Button(frame, text="Retour", command=self.show_home).pack()