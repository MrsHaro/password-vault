import tkinter as tk
from tkinter import messagebox
from vault.auth import Authenticator
from vault.manager import PasswordManager


class PasswordVaultApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PasswordVault")
        self.root.geometry("500x400")
        
        self.auth = Authenticator()
        self.manager = PasswordManager(self.auth)
        self.current_user = None
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

        quit_button = tk.Button(
            frame,
            text="Quitter",
            width=10,
            height=2,
            bg="red",
            fg="white",
            font=("Arial", 12, "bold"),
            command=self.root.quit
        )
        quit_button.pack(pady=10)

        # pied de page
        footer = tk.Label(self.root, text="© Arthur TCHANDA", font=("Arial", 11, "italic"), fg="black")
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
                self.current_user = self.auth.username
                messagebox.showinfo("Connexion", "Connexion réussie !")
                self.dashboard()
            else:
                messagebox.showerror("Connexion", "Échec de connexion.")

        tk.Button(frame, text="Connexion", command=login_action, bg="green", fg="white").pack(pady=10)
        tk.Button(frame, text="Retour", command=self.show_home, bg="red", fg="white").pack()

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
                messagebox.showinfo("Inscription", "Compte créé avec succès !")
                self.show_home()
            else:
                messagebox.showerror("Erreur", "Nom d'utilisateur déjà utilisé.")

        tk.Button(frame, text="Créer le compte", command=register_action, bg="green").pack(pady=10)
        tk.Button(frame, text="Retour", command=self.show_home, bg="red", fg="white",).pack()

    def dashboard(self):
        self.clear_frame()

        frame = tk.Frame(self.root)
        frame.pack(pady=20)

        welcome_text = f"Bienvenue {self.auth.username} !" if self.auth.username else "Bienvenue !"
        tk.Label(frame, text=welcome_text, font=("Arial", 14)).pack(pady=10)

        tk.Button(frame, text="Ajouter un mot de passe", width=30, command=self.show_add_password_screen).pack(pady=5)
        tk.Button(frame, text="Afficher les mots de passe", width=30, command=self.not_implemented).pack(pady=5)
        tk.Button(frame, text="Supprimer un mot de passe", width=30, command=self.not_implemented).pack(pady=5)
        tk.Button(frame, text="Rechercher un mot de passe", width=30, command=self.not_implemented).pack(pady=5)
        tk.Button(frame, text="Modifier un mot de passe", width=30, command=self.not_implemented).pack(pady=5)
        tk.Button(frame, text="Générer un mot de passe", width=30, command=self.not_implemented).pack(pady=5)
        tk.Button(
            frame,
            text="Déconnexion",
            width=30,
            height=2,
            bg="red",
            fg="white",
            font=("Arial", 12, "bold"),
            command=self.logout
        ).pack(pady=20)

    def logout(self):
        self.auth.username = None
        self.auth.password = None
        self.current_user = None
        self.show_home()

    # !Ajouter un mot de passe
    def show_add_password_screen(self):
      self.clear_window()

      title_label = tk.Label(self.root, text="Ajouter un mot de passe", font=("Helvetica", 18,   "bold"))
      title_label.pack(pady=20)

      site_label = tk.Label(self.root, text="Nom du site")
      site_label.pack()
      site_entry = tk.Entry(self.root)
      site_entry.pack()

      username_label = tk.Label(self.root, text="Nom d'utilisateur")
      username_label.pack()
      username_entry = tk.Entry(self.root)
      username_entry.pack()

      password_label = tk.Label(self.root, text="Mot de passe")
      password_label.pack()
      password_entry = tk.Entry(self.root)
      password_entry.pack()

      def submit():
          site = site_entry.get()
          username = username_entry.get()
          password = password_entry.get()
          if site and username and password:
              self.manager.ajouter_password_direct(site, username, password)
              messagebox.showinfo("Succès", "Mot de passe ajouté !")
              self.create_dashboard_screen()
          else:
              messagebox.showerror("Erreur", "Tous les champs sont obligatoires")

      add_btn = tk.Button(self.root, text="Ajouter", command=submit)
      add_btn.pack(pady=10)

      back_btn = tk.Button(self.root, text="Retour", command=self.dashboard)
      
      back_btn.pack()

    def not_implemented(self):
        messagebox.showinfo("À venir", "Cette fonctionnalité sera bientôt disponible.")
    
    def clear_window(self):
      for widget in self.root.winfo_children():
        widget.destroy()
