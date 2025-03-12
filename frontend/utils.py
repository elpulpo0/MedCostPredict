import requests
import streamlit as st

API_URL = "http://127.0.0.1:8000"

def authenticate_user(email, password):
    """Vérifie les identifiants et retourne l'utilisateur avec son rôle."""
    response = requests.post(
        f"{API_URL}/token",
        data={"username": email, "password": password},
    )
    if response.status_code == 200:
        token = response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        user_response = requests.get(f"{API_URL}/users/me", headers=headers)

        if user_response.status_code == 200:
            user_data = user_response.json()
            return {
                "role": user_data["role"],
                "token": token,
            }
    return None


def get_patients(token):
    """Récupère la liste des patients via l'API."""
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{API_URL}/patients", headers=headers)
    return response.json() if response.status_code == 200 else []


def get_users(token):
    """Récupère la liste des utilisateurs si l'utilisateur est admin."""
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{API_URL}/users/", headers=headers)
    return response.json() if response.status_code == 200 else []


def create_user(full_name, email, password):
    """Crée un utilisateur via l'API."""
    response = requests.post(
        f"{API_URL}/users/",
        json={"full_name": full_name, "email": email, "password": password},
    )

    if response.status_code == 200:
        return True, "Compte créé avec succès"
    elif response.status_code == 400:
        return False, response.json()["detail"]
    else:
        return False, "Erreur lors de la création du compte"


def logout():
    """Déconnecte l'utilisateur en réinitialisant la session."""
    st.session_state.clear()  # ✅ Réinitialisation complète de la session
    st.success(
        "Déconnexion réussie ! Redirection vers la page de connexion..."
    )
    st.rerun()  # ✅ Recharge proprement Streamlit pour retourner à la connexion
