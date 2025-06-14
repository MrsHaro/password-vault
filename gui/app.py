import tkinter as tk
from tkinter import messagebox
from vault.auth import Authenticator
from vault.manager import PasswordManager


class PasswordVaultApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PasswordVault (v.1.0)")
        self.root.geometry("500x400")
        
        self.auth = Authenticator()
        self.manager = None  # Ne pas initialiser ici
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
                self.manager = PasswordManager(self.auth)  # Initialiser ici
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
                self.manager = PasswordManager(self.auth)  # Initialiser ici si besoin
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
        tk.Button(frame, text="Afficher les mots de passe", width=30, command=self.show_view_passwords_screen).pack(pady=5)
        tk.Button(frame, text="Supprimer un mot de passe", width=30, command=self.show_delete_password_screen).pack(pady=5)
        tk.Button(frame, text="Rechercher un mot de passe", width=30, command=self.show_search_password_screen).pack(pady=5)
        tk.Button(frame, text="Modifier un mot de passe", width=30, command=self.show_edit_password_screen).pack(pady=5)
        tk.Button(frame, text="Générer un mot de passe", width=30, command=self.show_generate_password_screen).pack(pady=5)
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
              self.dashboard()
          else:
              messagebox.showerror("Erreur", "Tous les champs sont obligatoires")

      add_btn = tk.Button(self.root, text="Ajouter", command=submit)
      add_btn.pack(pady=10)

      back_btn = tk.Button(self.root, text="Retour", command=self.dashboard)
      
      back_btn.pack()

    # !Afficher les mots de passe
    def show_view_passwords_screen(self):
        self.clear_window()
        title_label = tk.Label(self.root, text="Mots de passe enregistrés", font=("Helvetica", 18, "bold"))
        title_label.pack(pady=20)

        # Utilise la nouvelle méthode pour obtenir les mots de passe
        passwords = self.manager.get_passwords()
        if not passwords:
            messagebox.showinfo("Aucun mot de passe", "Aucun mot de passe enregistré.")
            self.dashboard()
            return

        for site, creds in passwords.items():
            password_info = f"{site} :\n    Nom d'utilisateur: {creds['username']}\n    Mot de passe: {creds['password']}"
            password_label = tk.Label(self.root, text=password_info, anchor="w", justify="left", font=("Arial", 12))
            password_label.pack(anchor="w", padx=20, pady=5)

        back_btn = tk.Button(self.root, text="Retour", command=self.dashboard)
        back_btn.pack(pady=10)

    def not_implemented(self):
        messagebox.showinfo("À venir", "Cette fonctionnalité sera bientôt disponible.")
    
    def clear_window(self):
      for widget in self.root.winfo_children():
        widget.destroy()

    def show_delete_password_screen(self):
        self.clear_window()
        title_label = tk.Label(self.root, text="Supprimer un mot de passe", font=("Helvetica", 18, "bold"))
        title_label.pack(pady=20)

        passwords = self.manager.get_passwords()
        if not passwords:
            messagebox.showinfo("Aucun mot de passe", "Aucun mot de passe enregistré.")
            self.dashboard()
            return

        sites = list(passwords.keys())
        var = tk.StringVar(value=sites[0])

        for site in sites:
            tk.Radiobutton(self.root, text=site, variable=var, value=site).pack(anchor="w", padx=20)

        def delete():
            site = var.get()
            if site:
                self.manager.supprimer_password_direct(site)
                messagebox.showinfo("Succès", f"Mot de passe pour '{site}' supprimé.")
                self.dashboard()

        tk.Button(self.root, text="Supprimer", command=delete, bg="red", fg="white").pack(pady=10)
        tk.Button(self.root, text="Retour", command=self.dashboard).pack(pady=5)

    def show_search_password_screen(self):
        self.clear_window()
        title_label = tk.Label(self.root, text="Rechercher un mot de passe", font=("Helvetica", 18, "bold"))
        title_label.pack(pady=20)

        search_label = tk.Label(self.root, text="Nom du site à rechercher :")
        search_label.pack()
        search_entry = tk.Entry(self.root)
        search_entry.pack()

        result_label = tk.Label(self.root, text="", font=("Arial", 12))
        result_label.pack(pady=10)

        def search():
            query = search_entry.get().lower()
            results = []
            passwords = self.manager.get_passwords()
            for site, creds in passwords.items():
                if query in site.lower():
                    results.append(f"{site} :\n    Nom d'utilisateur: {creds['username']}\n    Mot de passe: {creds['password']}")
            if results:
                result_label.config(text="\n\n".join(results))
            else:
                result_label.config(text="Aucun résultat trouvé.")

        tk.Button(self.root, text="Rechercher", command=search).pack(pady=5)
        tk.Button(self.root, text="Retour", command=self.dashboard).pack(pady=5)

    def show_edit_password_screen(self):
        self.clear_window()
        title_label = tk.Label(self.root, text="Modifier un mot de passe", font=("Helvetica", 18, "bold"))
        title_label.pack(pady=20)

        passwords = self.manager.get_passwords()
        if not passwords:
            messagebox.showinfo("Aucun mot de passe", "Aucun mot de passe enregistré.")
            self.dashboard()
            return

        sites = list(passwords.keys())
        var = tk.StringVar(value=sites[0])

        for site in sites:
            tk.Radiobutton(self.root, text=site, variable=var, value=site).pack(anchor="w", padx=20)

        username_label = tk.Label(self.root, text="Nouveau nom d'utilisateur (laisser vide pour ne pas changer) :")
        username_label.pack()
        username_entry = tk.Entry(self.root)
        username_entry.pack()

        password_label = tk.Label(self.root, text="Nouveau mot de passe (laisser vide pour ne pas changer) :")
        password_label.pack()
        password_entry = tk.Entry(self.root)
        password_entry.pack()

        def edit():
            site = var.get()
            if site:
                username = username_entry.get() or passwords[site]['username']
                password = password_entry.get() or passwords[site]['password']
                self.manager.ajouter_password_direct(site, username, password)
                messagebox.showinfo("Succès", f"Mot de passe pour '{site}' modifié.")
                self.dashboard()

        tk.Button(self.root, text="Modifier", command=edit).pack(pady=10)
        tk.Button(self.root, text="Retour", command=self.dashboard).pack(pady=5)

    def show_generate_password_screen(self):
        self.clear_window()
        title_label = tk.Label(self.root, text="Générer un mot de passe", font=("Helvetica", 18, "bold"))
        title_label.pack(pady=20)

        length_label = tk.Label(self.root, text="Longueur du mot de passe :")
        length_label.pack()
        length_entry = tk.Entry(self.root)
        length_entry.insert(0, "16")
        length_entry.pack()

        result_label = tk.Label(self.root, text="", font=("Arial", 12, "bold"))
        result_label.pack(pady=10)

        def generate():
            try:
                length = int(length_entry.get())
                password = self.manager.generer_mot_de_passe(length)
                result_label.config(text=password)
            except Exception:
                result_label.config(text="Erreur : longueur invalide.")

        tk.Button(self.root, text="Générer", command=generate).pack(pady=5)
        tk.Button(self.root, text="Retour", command=self.dashboard).pack(pady=5)
