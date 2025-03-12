import streamlit as st
from login import login_page
from home import home_page
from patients import patients_page
from users import users_page
from utils import (
    logout,
)

# 🔹 Initialisation de la session
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False
    st.session_state["role"] = None
    st.session_state["token"] = None

# 🔹 Gestion de la connexion
if not st.session_state["authenticated"]:
    login_page()
else:
    # 🔹 Affichage du bouton de déconnexion dans la sidebar
    if st.sidebar.button("🚪 Se déconnecter", key="logout"):
        logout()

    # 🔹 Définition des pages disponibles
    PAGES = {
        "🏠 Accueil": home_page,
        "👨‍⚕️ Patients": patients_page,
    }

    # 🔹 Ajouter la page "Utilisateurs" uniquement pour les admins
    if st.session_state["role"] == "admin":
        PAGES["👥 Utilisateurs"] = users_page

    # 🔹 Sélecteur de page dans la barre latérale
    selection = st.sidebar.radio("📍 Navigation", list(PAGES.keys()))

    # 🔹 Affichage de la page sélectionnée
    PAGES[selection]()
