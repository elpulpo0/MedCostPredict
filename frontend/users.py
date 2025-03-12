import streamlit as st
from utils import get_users


def users_page():
    """Affiche la liste des utilisateurs si admin."""
    st.title("Gestion des utilisateurs")

    users = get_users(st.session_state["token"])

    if not users:
        st.warning("Aucun utilisateur trouvé.")
        return

    for user in users:
        st.write(f"**Nom** : {user['full_name']}")
        st.write(f"**Email** : {user['email']}")
        st.write(f"**Rôle** : {user['role']}")
        st.write("---")
